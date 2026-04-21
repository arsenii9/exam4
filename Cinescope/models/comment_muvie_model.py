from Cinescope.models.base_ui_models import BasePage
from playwright.sync_api import Page


class CommentPageModel(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}movies/2450"
        self.review_textarea = "textarea[name='text'][placeholder='Написать отзыв']"
        self.rating_dropdown = "form button[role='combobox']"
        self.rating_option = "[role='option']:has-text('{rating}')"
        self.submit_review_button = "form button[type='submit']"

    def open(self):
        self.open_url(self.url)
        self.page.locator(self.review_textarea).wait_for(state="visible", timeout=10000)

    def fill_comment(self, text):
        self.page.locator(self.review_textarea).fill(text)

    def select_rating(self, rating):
        self.page.locator(self.rating_dropdown).click()
        self.page.locator(self.rating_option.format(rating=rating)).click()

    def submit_comment(self):
        self.page.locator(self.submit_review_button).click()
        self.page.wait_for_timeout(2000)
        self.page.reload()
        self.page.wait_for_load_state("networkidle")

    def check_is_comment_visible(self, text):
        return text in self.page.locator("body").inner_text()

    def comment(self, text, rating):
        self.fill_comment(text)
        self.select_rating(rating)
        self.submit_comment()