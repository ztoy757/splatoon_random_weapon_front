import os
import re
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def base_url():
    """環境変数からベースURLを取得、デフォルトはMockoonのURL"""
    return os.getenv("MOCKOON_API_URL", os.getenv("BASE_URL", "http://localhost:8501"))


@pytest.fixture(scope="session") 
def headless_mode():
    """環境変数からヘッドレスモードを取得、デフォルトはTrue"""
    return os.getenv("HEADLESS", "true").lower() == "true"


@pytest.fixture(scope="session")
def evidence_dir():
    """スクリーンショット用の証跡ディレクトリを作成"""
    evidence_path = "./evidence"
    os.makedirs(evidence_path, exist_ok=True)
    return evidence_path


def test_weapon_generator_basic_flow(page: Page, base_url: str, evidence_dir: str):
    """武器ジェネレーターの基本機能をテスト"""
    # アプリケーションにアクセス
    page.goto(base_url)
    
    # ページの読み込み完了を待ち、初期スクリーンショットを撮影
    page.wait_for_load_state("networkidle")
    page.screenshot(path=f"{evidence_dir}/01_initial_page.png")
    
    # ページが正常に読み込まれたことを確認
    expect(page).to_have_title(re="Splatoon|武器")
    
    # 武器生成ボタンを見つけてクリック
    generate_button = page.get_by_test_id("baseButton-primary")
    expect(generate_button).to_be_visible()
    
    generate_button.click()
    page.screenshot(path=f"{evidence_dir}/02_after_generate_click.png")
    
    # ローディング/アニメーションの完了を待つ
    page.wait_for_timeout(1000)
    
    # 武器カードまたは結果が表示されることを確認
    # 実装に応じてセレクタの調整が必要な場合があります
    page.wait_for_selector("[data-testid*='weapon'], .weapon-card, .weapon-result", timeout=5000)
    
    page.screenshot(path=f"{evidence_dir}/03_weapons_generated.png")


def test_weapon_generator_multiple_generations(page: Page, base_url: str, evidence_dir: str):
    """武器を複数回生成するテスト"""
    page.goto(base_url)
    page.wait_for_load_state("networkidle")
    
    # 武器を複数回生成
    for i in range(3):
        generate_button = page.get_by_test_id("baseButton-primary")
        generate_button.click()
        page.wait_for_timeout(500)  # クリック間の短い待機
        
        # 各生成のスクリーンショットを撮影
        page.screenshot(path=f"{evidence_dir}/04_generation_{i+1}.png")
    
    # ボタンがまだ機能することを確認
    expect(page.get_by_test_id("baseButton-primary")).to_be_enabled()


def test_page_accessibility(page: Page, base_url: str):
    """基本的なアクセシビリティテスト"""
    page.goto(base_url)
    page.wait_for_load_state("networkidle")
    
    # 必須要素の存在確認
    expect(page.get_by_test_id("baseButton-primary")).to_be_visible()
    
    # ページが適切な見出し構造を持つことを確認
    headings = page.locator("h1, h2, h3")
    expect(headings.first).to_be_visible()