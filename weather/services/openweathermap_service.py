import os
from dataclasses import dataclass, field
from datetime import datetime
import logging

import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


@dataclass
class ServiceResult:
    status: str
    data: dict = field(default_factory=dict)
    errors: str = ''

    @classmethod
    def ok(cls, data: dict) -> "ServiceResult":
        """Создание экземпляра с успешным результатом."""
        return cls(status='ok', data=data, errors='')

    @classmethod
    def fail(cls, errors: str) -> "ServiceResult":
        """Создание экземпляра с неудачным результатом."""
        return cls(status='fail', data={}, errors=errors)

    @property
    def is_ok(self) -> bool:
        return self.status == 'ok'


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
            logger.error(f'{method} request to {url} error - {err}')
            return


class GeoService(OpenWeatherBase):
    """Геосервис OpenWeatherMap."""

    def __init__(self):
        super().__init__()
        self.geo_url = f'{self.BASE_URL}/geo/1.0/direct'

    def get_coordinates(self, city: str) -> ServiceResult:
        """Координаты запрошенного города."""
        params = {'q': city, 'limit': 1}
        response = self._api_request(self.geo_url, params=params)
        if not response:
            return ServiceResult.fail('Geocoding error')

        data = response.json()
        if not data:
            return ServiceResult.fail(f'City {city} not found.')

        city_data = data[0]
        latitude_key = 'lat'
        longitude_key = 'lon'
        if any(key not in city_data for key in (latitude_key, longitude_key)):
            return ServiceResult.fail('Geocoding error')

        return ServiceResult.ok(
            {
                latitude_key: city_data[latitude_key],
                longitude_key: city_data[longitude_key],
            }
        )


class WeatherService(OpenWeatherBase):
    """Сервис погоды OpenWeatherMap."""

    def __init__(self):
        super().__init__()
        self.geo_client = GeoService()
        self.weather_url = f'{self.BASE_URL}/data/3.0/onecall'

    def get_current_weather(self, city: str) -> ServiceResult:
        """Текущая температура и локальное время в запрошенном городе."""
        coords_result = self.geo_client.get_coordinates(city)
        if not coords_result.ok:
            return coords_result

        params = {
            'lat': coords_result.data['lat'],
            'lon': coords_result.data['lon'],
            'exclude': 'minutely,hourly,daily,alerts',
        }

        response = self._api_request(self.weather_url, params=params)
        if not response:
            return ServiceResult.fail('Error retrieving current weather data')

        data = response.json()
        current = data.get('current')
        timezone_offset = data.get('timezone_offset', 0)
        if not current:
            return ServiceResult.fail('Error retrieving current weather data')

        local_time = datetime.utcfromtimestamp(current['dt'] + timezone_offset).strftime('%H:%M')
        return ServiceResult.ok(
            {
                'temperature': current['temp'],
                'local_time': local_time,
            }
        )

    def get_forecast(self, city: str, target_date: datetime) -> ServiceResult:
        """Прогноз погоды по дате (min и max температура)."""
        coords_result = self.geo_client.get_coordinates(city)
        if not coords_result.ok:
            return coords_result

        url = f'{self.weather_url}/day_summary'
        params = {
            'lat': coords_result.data['lat'],
            'lon': coords_result.data['lon'],
            'date': target_date.strftime('%Y.%m.%d'),
        }
        response = self._api_request(url, params=params)
        if not response:
            return ServiceResult.fail('Error getting weather forecast')

        data = response.json()
        temperature = data.get('temperature')
        if not temperature:
            return ServiceResult.fail('Error getting weather forecast')

        return ServiceResult.ok(
            {
                'min': temperature['min'],
                'max': temperature['max'],
            }
        )
