from datetime import datetime, timedelta

from rest_framework import serializers

from .models import ForecastOverride


class ForecastRequestSerializer(serializers.Serializer):
    city = serializers.CharField()
    date = serializers.CharField()

    def validate_date(self, value):
        try:
            parsed_date = datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError:
            raise serializers.ValidationError('Invalid date format. Use dd.MM.yyyy')

        if parsed_date < datetime.now().date():
            raise serializers.ValidationError('Date cannot be in the past')

        max_days = 10
        if parsed_date > datetime.now().date() + timedelta(days=max_days):
            raise serializers.ValidationError(f'Date cannot be more than {max_days} days in the future')

        return parsed_date


class ForecastOverrideSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format='%d.%m.%Y', input_formats=['%d.%m.%Y'])

    class Meta:
        model = ForecastOverride
        fields = ('city', 'date', 'min_temperature', 'max_temperature')

    def validate(self, data):
        if data['min_temperature'] > data['max_temperature']:
            raise serializers.ValidationError(
                {'min_temperature': 'min_temperature must be less than or equal to max_temperature'}
            )
        return data
