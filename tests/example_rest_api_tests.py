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


# @pytest.mark.regression
# def test_get_user_api(global_setup, shared_data):
#     url = global_setup['apiurl'] + "objects/2/"

#     response = requests.get(url, headers=shared_data['headers'])
#     assert_that(response.status_code).is_equal_to(200)

#     response_data = response.json()
#     assert_that(response_data["id"]).is_equal_to("2")


@pytest.mark.smoke
def test_create_user_api(global_setup, shared_data):
    url = global_setup['apiurl'] + "objects/"
    
    # get data form test_data file
    body = shared_data['test_data']['test_create_user_api_body']

    response = requests.post(url, headers=shared_data['headers'], json=body)
    assert_that(response.status_code).is_equal_to(200)

    response_data = response.json()
    shared_data['id'] = response_data["id"]


@pytest.mark.skip(reason="no way of currently testing this")
def dummy_test(global_setup, shared_data):
    logger.info('Hey i am just fooling around!')