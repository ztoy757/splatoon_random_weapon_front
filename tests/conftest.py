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


@pytest.fixture(scope="session")
def base_url():
    """環境変数からベースURLを取得、デフォルトはStreamlitアプリのURL"""
    # MOCKOON_API_URLが設定されている場合はそれを優先、そうでなければBASE_URLを使用
    return os.getenv("MOCKOON_API_URL", os.getenv("BASE_URL", "http://localhost:8501"))


@pytest.fixture(scope="session")
def evidence_dir():
    """スクリーンショット用の証跡ディレクトリを作成"""
    evidence_path = "./evidence"
    os.makedirs(evidence_path, exist_ok=True)
    return evidence_path
