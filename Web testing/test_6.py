from datetime import datetime
from pathlib import Path
from playwright.sync_api import expect


def test_fill(page):
    page.goto("https://demoqa.com/automation-practice-form", wait_until="domcontentloaded")

    page.locator("#firstName").fill("Abc")
    page.locator("#lastName").fill("Def")
    page.locator("#userEmail").fill("name@example.com")

    page.locator('label[for="gender-radio-1"]').click()

    page.locator("#userNumber").fill("1234567890")

    expect(page.locator("#dateOfBirthInput")).to_have_value(
        datetime.now().strftime("%d %b %Y")
    )

    page.locator("#subjectsInput").fill("Maths")
    page.keyboard.press("Enter")

    page.locator('label[for="hobbies-checkbox-1"]').click()
    page.locator('label[for="hobbies-checkbox-3"]').click()

    page.locator("#uploadPicture").set_input_files(str(Path("test.png")))

    page.locator("#currentAddress").fill("Some address")

    page.locator("#state").scroll_into_view_if_needed()
    page.locator("#state").click()
    page.locator("#react-select-3-option-0").click()

    page.locator("#city").click()
    page.locator("#react-select-4-option-0").click()

    footer_text = page.locator("footer").inner_text()
    assert "TOOLSQA.COM" in footer_text

    page.locator("#submit").scroll_into_view_if_needed()
    page.locator("#submit").click()

    expect(page.locator("#example-modal-sizes-title-lg")).to_have_text(
        "Thanks for submitting the form"
    )