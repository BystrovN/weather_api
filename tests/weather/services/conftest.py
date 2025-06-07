import pytest

from weather.services.open_weather_map import ServiceResult


@pytest.fixture
def geo_correct_response():
    return [{'zip': '90210', 'name': 'Beverly Hills', 'lat': 34.0901, 'lon': -118.4065, 'country': 'US'}]


@pytest.fixture
def geo_incorrect_response():
    return [{'name': 'Beverly Hills', 'lat': 34.0901}]


@pytest.fixture
def coords_result():
    return ServiceResult.ok({'lat': 34.0901, 'lon': -118.4065})


@pytest.fixture
def current_weather_correct_response():
    return {'current': {'dt': 1717766400, 'temp': 18.5}, 'timezone_offset': 3600}


@pytest.fixture
def current_weather_incorrect_response():
    return {'timezone_offset': 3600}


@pytest.fixture
def forecast_correct_response():
    return {'temperature': {'min': 12.3, 'max': 22.7}}


@pytest.fixture
def forecast_incorrect_response():
    return {'temperature': {}}


@pytest.fixture
def override_forecast_object():
    class Forecast:
        min_temperature = 8
        max_temperature = 18

    return Forecast()
