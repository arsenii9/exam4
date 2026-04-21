import requests
from Cinescope.constants import BASE_URL, ADMIN_EMAIL, ADMIN_PASSWORD, DEFAULT_UI_TIMEOUT
import pytest

from Cinescope.db_requester.db_helpers import DBHelper
from Cinescope.utils.data_generator import DataGenerator
from Cinescope.custom_requester.custom_requester import CustomRequester
from Cinescope.api.api_manager import ApiManager
from Cinescope.resources.user_creds import SuperAdminCreds
from Cinescope.entities.user import User
from Cinescope.constants_directory.roles import Roles
from Cinescope.models.base_models import TestUser
from sqlalchemy.orm import Session
from Cinescope.db_requester.db_client import get_db_session
from Cinescope.models.login_page_model import CinescopLoginPage
from Cinescope.common.tools import Tools



@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )


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
    user_data = test_user.model_dump(mode="json")

    response = api_manager.auth_api.register_user(user_data)
    user_id = response.json()["id"]

    login_data = {
        "email": test_user.email,
        "password": test_user.password
    }
    login_response = api_manager.auth_api.login_user(login_data)
    token = login_response.json()["accessToken"]

    api_manager.user_api.set_auth_token(token)

    yield {
        "id": user_id,
        "data": user_data
    }

    api_manager.user_api.delete_user(user_id)


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
    movie_id = response.json()["id"]

    yield {
        "id": movie_id,
        "data": data
    }

    api_admin.movies_api.delete_movie(movie_id)


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_api_manager = ApiManager(session)
        user_pool.append(user_api_manager)
        return user_api_manager

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session
    )

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.model_dump(mode="json")
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data["email"],
        creation_user_data["password"],
        [Roles.USER.value],
        new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def admin_user(user_session, super_admin, creation_user_data):
    new_session = user_session()
    admin_data = creation_user_data.copy()
    admin_data["email"] = DataGenerator.generate_random_email()

    create_response = super_admin.api.user_api.create_user(admin_data)
    user_id = create_response.json()["id"]

    super_admin.api.user_api.update_user(
        user_id=user_id,
        user_data={
            "roles": [Roles.ADMIN.value],
            "verified": True,
            "banned": False
        },
        expected_status=200
    )

    admin_user = User(
        admin_data["email"],
        admin_data["password"],
        [Roles.ADMIN.value],
        new_session
    )
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user


@pytest.fixture
def super_admin_user(user_session, super_admin, creation_user_data):
    new_session = user_session()
    super_admin_data = creation_user_data.copy()
    super_admin_data["email"] = DataGenerator.generate_random_email()

    create_response = super_admin.api.user_api.create_user(super_admin_data)
    user_id = create_response.json()["id"]

    super_admin.api.user_api.update_user(
        user_id=user_id,
        user_data={
            "roles": [Roles.SUPER_ADMIN.value],
            "verified": True,
            "banned": False
        },
        expected_status=200
    )

    super_admin_user = User(
        super_admin_data["email"],
        super_admin_data["password"],
        [Roles.SUPER_ADMIN.value],
        new_session
    )
    super_admin_user.api.auth_api.authenticate(super_admin_user.creds)
    return super_admin_user

@pytest.fixture(scope="module")
def db_session() -> Session:
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="module")
def db_helper(db_session) -> DBHelper:
    return DBHelper(db_session=db_session)


@pytest.fixture(scope="function")
def created_test_user(db_helper):
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    if db_helper.get_user_by_id(user.id):

        db_helper.delete_user(user)

@pytest.fixture(scope="session")  # Браузер запускается один раз для всей сессии
def browser(playwright):
    browser = playwright.chromium.launch(headless=True)  # headless=True для CI/CD, headless=False для локальной разработки
    yield browser  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    browser.close()  # Браузер закрывается после завершения всех тестов


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    log_name = f"trace_{Tools.get_timestamp()}.zip"
    trace_path = Tools.files_dir('playwright_trace', log_name)
    context.tracing.stop(path=trace_path)
    context.close()


@pytest.fixture(scope="function")  # Страница создается для каждого теста
def page(context):
    page = context.new_page()
    yield page  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    page.close()  # Страница закрывается после завершения теста


@pytest.fixture(scope="function")
def logged_in_ui_user(page, registered_user):
    login_page = CinescopLoginPage(page=page)
    login_page.open()
    login_page.login(
        registered_user["data"]["email"],
        registered_user["data"]["password"]
    )

    page.wait_for_load_state()

    return page
