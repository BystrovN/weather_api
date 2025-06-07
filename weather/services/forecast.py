from weather.models import ForecastOverride
from .open_weather_map import WeatherService


def save_forecast_override(data: dict) -> None:
    """Создание или обновление существующей записи модели ForecastOverride."""

    ForecastOverride.objects.update_or_create(
        city=data['city'],
        date=data['date'],
        defaults={
            'min_temperature': data['min_temperature'],
            'max_temperature': data['max_temperature'],
        },
    )


def get_forecast(data: dict) -> tuple[bool, dict]:
    """Прогноз погоды на день в запрошенном городе."""

    city, date = data['city'], data['date']
    override = ForecastOverride.objects.filter(city=city, date=date).first()

    if override:
        min = override.min_temperature
        max = override.max_temperature
    else:
        result = WeatherService().get_forecast(city, date)
        if not result.is_ok:
            return True, result.errors

        min = result.data['min']
        max = result.data['max']

    return False, {'min_temperature': min, 'max_temperature': max}
