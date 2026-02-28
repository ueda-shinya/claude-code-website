"""
インタラクションテスト

- メニュータブ切替（coffee / sweets）
- FAQ アコーディオンの開閉
- プライバシーポリシーモーダルの開閉
- 数値カウンターが表示されること
"""
from playwright.sync_api import Page, expect


# ── メニュータブ ──────────────────────────────────────────────

def test_menu_tab_coffee_active_by_default(page: Page) -> None:
    """デフォルトでコーヒータブが選択されており、コーヒーパネルが表示されること"""
    page.locator("#menu").scroll_into_view_if_needed()

    coffee_tab = page.locator('#tab-coffee')
    # aria-selected="true" でアクティブ状態を確認
    expect(coffee_tab).to_have_attribute("aria-selected", "true")

    # コーヒーメニューパネルが表示されていること
    coffee_panel = page.locator('#panel-coffee')
    expect(coffee_panel).to_be_visible()


def test_menu_tab_switches_to_sweets(page: Page) -> None:
    """スイーツタブをクリックするとスイーツメニューが表示されること"""
    page.locator("#menu").scroll_into_view_if_needed()
    sweets_tab = page.locator('#tab-sweets')
    sweets_tab.click()
    page.wait_for_timeout(300)

    sweets_panel = page.locator('#panel-sweets')
    expect(sweets_panel).to_be_visible()

    coffee_panel = page.locator('#panel-coffee')
    expect(coffee_panel).to_be_hidden()


def test_menu_tab_switches_back_to_coffee(page: Page) -> None:
    """スイーツ→コーヒーと戻れること"""
    page.locator("#menu").scroll_into_view_if_needed()
    page.locator('#tab-sweets').click()
    page.wait_for_timeout(200)
    page.locator('#tab-coffee').click()
    page.wait_for_timeout(300)

    expect(page.locator('#panel-coffee')).to_be_visible()
    expect(page.locator('#panel-sweets')).to_be_hidden()


# ── FAQ アコーディオン ────────────────────────────────────────

def test_faq_answer_hidden_by_default(page: Page) -> None:
    """FAQ の回答が初期状態で非表示であること"""
    page.locator("#faq").scroll_into_view_if_needed()
    first_trigger = page.locator("#faq-trigger-1")
    expect(first_trigger).to_have_attribute("aria-expanded", "false")


def test_faq_opens_on_click(page: Page) -> None:
    """FAQ トリガーをクリックすると回答が展開されること"""
    page.locator("#faq").scroll_into_view_if_needed()
    trigger = page.locator("#faq-trigger-1")
    trigger.click()
    page.wait_for_timeout(400)

    expect(trigger).to_have_attribute("aria-expanded", "true")


def test_faq_closes_on_second_click(page: Page) -> None:
    """同じ FAQ を2回クリックすると閉じること"""
    page.locator("#faq").scroll_into_view_if_needed()
    trigger = page.locator("#faq-trigger-1")

    trigger.click()
    page.wait_for_timeout(300)
    expect(trigger).to_have_attribute("aria-expanded", "true")

    trigger.click()
    page.wait_for_timeout(300)
    expect(trigger).to_have_attribute("aria-expanded", "false")


# ── プライバシーモーダル ──────────────────────────────────────

def test_privacy_modal_opens(page: Page) -> None:
    """プライバシーポリシーリンクをクリックするとモーダルが表示されること"""
    page.locator("#contact").scroll_into_view_if_needed()
    modal = page.locator("#modal-privacy")

    # 初期は非表示
    expect(modal).to_be_hidden()

    privacy_link = page.locator(".js-privacy-open").first
    privacy_link.click()
    page.wait_for_timeout(300)

    expect(modal).to_be_visible()


def test_privacy_modal_closes(page: Page) -> None:
    """モーダルの × ボタンをクリックするとモーダルが非表示になること"""
    page.locator("#contact").scroll_into_view_if_needed()
    page.locator(".js-privacy-open").first.click()
    page.wait_for_timeout(300)

    # ボタン（×）を使って閉じる（オーバーレイと区別するため button タグを指定）
    close_btn = page.locator("#modal-privacy button.js-modal-close")
    close_btn.click()
    page.wait_for_timeout(300)

    expect(page.locator("#modal-privacy")).to_be_hidden()


# ── 統計カウンター ────────────────────────────────────────────

def test_stats_section_visible(page: Page) -> None:
    """stats セクションが DOM に存在し、カウンター要素があること"""
    page.locator("#stats").scroll_into_view_if_needed()
    counters = page.locator(".js-stats-counter")
    assert counters.count() > 0, "js-stats-counter 要素が見つかりません"
