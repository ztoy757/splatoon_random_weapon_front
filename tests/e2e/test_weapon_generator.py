import re

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_weapon_generator_basic_flow(page: Page, base_url: str, evidence_dir: str):
    """武器ジェネレーターの基本機能をテスト"""
    # アプリケーションにアクセス
    page.goto(base_url)

    # ページの読み込み完了を待ち、初期スクリーンショットを撮影
    page.wait_for_load_state("networkidle")
    page.screenshot(path=f"{evidence_dir}/01_initial_page.png")

    # ページが正常に読み込まれたことを確認（Streamlitのデフォルトタイトルまたはアプリタイトル）
    expect(page).to_have_title(
        re.compile(r"Splatoon3 Random Weapon Generator|Streamlit")
    )

    # 武器生成ボタンを見つけてクリック（Streamlitのボタン要素）
    generate_button = page.get_by_text(re.compile(r"🎲.*ランダム武器を生成|ランダム武器を生成"))
    expect(generate_button).to_be_visible()

    generate_button.click()
    page.screenshot(path=f"{evidence_dir}/02_after_generate_click.png")

    # ローディング/アニメーションの完了を待つ
    page.wait_for_timeout(1000)

    # 武器カードまたは武器結果が表示されることを確認
    page.wait_for_selector(".weapon-card", timeout=10000)

    page.screenshot(path=f"{evidence_dir}/03_weapons_generated.png")


@pytest.mark.e2e
def test_weapon_generator_multiple_generations(
    page: Page, base_url: str, evidence_dir: str
):
    """武器を複数回生成するテスト"""
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    # 武器を複数回生成
    for i in range(3):
        generate_button = page.get_by_text(re.compile(r"🎲.*ランダム武器を生成|ランダム武器を生成"))
        generate_button.click()
        page.wait_for_timeout(2000)  # 生成処理の待機時間を長くする

        # 各生成のスクリーンショットを撮影
        page.screenshot(path=f"{evidence_dir}/04_generation_{i+1}.png")

    # ボタンがまだ機能することを確認
    expect(page.get_by_text(re.compile(r"🎲.*ランダム武器を生成|ランダム武器を生成"))).to_be_visible()


@pytest.mark.e2e
def test_page_accessibility(page: Page, base_url: str):
    """基本的なアクセシビリティテスト"""
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    # 必須要素の存在確認
    expect(page.get_by_text(re.compile(r"🎲.*ランダム武器を生成|ランダム武器を生成"))).to_be_visible()

    # ページが適切な見出し構造を持つことを確認
    headings = page.locator("h1, h2, h3")
    expect(headings.first).to_be_visible()
