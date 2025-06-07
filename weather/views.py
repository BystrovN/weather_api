from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ForecastRequestSerializer, ForecastOverrideSerializer
from .services.open_weather_map import WeatherService
from .services.forecast import save_forecast_override, get_forecast


class CurrentWeatherView(APIView):
    def get(self, request):
        """Текущая погода в запрошенном городе."""
        city = request.query_params.get('city')
        if not city:
            return Response({'detail': 'city parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        result = WeatherService().get_current_weather(city)
        if not result.is_ok:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(result.data)


class ForecastWeatherView(APIView):
    def get(self, request):
        """Прогноз погоды на день в запрошенном городе."""
        serializer = ForecastRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        is_error, data = get_forecast(serializer.validated_data)

        return Response(data, status=status.HTTP_400_BAD_REQUEST if is_error else status.HTTP_200_OK)

    def post(self, request):
        """Запись прогноза погоды для города."""
        serializer = ForecastOverrideSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        save_forecast_override(serializer.validated_data)

        return Response({'detail': 'Forecast saved successfully'}, status=status.HTTP_200_OK)
