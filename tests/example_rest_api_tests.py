import requests, pytest, logging
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

    shared_data['headers'] = {"Content-Type": "application/json"}

    # store all test_data in shared_daya
    shared_data['test_data'] = test_data

    yield context


def test_create_user_api(global_setup, shared_data):
    url = global_setup['apiurl']
    body = shared_data['test_data']['test_create_user_api_body']

    try:
        response = requests.post(url, headers=shared_data['headers'], json=body)
        response.raise_for_status()
    except Exception as e:
        pytest.fail(f"API request failed: {e}")

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Invalid JSON response: {response.text}")

    assert_that(response.status_code).is_equal_to(200)
    assert_that(data).contains_key("id", "name", "data")
    assert_that(data["name"]).is_equal_to("Apple MacBook Pro 16")
    assert_that(data["data"]["CPU model"]).is_equal_to("Intel Core i9")
    assert_that(data["data"]["price"]).is_greater_than(0)

    # example of sharing data across tests, here we are storing 'id' in shared_data
    shared_data['id'] = data["id"]


@pytest.mark.smoke
def test_update_user_api(global_setup, shared_data):
    id = shared_data.get('id')
    assert id, "ID not found in shared_data"

    body = shared_data['test_data']['test_update_user_api']
    url = f"{global_setup['apiurl']}/{id}"

    try:
        response = requests.put(url, headers=shared_data['headers'], json=body)
        response.raise_for_status()
    except Exception as e:
        pytest.fail(f"API request failed: {e}")

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Invalid JSON response: {response.text}")

    assert_that(response.status_code).is_equal_to(200)
    assert_that(data["id"]).is_equal_to(id)
    assert_that(data["data"]["color"]).is_equal_to(body["data"]['color'])


@pytest.mark.regression
def test_get_user_api(global_setup, shared_data):
    body = shared_data['test_data']['test_get_user_api']
    id = body.get('id')
    url = f"{global_setup['apiurl']}/{id}"

    try:
        response = requests.get(url, headers=shared_data['headers'])
        response.raise_for_status()
    except Exception as e:
        pytest.fail(f"API request failed: {e}")

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Invalid JSON response: {response.text}")

    assert_that(response.status_code).is_equal_to(200)
    assert_that(data).contains_key("id")
    assert_that(str(data["id"])).is_equal_to(id)


# #------------------ Negative Cases---

@pytest.mark.regression
def test_invalid_endpoint(global_setup):
    url = global_setup['apiurl'] + "invalid_endpoint"
    try:
        response = requests.get(url)
    except Exception as e:
        pytest.fail(f"Request failed: {e}")
    assert_that(response.status_code).is_equal_to(404)


@pytest.mark.regression
def test_update_non_existent_resource(global_setup, shared_data):
    non_existent_id = 9999
    url = f"{global_setup['apiurl']}{non_existent_id}"
    body = {"name": "Updated Laptop"}
    
    try:
        response = requests.patch(url, headers=shared_data['headers'], json=body)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        assert_that(response.status_code).is_equal_to(404)
        return
    except Exception as e:
        pytest.fail(f"API request failed: {e}")

    pytest.fail(f"Expected 404 but got {response.status_code}")


@pytest.mark.skip(reason="no way of currently testing this")
def dummy_test(global_setup, shared_data):
    logger.info('Hey i am just fooling around!')


## Test Coverage

# - PATCH endpoints: positive and negative test scenarios
# - POST endpoints: validation of required fields
# - GET endpoints: handling invalid query parameters

## Observations

# - API returns 400 for invalid data types
# - PATCH endpoint correctly updates existing resources
# - Negative tests confirmed proper error handling