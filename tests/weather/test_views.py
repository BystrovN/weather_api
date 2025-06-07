import pytest
from django.urls import reverse
from unittest.mock import patch

from weather.services.open_weather_map import ServiceResult


@patch('weather.views.WeatherService.get_current_weather')
def test_current_weather_success(mock_get_weather, client, weather_response_params):
    mock_get_weather.return_value = ServiceResult.ok({'temperature': 0, 'local_time': '00:00'})
    response = client.get(reverse('current-weather'), weather_response_params)

    assert response.status_code == 200
    assert 'temperature' in response.data
    assert 'local_time' in response.data


@patch('weather.views.WeatherService.get_current_weather')
def test_current_weather_fail(mock_get_weather, client, weather_response_params):
    mock_get_weather.return_value = ServiceResult.fail('City not found')
    response = client.get(reverse('current-weather'), weather_response_params)

    assert response.status_code == 400
    assert 'error' in response.data


def test_current_weather_missing_city(client):
    response = client.get(reverse('current-weather'))
    assert response.status_code == 400
    assert response.data['detail'] == 'city parameter is required'


@pytest.mark.django_db
@patch('weather.views.get_forecast')
def test_forecast_success(mock_get_forecast, client, forecast_response_params):
    min_temp_key = 'min_temperature'
    max_temp_key = 'max_temperature'

    mock_get_forecast.return_value = (False, {min_temp_key: 0, max_temp_key: 1})
    response = client.get(reverse('forecast-weather'), forecast_response_params)

    assert response.status_code == 200
    assert min_temp_key in response.data
    assert max_temp_key in response.data


@pytest.mark.django_db
@patch('weather.views.get_forecast')
def test_forecast_fail(mock_get_forecast, client, forecast_response_params):
    mock_get_forecast.return_value = (True, {'error': 'City not found'})
    response = client.get(reverse('forecast-weather'), forecast_response_params)

    assert response.status_code == 400
    assert 'error' in response.data


@patch('weather.views.save_forecast_override')
def test_forecast_save_success(mock_save, client, forecast_response_correct_body):
    response = client.post(reverse('forecast-weather'), forecast_response_correct_body, format='json')

    assert response.status_code == 200
    assert response.data['detail'] == 'Forecast saved successfully'
    mock_save.assert_called_once()


@pytest.mark.django_db
def test_forecast_save_fail(client, forecast_response_incorrect_body):
    response = client.post(reverse('forecast-weather'), forecast_response_incorrect_body, format='json')

    assert response.status_code == 400
    assert 'min_temperature' in response.data
