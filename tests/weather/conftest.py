from datetime import date, timedelta

import pytest
from django.core.cache import cache
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def clear_cache_before_test():
    cache.clear()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def today():
    return date.today().strftime('%d.%m.%Y')


@pytest.fixture
def data_in_the_past():
    return (date.today() - timedelta(days=1)).strftime('%d.%m.%Y')


@pytest.fixture
def data_too_far():
    return (date.today() + timedelta(days=11)).strftime('%d.%m.%Y')


@pytest.fixture
def weather_response_params():
    return {'city': 'BlaBla'}


@pytest.fixture
def forecast_params_base(city='BlaBla'):
    return {'city': city}


@pytest.fixture
def forecast_response_correct_params(forecast_params_base, today):
    return {**forecast_params_base, 'date': today}


@pytest.fixture
def forecast_response_params_data_too_far(forecast_params_base, data_too_far):
    return {**forecast_params_base, 'date': data_too_far}


@pytest.fixture
def forecast_response_params_data_in_the_past(forecast_params_base, data_in_the_past):
    return {**forecast_params_base, 'date': data_in_the_past}


@pytest.fixture
def forecast_body_base(forecast_params_base):
    return {**forecast_params_base, 'min_temperature': 10, 'max_temperature': 20}


@pytest.fixture
def forecast_response_correct_body(forecast_body_base, today):
    return {**forecast_body_base, 'date': today}


@pytest.fixture
def forecast_response_body_incorrect_temp(forecast_body_base, today):
    return {
        **forecast_body_base,
        'date': today,
        'min_temperature': 20,
        'max_temperature': 10,
    }


@pytest.fixture
def forecast_response_body_data_too_far(forecast_body_base, data_too_far):
    return {**forecast_body_base, 'date': data_too_far}


@pytest.fixture
def forecast_response_body_data_in_the_past(forecast_body_base, data_in_the_past):
    return {**forecast_body_base, 'date': data_in_the_past}
