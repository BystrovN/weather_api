from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ForecastRequestSerializer, ForecastOverrideSerializer
from .models import ForecastOverride
from .services.openweathermap import WeatherService
from .services.forecast import save_forecast_override


class CurrentWeatherView(APIView):

    def get(self, request):
        """Текущая погода в запрошенном городе."""
        city = request.query_params.get('city')
        if not city:
            return Response({'detail': 'city parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        result = WeatherService().get_current_weather(city)
        if not result.is_ok:
            return Response({'detail': result.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result.data, status=status.HTTP_200_OK)


class ForecastWeatherView(APIView):

    def get(self, request):
        """Прогноз погоды на день в запрошенном городе."""
        serializer = ForecastRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        city = serializer.validated_data['city']
        date = serializer.validated_data['date']
        override = ForecastOverride.objects.filter(city=city, date=date).first()

        if override:
            min = override.min_temperature
            max = override.max_temperature
        else:
            result = WeatherService().get_forecast(city, date)
            if not result.is_ok:
                return Response({'detail': result.errors}, status=status.HTTP_400_BAD_REQUEST)

            min = result.data['min']
            max = result.data['max']

        return Response({'min_temperature': min, 'max_temperature': max})

    def post(self, request):
        """Запись прогноза погоды для города."""
        serializer = ForecastOverrideSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        save_forecast_override(serializer.validated_data)

        return Response({'detail': 'Forecast saved successfully'}, status=status.HTTP_200_OK)
