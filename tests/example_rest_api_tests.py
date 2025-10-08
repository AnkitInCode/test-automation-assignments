import requests
import pytest
import logging
from utils.get_env_details import get_env_details
from assertpy import assert_that
from utils.get_test_data import get_test_data

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def shared_data():
    '''using this fixture to share data across tests'''
    data = {}
    yield data


@pytest.fixture(scope="module")
def global_setup(request, shared_data):
    '''context will contain all env variables & env specific data stored in configs/env_data'''
    context = get_env_details(request)
    test_data = get_test_data(context)

    # store header in shared_data
    shared_data['headers'] = {
        'Authorization': context['envData']['apiToken'],
        'Content-Type': 'application/json'
    }

    # store all test_data in shared_daya
    shared_data['test_data'] = test_data

    yield context