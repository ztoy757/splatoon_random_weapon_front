import os
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    """環境変数に基づいてブラウザを設定"""
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """各テスト用に新しいページを作成"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()