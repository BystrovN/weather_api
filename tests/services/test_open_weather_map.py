from datetime import datetime

from unittest.mock import patch, Mock

from weather.services.open_weather_map import WeatherService, GeoService, ServiceResult


@patch('weather.services.open_weather_map.requests.request')
def test_geo_service_success(mock_request, geo_correct_response):
    response = Mock()
    response.status_code = 200
    response.json.return_value = geo_correct_response
    mock_request.return_value = response

    result = GeoService().get_coordinates('Beverly Hills')

    assert isinstance(result, ServiceResult)
    assert result.is_ok
    assert 'lat' in result.data
    assert 'lon' in result.data


@patch('weather.services.open_weather_map.requests.request')
def test_geo_service_fail(mock_request, geo_incorrect_response):
    response = Mock()
    response.status_code = 200
    response.json.return_value = geo_incorrect_response
    mock_request.return_value = response

    result = GeoService().get_coordinates('Beverly Hills')

    assert isinstance(result, ServiceResult)
    assert not result.is_ok


@patch.object(GeoService, 'get_coordinates')
@patch('weather.services.open_weather_map.requests.request')
def test_get_current_weather_success(mock_request, mock_coords, coords_result, current_weather_correct_response):
    mock_coords.return_value = coords_result

    response = Mock()
    response.status_code = 200
    response.json.return_value = current_weather_correct_response
    mock_request.return_value = response

    result = WeatherService().get_current_weather('Abc')

    assert isinstance(result, ServiceResult)
    assert result.is_ok
    assert 'temperature' in result.data
    assert 'local_time' in result.data


@patch.object(GeoService, 'get_coordinates')
@patch('weather.services.open_weather_map.requests.request')
def test_get_current_weather_fail(mock_request, mock_coords, coords_result, current_weather_incorrect_response):
    mock_coords.return_value = coords_result

    response = Mock()
    response.status_code = 200
    response.json.return_value = current_weather_incorrect_response
    mock_request.return_value = response

    result = WeatherService().get_current_weather('Abc')

    assert isinstance(result, ServiceResult)
    assert not result.is_ok
    assert 'temperature' not in result.data


@patch.object(GeoService, 'get_coordinates')
@patch('weather.services.open_weather_map.requests.request')
def test_get_forecast_success(mock_request, mock_coords, coords_result, forecast_correct_response):
    mock_coords.return_value = coords_result

    response = Mock()
    response.status_code = 200
    response.json.return_value = forecast_correct_response
    mock_request.return_value = response

    date = datetime(2025, 6, 11)
    result = WeatherService().get_forecast('Abc', date)

    assert isinstance(result, ServiceResult)
    assert result.is_ok
    assert 'min' in result.data
    assert 'max' in result.data


@patch.object(GeoService, 'get_coordinates')
@patch('weather.services.open_weather_map.requests.request')
def test_get_forecast_fail(mock_request, mock_coords, coords_result, forecast_incorrect_response):
    mock_coords.return_value = coords_result

    response = Mock()
    response.status_code = 200
    response.json.return_value = forecast_incorrect_response
    mock_request.return_value = response

    result = WeatherService().get_forecast('Abc', datetime(2025, 6, 11))

    assert isinstance(result, ServiceResult)
    assert not result.is_ok
