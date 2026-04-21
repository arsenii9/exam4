import allure
from playwright.sync_api import Page
class PageAction:
    def __init__(self, page: Page):
        self.page = page

    def open_url(self, url: str):
        self.page.goto(url)

    def enter_text_to_element(self, locator: str, text: str):
        self.page.fill(locator, text)

    def click_element(self, locator: str):
        self.page.click(locator)

    def wait_redirect_for_url(self, url: str):
        self.page.wait_for_url(url)
        assert self.page.url == url, "Редирект на домашнюю старницу не произошел"

    def get_element_text(self, locator: str) -> str:
        return self.page.locator(locator).text_content()

    def wait_for_element(self, locator: str, state: str = "visible"):
        self.page.locator(locator).wait_for(state=state)

    def make_screenshot_and_attach_to_allure(self):
        screenshot_path = "screenshot.png"
        self.page.screenshot(path=screenshot_path, full_page=True)  # full_page=True для скриншота всей страницы

        # Прикрепление скриншота к Allure-отчёту
        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name="Screenshot after redirect", attachment_type=allure.attachment_type.PNG)

    def check_pop_up_element_with_text(self, text: str) -> bool:
        notification_locator = self.page.get_by_text(text)
        notification_locator.wait_for(state="visible")
        assert notification_locator.is_visible(), "Уведомление не появилось"

        notification_locator.wait_for(state="hidden")
        assert notification_locator.is_visible() == False, "Уведомление не исчезло"


class BasePage(PageAction): #Базовая логика доспустимая для всех страниц на сайте
    def __init__(self, page: Page):
        super().__init__(page)
        self.home_url = "https://dev-cinescope.coconutqa.ru/"

        # Общие локаторы для всех страниц на сайте
        self.home_button = "a[href='/' and text()='Cinescope']"
        self.all_movies_button = "a[href='/movies' and text()='Все фильмы']"

    def go_to_home_page(self):
        self.click_element(self.home_button)
        self.wait_redirect_for_url(self.home_url)

    def go_to_all_movies(self):
        self.click_element(self.all_movies_button)
        self.wait_redirect_for_url(f"{self.home_url}movies")


