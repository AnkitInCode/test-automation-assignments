import pytest, logging
from assertpy import assert_that
from tests.modules.manage_user import ManageUser
from utils.get_env_details import get_env_details
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

    # store all test_data in shared_daya
    shared_data['test_data'] = test_data
    yield context

@pytest.mark.smoke
def test_create_user_api_body(global_setup, shared_data):
    result = ManageUser().create_user(global_setup, shared_data)
    assert result is True

@pytest.mark.smoke
def test_put_update_user_api_body(global_setup, shared_data):
    result = ManageUser().update_user(global_setup, shared_data)
    assert result is True

@pytest.mark.smoke
def test_patch_update_user_api_body(global_setup, shared_data):
    result = ManageUser().edit_user(global_setup, shared_data)
    assert result is True

@pytest.mark.smoke
def test_get_user_api_body(global_setup, shared_data):
    result = ManageUser().get_user(global_setup, shared_data)
    assert result is True

@pytest.mark.negative_test
@pytest.mark.regression
def test_invalid_endpoint(global_setup, shared_data):
    result = ManageUser().invalid_endpoint(global_setup, shared_data)
    assert result is True

@pytest.mark.negative_test
@pytest.mark.regression
def test_patch_non_existent_resource(global_setup, shared_data):
    result = ManageUser().edit_non_existent_resource(global_setup, shared_data)
    assert result is True