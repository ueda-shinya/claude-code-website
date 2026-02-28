"""
共通フィクスチャ定義

環境変数 TEST_BASE_URL でテスト対象を切り替えられる:
  set TEST_BASE_URL=http://localhost/claude-code-website/output/MY-SITE/
  python -m pytest tests/ -v
"""
import os
import pytest
from playwright.sync_api import Page, BrowserContext


def pytest_configure(config) -> None:
    """TEST_BASE_URL 環境変数が設定されていれば pytest-base-url に反映する"""
    env_url = os.environ.get("TEST_BASE_URL")
    if env_url:
        # pytest-base-url の --base-url オプションと同等の効果
        config.option.base_url = env_url


@pytest.fixture
def page(page: Page, base_url: str) -> Page:
    """デスクトップ (1280×800) で対象ページを開く"""
    page.set_viewport_size({"width": 1280, "height": 800})
    page.goto(base_url)
    return page


@pytest.fixture
def mobile_page(context: BrowserContext, base_url: str) -> Page:
    """モバイル (375×667 / iPhone SE 相当) で対象ページを開く"""
    page = context.new_page()
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto(base_url)
    return page


@pytest.fixture
def tablet_page(context: BrowserContext, base_url: str) -> Page:
    """タブレット (768×1024) で対象ページを開く"""
    page = context.new_page()
    page.set_viewport_size({"width": 768, "height": 1024})
    page.goto(base_url)
    return page
