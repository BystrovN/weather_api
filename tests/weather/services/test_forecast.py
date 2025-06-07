from unittest.mock import patch

from weather.services.forecast import get_forecast
from weather.services.open_weather_map import ServiceResult


@patch('weather.services.forecast.ForecastOverride.objects.filter')
@patch('weather.services.forecast.WeatherService.get_forecast')
def test_get_forecast_uses_override(mock_get_forecast, mock_filter, override_forecast_object):
    mock_filter.return_value.first.return_value = override_forecast_object
    is_error, data = get_forecast({'city': 'BlaBla', 'date': ''})

    assert not is_error
    assert data['min_temperature'] == override_forecast_object.min_temperature
    assert data['max_temperature'] == override_forecast_object.max_temperature
    mock_get_forecast.assert_not_called()


@patch('weather.services.forecast.ForecastOverride.objects.filter')
@patch('weather.services.forecast.WeatherService.get_forecast')
def test_get_forecast_uses_api_success(mock_get_forecast, mock_filter):
    min_temp, max_temp = 0, 1

    mock_filter.return_value.first.return_value = None
    mock_get_forecast.return_value = ServiceResult.ok({'min': min_temp, 'max': max_temp})
    is_error, data = get_forecast({'city': 'BlaBla', 'date': ''})

    assert not is_error
    assert data['min_temperature'] == min_temp
    assert data['max_temperature'] == max_temp
    mock_get_forecast.assert_called_once()


@patch('weather.services.forecast.ForecastOverride.objects.filter')
@patch('weather.services.forecast.WeatherService.get_forecast')
def test_get_forecast_uses_api_fail(mock_get_forecast, mock_filter):
    mock_filter.return_value.first.return_value = None
    mock_get_forecast.return_value = ServiceResult.fail('')
    is_error, _ = get_forecast({'city': 'BlaBla', 'date': ''})

    assert is_error
