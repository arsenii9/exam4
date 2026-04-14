def test_add(page):
    page.goto("https://demoqa.com/webtables")

    add_button = page.locator("button", has_text="Add")
    add_button.click()

    registration_form_title = page.locator(".modal-content .modal-title", has_text="Registration Form")
    assert registration_form_title.is_visible()

    page.locator('input[placeholder="First Name"]').fill("Abc")

    page.get_by_role("textbox", name="Last Name").fill("Def")
    page.get_by_role("textbox", name="name@example.com").fill("abcdef@gmail.com")
    page.get_by_role("textbox", name="Age").fill("27")
    page.get_by_role("textbox", name="Salary").fill("50000")
    page.get_by_role("textbox", name="Department").fill("Abc")

    page.get_by_role("button", name="Submit").click()