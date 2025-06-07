from weather.models import ForecastOverride


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
