import html
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_imports():
    """Test that main modules can be imported without errors."""
    try:
        import streamlit_app

        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import streamlit_app: {e}")


def test_basic_functionality():
    """Basic test to ensure the module loads correctly."""
    import streamlit_app

    assert hasattr(streamlit_app, 'st')


def test_html_sanitization():
    """Test HTML sanitization functionality."""
    import streamlit_app

    # テスト用のXSSペイロードを含む武器データ
    malicious_weapon = {
        "name": "<script>alert('XSS')</script>",
        "category": "<img src=x onerror=alert('XSS')>",
        "sub_weapon": "<iframe src='javascript:alert(\"XSS\")'></iframe>",
        "special_weapon": "<svg onload=alert('XSS')>",
    }

    # HTMLエスケープのテスト
    safe_name = html.escape(str(malicious_weapon.get("name", "不明")))
    safe_category = html.escape(str(malicious_weapon.get("category", "不明")))
    safe_sub_weapon = html.escape(str(malicious_weapon.get("sub_weapon", "不明")))
    safe_special_weapon = html.escape(str(malicious_weapon.get("special_weapon", "不明")))

    # スクリプトタグが適切にエスケープされていることを確認
    assert "&lt;script&gt;" in safe_name
    assert "&lt;img" in safe_category
    assert "&lt;iframe" in safe_sub_weapon
    assert "&lt;svg" in safe_special_weapon

    # エスケープ後にスクリプトタグが含まれていないことを確認
    assert "<script>" not in safe_name
    assert "<img" not in safe_category
    assert "<iframe" not in safe_sub_weapon
    assert "<svg" not in safe_special_weapon


def test_weapon_service_initialization():
    """Test WeaponService initialization with environment variables."""
    import streamlit_app

    # デフォルト値でのテスト
    service = streamlit_app.WeaponService()
    assert service.base_url == "http://mockoon:3000"

    # 環境変数でのテスト（モック）
    import os

    original_env = os.environ.get("MOCKOON_API_URL")

    try:
        os.environ["MOCKOON_API_URL"] = "http://test:8080"
        service = streamlit_app.WeaponService()
        assert service.base_url == "http://test:8080"
    finally:
        # 環境変数を元に戻す
        if original_env is not None:
            os.environ["MOCKOON_API_URL"] = original_env
        elif "MOCKOON_API_URL" in os.environ:
            del os.environ["MOCKOON_API_URL"]

    # 明示的な値でのテスト
    service = streamlit_app.WeaponService("http://custom:9000")
    assert service.base_url == "http://custom:9000"
