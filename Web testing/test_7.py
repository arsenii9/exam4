from playwright.sync_api import expect


def test_radio_buttons(page):
    page.goto("https://demoqa.com/radio-button")

    yes = page.locator("#yesRadio")
    impressive = page.locator("#impressiveRadio")
    no = page.locator("#noRadio")

    assert yes.is_enabled()
    assert impressive.is_enabled()
    assert not no.is_enabled()


def test_checkbox_visibility(page):
    page.goto("https://demoqa.com/checkbox")

    home = page.locator(".rc-tree-title", has_text="Home")
    desktop = page.locator(".rc-tree-title", has_text="Desktop")
    toggle = page.locator(".rc-tree-switcher").first

    expect(home).to_be_visible()
    assert desktop.count() == 0

    toggle.click()

    expect(desktop).to_be_visible()


def test_dynamic_element(page):
    page.goto("https://demoqa.com/dynamic-properties")

    button = page.locator("#visibleAfter")

    assert button.count() == 0

    page.wait_for_selector("#visibleAfter")

    expect(button).to_be_visible()