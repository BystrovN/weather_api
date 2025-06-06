import os
from datetime import datetime
import logging

import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class OpenWeatherBase:
    BASE_URL: str = 'https://api.openweathermap.org'
    DEFAULT_REQUEST_TIMEOUT: int = 15

    def __init__(self):
        self.api_key = os.getenv('OPENWEATHERMAP_API_KEY')

    def _api_request(
        self, url: str, method: str = 'get', params: dict | None = None, timeout: int = DEFAULT_REQUEST_TIMEOUT
    ) -> requests.Response | None:
        """Запрос к OpenWeatherMap API."""
        try:
            if not params:
                params = {}

            params['appid'] = self.api_key
            params['units'] = 'metric'

            response = requests.request(method, url=url, params=params, timeout=timeout)
            logger.info(f'OpenWeatherMap response - {response.status_code}, {response.text}')
            response.raise_for_status()
            return response
        except requests.RequestException as err:
            logger.error(f'Ошибка {method} запроса к {url} - {err}')
            return


class GeoService(OpenWeatherBase):
    """Геосервис OpenWeatherMap."""

    def __init__(self):
        super().__init__()
        self.geo_url = f'{self.BASE_URL}/geo/1.0/direct'

    def get_coordinates(self, city: str) -> dict:
        """Координаты запрошенного города."""
        params = {'q': city, 'limit': 1}
        response = self._api_request(self.geo_url, params=params)
        if not response:
            raise Exception('Ошибка геокодирования')

        data = response.json()
        if not data:
            raise ValueError(f'Город {city} не найден.')

        city_data = data[0]
        latitude_key = 'lat'
        longitude_key = 'lon'
        if any(key not in city_data for key in (latitude_key, longitude_key)):
            raise Exception('Ошибка геокодирования')

        return {
            latitude_key: city_data[latitude_key],
            longitude_key: city_data[longitude_key],
        }


class WeatherService(OpenWeatherBase):
    """Сервис погоды OpenWeatherMap."""

    def __init__(self):
        super().__init__()
        self.geo_client = GeoService()
        self.weather_url = f'{self.BASE_URL}/data/3.0/onecall'

    def get_current_weather(self, city: str) -> dict:
        """Текущая температура и локальное время в запрошенном городе."""
        coords = self.geo_client.get_coordinates(city)
        params = {
            'lat': coords['lat'],
            'lon': coords['lon'],
            'exclude': 'minutely,hourly,daily,alerts',
        }

        response = self._api_request(self.weather_url, params=params)
        if not response:
            raise Exception('Ошибка получения данных о текущей погоде')

        data = response.json()
        current = data.get('current')
        timezone_offset = data.get('timezone_offset', 0)
        if not current:
            raise Exception('Ошибка получения данных о текущей погоде')

        local_time = datetime.utcfromtimestamp(current['dt'] + timezone_offset).strftime('%H:%M')
        return {
            'temperature': current['temp'],
            'local_time': local_time,
        }

    def get_forecast(self, city: str, target_date: datetime) -> dict | None:
        """Прогноз погоды по дате (min и max температура)."""
        coords = self.geo_client.get_coordinates(city)
        url = f'{self.weather_url}/day_summary'
        params = {
            'lat': coords['lat'],
            'lon': coords['lon'],
            'date': datetime.strptime(target_date, '%d.%m.%Y').strftime('%Y.%m.%d'),
        }
        response = self._api_request(url, params=params)
        if not response:
            raise Exception('Ошибка получения прогноза погоды')

        data = response.json()
        temperature = data.get('temperature')
        if not temperature:
            raise Exception('Ошибка получения прогноза погоды')

        return {
            'min_temperature': temperature['min'],
            'max_temperature': temperature['max'],
        }
