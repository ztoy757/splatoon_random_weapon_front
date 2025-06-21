import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8501/")
    page.screenshot(path="./evidence/screenshot1.png")
    page.get_by_test_id("baseButton-primary").click()
    page.screenshot(path="./evidence/screenshot2.png")
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
