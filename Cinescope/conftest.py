import requests
from Cinescope.constants import BASE_URL, ADMIN_EMAIL, ADMIN_PASSWORD
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
    id = response.json()["id"]

    login_response = api_manager.auth_api.login_user(test_user)
    token = login_response.json()["accessToken"]

    api_manager.user_api.set_auth_token(token)

    yield {
        "id": id,
        "data": test_user
    }

    api_manager.user_api.delete_user(id)

@pytest.fixture
def api_admin(api_manager):
    admin_cred = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }

    login_response = api_manager.auth_api.login_user(admin_cred)
    token = login_response.json()["accessToken"]
    api_manager.movies_api.set_auth_token(token)

    return api_manager


@pytest.fixture
def created_movie(api_admin):
    data = DataGenerator.generate_movie_payload()

    response = api_admin.movies_api.post_movie(data=data)
    id = response.json()["id"]

    yield {
        "id": id,
        "data": data
    }
    api_admin.movies_api.delete_movie(id)