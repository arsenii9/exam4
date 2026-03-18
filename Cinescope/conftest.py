import requests
from Cinescope.constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
import pytest
from Cinescope.utils.data_generator import DataGenerator
from Cinescope.custom_requester.custom_requester import CustomRequester
from Cinescope.api.api_manager import ApiManager

@pytest.fixture
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture()
def non_auth_session():
    return requests.Session()

@pytest.fixture
def requester(non_auth_session):
    return CustomRequester(session=non_auth_session, base_url=BASE_URL)

@pytest.fixture
def api_manager(requester):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(requester.session)

@pytest.fixture
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user)
    user_id = response.json()["id"]

    login_response = api_manager.auth_api.login_user(test_user)
    token = login_response.json()["accessToken"]

    api_manager.user_api._update_session_headers(
        Authorization=f"Bearer {token}"
    )

    yield {
        "id": user_id,
        "data": test_user
    }

    api_manager.user_api.delete_user(user_id)
