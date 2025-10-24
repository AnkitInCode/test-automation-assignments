import requests, logging
from assertpy import assert_that

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class ManageUser:

    def create_user(self, global_setup, shared_data):
        url, body = global_setup['apiurl'], shared_data['test_data']['test_create_user_api_body']
        expected_status = body['expected_status_code']
        logger.info("Test Started: Create User API")
        try:

            try:
                response = requests.post(url, headers=global_setup['headers'], json=body)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Request successful | Status: {response.status_code}")
            except Exception as e:
                logger.error(f"API request failed: {e}")
            except ValueError:
                logger.error("Invalid JSON in API response: {response.text}")

            # Key validations
            assert_that(response.status_code).is_equal_to(expected_status)
            assert_that(data).contains_key("id", "name", "data")
            assert_that(data["name"]).is_equal_to(body["name"])
            assert_that(data["data"]["CPU model"]).is_equal_to(body["data"]["CPU model"])
            assert_that(data["data"]["price"]).is_greater_than(0)

            shared_data['id'] = data["id"]
            logger.info(f"User created successfully with ID: {shared_data['id']}")
            return True
        except (requests.exceptions.RequestException, AssertionError) as e:
            logger.error(f"Create User API failed: {e}")
            return False
    
    def update_user(self, global_setup, shared_data):
        logger.info("Test Started: Update User API")
        
        ManageUser().create_user(global_setup, shared_data)
        id = shared_data.get('id')
        assert id, "ID not found in shared_data"

        url = f"{global_setup['apiurl']}/{id}"
        body = shared_data['test_data']['test_create_user_api_body']
        path = shared_data['test_data']['test_put_update_user_api_body']['update_data']['path']
        expected_status = body['expected_status_code']

        nested_levels = ''
        for level in path.split('.'):
            nested_levels += f"['{level}']"

        exec(f"body{nested_levels} = shared_data['test_data']['test_put_update_user_api_body']['update_data']['value']")
        try:
            try:
                response = requests.put(url, headers=global_setup['headers'], json=body)
                response.raise_for_status()
                data = response.json()
                logger.info(f"PUT request successful | Status: {response.status_code}")
            except Exception as e:
                logger.error(f"API request failed: {e}")
            except ValueError:
                logger.error("Invalid JSON in API response: {response.text}")

            assert_that(response.status_code).is_equal_to(expected_status)
            assert_that(data["id"]).is_equal_to(id)
            assert_that(data["data"]["color"]).is_equal_to(body["data"]['color'])

            logger.info(f"User {id} updated successfully with color: {data['data']['color']}")
            return True
        except (requests.exceptions.RequestException, AssertionError) as e:
            logger.error(f"Update User API failed: {e}")
            return False

    def edit_user(self, global_setup, shared_data):
        logger.info("Test Started: Patch Update User API")
        ManageUser().create_user(global_setup, shared_data)
        id = shared_data.get('id')
        assert id, "ID not found in shared_data"

        url = f"{global_setup['apiurl']}/{id}"
        body = shared_data['test_data']['test_patch_update_user_api_body']
        expected_status = body['expected_status_code']

        try:
            try:
                response = requests.patch(url, headers=global_setup['headers'], json=body)
                response.raise_for_status()
                data = response.json()
                logger.info(f"PATCH request successful | Status: {response.status_code}")
            except Exception as e:
                logger.error(f"API request failed: {e}")
            except ValueError:
                logger.error("Invalid JSON in API response: {response.text}")

            assert_that(response.status_code).is_equal_to(expected_status)
            assert_that(data["id"]).is_equal_to(id)
            assert_that(data["name"]).is_equal_to(body["name"])

            logger.info(f"User {id} name updated successfully to: {data['name']}")
            return True
        except (requests.exceptions.RequestException, AssertionError) as e:
            logger.error(f"Edit User API failed: {e}")
            return False
    
    def get_user(self, global_setup, shared_data):
        logger.info("Test Started: Get User API")

        body = shared_data['test_data']['test_get_user_api_body']
        expected_status = body['expected_status_code']
        id = body.get('id')
        url = f"{global_setup['apiurl']}/{id}"
        try:
            try:
                response = requests.get(url, headers=global_setup['headers'])
                response.raise_for_status()
                data = response.json()
                logger.info(f"GET request successful | Status: {response.status_code}")
            except Exception as e:
                logger.error(f"API request failed: {e}")

            except ValueError:
                logger.error("Invalid JSON in API response: {response.text}")

            assert_that(response.status_code).is_equal_to(expected_status)
            assert_that(data).contains_key("id")
            assert_that(str(data["id"])).is_equal_to(id)

            logger.info(f"User data retrieved successfully for ID: {id}")
            return True
        except (requests.exceptions.RequestException, AssertionError) as e:
            logger.error(f"Get User API failed: {e}")
            return False
    
    def invalid_endpoint(self, global_setup, shared_data):
        logger.info("Test Started: Invalid Endpoint API")

        body = shared_data['test_data']['test_invalid_endpoint']
        endpoint = body['endpoint']
        expected_status = body['expected_status_code']
        url = global_setup['apiurl'] + endpoint
        try:
            try:
                response = requests.get(url)
                logger.info(f"Request sent to invalid endpoint | Status: {response.status_code}")
            except Exception as e:
                logger.error(f"Request failed: {e}")
            assert_that(response.status_code).is_equal_to(expected_status)
            logger.info("Verified response status 404 for invalid endpoint")
            return True
        except (requests.exceptions.RequestException, AssertionError) as e:
            logger.error(f"Invalid endpoint API failed: {e}")
            return False

    def edit_non_existent_resource(self, global_setup, shared_data):
        logger.info("Test Started: Update Non-Existent Resource API")

        api_data = shared_data['test_data']['test_patch_non_existent_resource']
        non_existent_id = api_data["non_existent_id"]
        expected_status = api_data["expected_status_code"]
        url = f"{global_setup['apiurl']}/{non_existent_id}"
        body = {"name": api_data["name"]}

        logger.info(f"Attempting PATCH on non-existent ID: {non_existent_id}")

        try:
            response = requests.patch(url, headers=global_setup['headers'], json=body)
            logger.info(f"Response Status: {response.status_code}")

            if response.status_code == expected_status:
                logger.info(f"Received expected {expected_status}")
                return True
            else:
                logger.error(f"Expected {expected_status}, got {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return False