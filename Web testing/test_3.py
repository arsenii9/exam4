from playwright.sync_api import Page, expect
from random import randint
import time


def test_registration(page: Page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')

    username_locator = '[name = "fullName"]'
    email_loacor = '[name = "email"]'
    password_locator = '[name = "password"]'
    repeat_password_locator = '[name = "passwordRepeat"]'

    user_email = f'test{randint(1, 9999)}-admin@email.qa'

    page.fill(username_locator, 'Жмышенко Валерий Альбертович')
    page.fill(email_loacor, user_email)
    page.fill(password_locator, 'qwerty123Q')
    page.fill(repeat_password_locator, 'qwerty123Q')

    page.get_by_role("button", name="Зарегистрироваться").click()

    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)

