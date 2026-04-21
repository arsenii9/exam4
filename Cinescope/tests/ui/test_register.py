import allure
import pytest

from Cinescope.models.register_page_model import CinescopRegisterPage
from Cinescope.utils.data_generator import DataGenerator


@allure.epic("Тестирование UI")
@allure.feature("Страница Register")
@pytest.mark.ui
class TestRegisterPage:

    @allure.title("Успешная регистрация нового пользователя")
    def test_register_by_ui(self, page):

        with allure.step("Подготовить данные пользователя"):
            random_email = DataGenerator.generate_random_email()
            random_name = DataGenerator.generate_random_name()
            random_password = DataGenerator.generate_random_password()

        register_page = CinescopRegisterPage(page)

        with allure.step("Открыть страницу регистрации"):
            register_page.open()

        with allure.step("Зарегистрировать нового пользователя"):
            register_page.register(
                f"PlaywrightTest {random_name}",
                random_email,
                random_password,
                random_password
            )

        with allure.step("Проверить редирект на страницу логина"):
            register_page.assert_was_redirect_to_login_page()

        with allure.step("Сделать скриншот страницы"):
            register_page.make_screenshot_and_attach_to_allure()

        with allure.step("Проверить появление и исчезновение алерта"):
            register_page.assert_allert_was_pop_up()