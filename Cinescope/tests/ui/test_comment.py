import pytest
import allure
from Cinescope.models.comment_muvie_model import CommentPageModel


@allure.epic("UI")
@allure.feature("Comments")
class TestComment:
    @pytest.mark.slow
    @pytest.mark.ui
    @allure.title("User can leave a comment under a movie")
    @allure.story("Create comment")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_comment(self, logged_in_ui_user):

        with allure.step("Open movie page"):
            page = CommentPageModel(logged_in_ui_user)
            page.open()

        text = "A poor movie about The Witcher that doesn't follow the original plot."

        with allure.step("Leave a comment"):
            page.comment(text=text, rating="2")

        with allure.step("Check that comment is visible on the page"):
            assert page.check_is_comment_visible(text=text)