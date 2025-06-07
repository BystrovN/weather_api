from rest_framework.test import APIClient

import pytest


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def weather_response_params():
    return {'city': 'BlaBla'}


@pytest.fixture
def forecast_response_params():
    return {'city': 'BlaBla', 'date': '11.06.2025'}


@pytest.fixture
def forecast_response_correct_body():
    return {
        'city': 'BlaBla',
        'date': '11.06.2025',
        'min_temperature': 10,
        'max_temperature': 20,
    }


@pytest.fixture
def forecast_response_incorrect_body():
    return {
        'city': 'BlaBla',
        'date': '11.06.2025',
        'min_temperature': 20,
        'max_temperature': 10,
    }
