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
