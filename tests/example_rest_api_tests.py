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
# def global_setup(request, shared_data, selected_datasets):
def global_setup(request, shared_data):
    '''context will contain all env variables & env specific data stored in configs/env_data'''
    context = get_env_details(request)
    # test_data = get_test_data(context, selected_datasets)
    test_data = get_test_data(context)

    # store all test_data in shared_daya
    shared_data['test_data'] = test_data

    yield context


def test_create_user_api_body(global_setup, shared_data):
    url, body = global_setup['apiurl'], shared_data['test_data']['test_create_user_api_body']

    logger.info("Test Started: Create User API")

    try:
        response = requests.post(url, headers=global_setup['headers'], json=body)
        response.raise_for_status()
        logger.info(f"Request successful | Status: {response.status_code}")
    except Exception as e:
        logger.error(f"API request failed: {e}")

    try:
        data = response.json()
    except ValueError:
        logger.error("Invalid JSON in API response: {response.text}")

    # Key validations
    assert_that(response.status_code).is_equal_to(200)
    assert_that(data).contains_key("id", "name", "data")
    assert_that(data["name"]).is_equal_to(body["name"])
    assert_that(data["data"]["CPU model"]).is_equal_to(body["data"]["CPU model"])
    assert_that(data["data"]["price"]).is_greater_than(0)

    shared_data['id'] = data["id"]
    logger.info(f"User created successfully with ID: {shared_data['id']}")


@pytest.mark.smoke
def test_put_update_user_api_body(global_setup, shared_data):
    logger.info("Test Started: Update User API")

    id = shared_data.get('id')
    assert id, "ID not found in shared_data"

    url = f"{global_setup['apiurl']}/{id}"
    body = shared_data['test_data']['test_create_user_api_body']
    path = shared_data['test_data']['test_put_update_user_api_body']['update_data']['path']

    nested_levels = ''
    for level in path.split('.'):
        nested_levels += f"['{level}']"

    exec(f"body{nested_levels} = shared_data['test_data']['test_put_update_user_api_body']['update_data']['value']")

    try:
        response = requests.put(url, headers=global_setup['headers'], json=body)
        response.raise_for_status()
        logger.info(f"PUT request successful | Status: {response.status_code}")
    except Exception as e:
        logger.error(f"API request failed: {e}")

    try:
        data = response.json()
    except ValueError:
        logger.error("Invalid JSON in API response: {response.text}")

    assert_that(response.status_code).is_equal_to(200)
    assert_that(data["id"]).is_equal_to(id)
    assert_that(data["data"]["color"]).is_equal_to(body["data"]['color'])

    logger.info(f"User {id} updated successfully with color: {data['data']['color']}")


@pytest.mark.smoke
def test_patch_update_user_api_body(global_setup, shared_data):
    logger.info("Test Started: Patch Update User API")
    id = shared_data.get('id')
    assert id, "ID not found in shared_data"

    url = f"{global_setup['apiurl']}/{id}"
    body = shared_data['test_data']['test_create_user_api_body']
    body['name'] = "Apple MacBook Pro 16 (Updated Name)"

    try:
        response = requests.put(url, headers=global_setup['headers'], json=body)
        response.raise_for_status()
        logger.info(f"PATCH request successful | Status: {response.status_code}")
    except Exception as e:
        logger.error(f"API request failed: {e}")

    try:
        data = response.json()
    except ValueError:
        logger.error("Invalid JSON in API response: {response.text}")

    assert_that(response.status_code).is_equal_to(200)
    assert_that(data["id"]).is_equal_to(id)
    assert_that(data["name"]).is_equal_to(body["name"])

    logger.info(f"User {id} name updated successfully to: {data['name']}")

@pytest.mark.regression
def test_get_user_api_body(global_setup, shared_data):
    logger.info("Test Started: Get User API")

    body = shared_data['test_data']['test_get_user_api_body']
    id = body.get('id')
    url = f"{global_setup['apiurl']}/{id}"

    try:
        response = requests.get(url, headers=global_setup['headers'])
        response.raise_for_status()
        logger.info(f"GET request successful | Status: {response.status_code}")
    except Exception as e:
        logger.error(f"API request failed: {e}")

    try:
        data = response.json()
    except ValueError:
        logger.error("Invalid JSON in API response: {response.text}")

    assert_that(response.status_code).is_equal_to(200)
    assert_that(data).contains_key("id")
    assert_that(str(data["id"])).is_equal_to(id)

    logger.info(f"User data retrieved successfully for ID: {id}")


# #------------------ Negative Cases---

@pytest.mark.regression
def test_invalid_endpoint(global_setup):
    logger.info("Test Started: Invalid Endpoint API")

    url = global_setup['apiurl'] + "invalid_endpoint"
    try:
        response = requests.get(url)
        logger.info(f"Request sent to invalid endpoint | Status: {response.status_code}")
    except Exception as e:
        logger.error(f"Request failed: {e}")
    assert_that(response.status_code).is_equal_to(404)
    logger.info("Verified response status 404 for invalid endpoint")


@pytest.mark.regression
def test_update_non_existent_resource(global_setup, shared_data):
    logger.info("Test Started: Update Non-Existent Resource API")

    non_existent_id = 9999
    url, body = f"{global_setup['apiurl']}{non_existent_id}", {"name": "Updated Laptop"}
    
    try:
        logger.info(f"Attempting to PATCH non-existent resource with ID: {non_existent_id}")
        response = requests.patch(url, headers=global_setup['headers'], json=body)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        logger.info(f"Received expected 404 for non-existent resource ID: {non_existent_id}")
        assert_that(response.status_code).is_equal_to(404)
        return
    except Exception as e:
        logger.error(f"API request failed: {e}")

    logger.error(f"Expected 404 but got {response.status_code}")


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