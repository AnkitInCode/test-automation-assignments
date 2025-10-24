import requests, logging
from assertpy import assert_that

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class ManageUser:

    def create_user(self, global_setup, shared_data):
        url, body = global_setup['apiurl'], shared_data['test_data']['test_create_user_api_body']

        logger.info("Test Started: Create User API")
        try:

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
            return True
        except (requests.exceptions.RequestException, AssertionError) as e:
            logger.error(f"Create User API failed: {e}")
            return False
    
    def update_user(self, global_setup, shared_data):
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
            try:
                response = requests.put(url, headers=global_setup['headers'], json=body)
                response.raise_for_status()
                logger.info(f"PUT request successful | Status: {response.status_code}")
                # breakpoint()
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
            return True
        except (requests.exceptions.RequestException, AssertionError) as e:
            logger.error(f"Update User API failed: {e}")
            return False
