from django.urls import path

from .views import CurrentWeatherView, ForecastWeatherView

urlpatterns = [
    path('current/', CurrentWeatherView.as_view(), name='current-weather'),
    path('forecast/', ForecastWeatherView.as_view(), name='forecast-weather'),
]
