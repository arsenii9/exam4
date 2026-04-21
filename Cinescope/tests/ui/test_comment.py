import pytest
import allure

from Cinescope.models.comment_muvie_model import CommentPageModel


@allure.epic("Тестирование UI")
@allure.feature("Страница комментариев")
class TestComment:
    @pytest.mark.xfail(reason="BUG: падает из-за ошибки 404 при открытии любого фильма в продукте", strict=True)
    @pytest.mark.slow
    @pytest.mark.ui
    @allure.title("Успешное добавление комментария к фильму")
    @allure.story("Создание комментария")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_comment(self, logged_in_ui_user):
        page = CommentPageModel(logged_in_ui_user)

        with allure.step("Открыть страницу фильма"):
            page.open()

        text = "A poor movie about The Witcher that doesn't follow the original plot."

        with allure.step("Оставить комментарий с оценкой"):
            page.comment(text=text, rating="2")

        with allure.step("Проверить отображение комментария на странице"):
            assert page.check_is_comment_visible(text=text)