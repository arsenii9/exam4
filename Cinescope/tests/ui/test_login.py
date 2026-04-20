import allure
import pytest

from Cinescope.models.login_page_model import CinescopLoginPage


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestloginPage:
    @allure.title("Проведение успешного входа в систему")
    def test_login_by_ui(self, page, registered_user):
        login_page = CinescopLoginPage(page)

        with allure.step("Открыть страницу логина"):
            login_page.open()

        with allure.step("Выполнить вход в систему"):
            login_page.login(
                registered_user["data"]["email"],
                registered_user["data"]["password"]
            )

        with allure.step("Проверить редирект на главную страницу"):
            login_page.assert_was_redirect_to_home_page()

        with allure.step("Прикрепить скриншот в Allure"):
            login_page.make_screenshot_and_attach_to_allure()

        with allure.step("Проверить появление и исчезновение алерта"):
            login_page.assert_allert_was_pop_up()