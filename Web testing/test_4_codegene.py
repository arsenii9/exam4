from playwright.sync_api import Playwright, sync_playwright, expect

def test_run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://demoqa.com/text-box")

    page.get_by_role("textbox", name="Full Name").fill("Name")
    page.get_by_role("textbox", name="name@example.com").fill("test@email.com")
    page.get_by_role("textbox", name="Current Address").fill("Address")
    page.locator("#permanentAddress").fill("Pay Address")

    page.get_by_role("button", name="Submit").click()

    expect(page.locator("#output")).to_be_visible()
    expect(page.locator("#name")).to_contain_text("Name")
    expect(page.locator("#email")).to_contain_text("test@email.com")

    context.close()
    browser.close()


with sync_playwright() as playwright:
    test_run(playwright)