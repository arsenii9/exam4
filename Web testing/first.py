from playwright.sync_api import sync_playwright
import time

from pytest_playwright.pytest_playwright import browser

with sync_playwright() as p:
    browser1 = p.chromium.launch(headless=False)
    context1 = browser1.new_context()
    context2 = browser1.new_context()

    page11 = context1.new_page()
    page12 = context1.new_page()

    page21 = context2.new_page()
    page22 = context2.new_page()

    page11.goto("https://www.google.com")