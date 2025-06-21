import os
import re
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def base_url():
    """Get base URL from environment variable or default to localhost"""
    return os.getenv("BASE_URL", "http://localhost:8501")


@pytest.fixture(scope="session") 
def headless_mode():
    """Get headless mode from environment variable or default to True"""
    return os.getenv("HEADLESS", "true").lower() == "true"


@pytest.fixture(scope="session")
def evidence_dir():
    """Create evidence directory for screenshots"""
    evidence_path = "./evidence"
    os.makedirs(evidence_path, exist_ok=True)
    return evidence_path


def test_weapon_generator_basic_flow(page: Page, base_url: str, evidence_dir: str):
    """Test basic weapon generator functionality"""
    # Navigate to the application
    page.goto(base_url)
    
    # Wait for page to load and take initial screenshot
    page.wait_for_load_state("networkidle")
    page.screenshot(path=f"{evidence_dir}/01_initial_page.png")
    
    # Verify the page loaded correctly
    expect(page).to_have_title(re="Splatoon|武器")
    
    # Find and click the weapon generation button
    generate_button = page.get_by_test_id("baseButton-primary")
    expect(generate_button).to_be_visible()
    
    generate_button.click()
    page.screenshot(path=f"{evidence_dir}/02_after_generate_click.png")
    
    # Wait for any potential loading/animation
    page.wait_for_timeout(1000)
    
    # Verify that weapon cards or results are displayed
    # This assumes weapon cards have some identifiable element after generation
    # You may need to adjust the selector based on actual implementation
    page.wait_for_selector("[data-testid*='weapon'], .weapon-card, .weapon-result", timeout=5000)
    
    page.screenshot(path=f"{evidence_dir}/03_weapons_generated.png")


def test_weapon_generator_multiple_generations(page: Page, base_url: str, evidence_dir: str):
    """Test generating weapons multiple times"""
    page.goto(base_url)
    page.wait_for_load_state("networkidle")
    
    # Generate weapons multiple times
    for i in range(3):
        generate_button = page.get_by_test_id("baseButton-primary")
        generate_button.click()
        page.wait_for_timeout(500)  # Brief pause between clicks
        
        # Take screenshot of each generation
        page.screenshot(path=f"{evidence_dir}/04_generation_{i+1}.png")
    
    # Verify the button is still functional
    expect(page.get_by_test_id("baseButton-primary")).to_be_enabled()


def test_page_accessibility(page: Page, base_url: str):
    """Basic accessibility test"""
    page.goto(base_url)
    page.wait_for_load_state("networkidle")
    
    # Check for essential elements
    expect(page.get_by_test_id("baseButton-primary")).to_be_visible()
    
    # Ensure page has proper heading structure
    headings = page.locator("h1, h2, h3")
    expect(headings.first).to_be_visible()