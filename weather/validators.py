from datetime import datetime, timedelta

from rest_framework import serializers


def validate_forecast_date(value: datetime.date) -> datetime.date:
    today = datetime.now().date()

    if value < today:
        raise serializers.ValidationError('Date cannot be in the past')

    max_days = 10
    if value > today + timedelta(days=max_days):
        raise serializers.ValidationError(f'Date cannot be more than {max_days} days in the future')

    return value
