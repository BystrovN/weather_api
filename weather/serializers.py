from rest_framework import serializers

from .models import ForecastOverride
from .validators import validate_forecast_date


class ForecastRequestSerializer(serializers.Serializer):
    city = serializers.CharField()
    date = serializers.DateField(input_formats=['%d.%m.%Y'])

    def validate_date(self, value):
        return validate_forecast_date(value)


class ForecastOverrideSerializer(serializers.ModelSerializer):
    date = serializers.DateField(input_formats=['%d.%m.%Y'])

    class Meta:
        model = ForecastOverride
        fields = ('city', 'date', 'min_temperature', 'max_temperature')

    def validate_date(self, value):
        return validate_forecast_date(value)

    def validate(self, data):
        if data['min_temperature'] > data['max_temperature']:
            raise serializers.ValidationError(
                {'min_temperature': 'min_temperature must be less than or equal to max_temperature'}
            )
        return data
