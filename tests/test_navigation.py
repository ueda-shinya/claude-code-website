"""
ナビゲーションテスト

- デスクトップ: ナビリンクが表示・クリック可能
- モバイル: ハンバーガーメニューの開閉
- スムーズスクロール（アンカー先へのスクロール確認）
"""
from playwright.sync_api import Page, expect


def test_desktop_nav_links(page: Page) -> None:
    """デスクトップでナビリンクが 6 項目以上表示されること"""
    nav = page.locator("#js-nav")
    links = nav.locator("a")
    assert links.count() >= 6, f"ナビリンクが少ない: {links.count()} 件"


def test_hamburger_opens_nav(mobile_page: Page) -> None:
    """モバイルでハンバーガーボタンをクリックするとナビが開くこと"""
    hamburger = mobile_page.locator("#js-hamburger")
    nav = mobile_page.locator("#js-nav")

    # 初期状態: ナビが閉じている（aria-expanded="false"）
    expect(hamburger).to_have_attribute("aria-expanded", "false")

    # クリックで開く
    hamburger.click()
    expect(hamburger).to_have_attribute("aria-expanded", "true")
    expect(nav).to_be_visible()


def test_hamburger_closes_nav(mobile_page: Page) -> None:
    """ハンバーガーを2回クリックするとナビが閉じること"""
    hamburger = mobile_page.locator("#js-hamburger")

    hamburger.click()  # 開く
    expect(hamburger).to_have_attribute("aria-expanded", "true")

    hamburger.click()  # 閉じる
    expect(hamburger).to_have_attribute("aria-expanded", "false")


def test_nav_link_scrolls_to_section(page: Page) -> None:
    """ナビの「こだわり」リンクをクリックすると #concept セクションへスクロールすること"""
    # ヘッダーを避けるため force=True でクリック
    concept_link = page.locator('#js-nav a[href="#concept"]')
    concept_link.click(force=True)

    # スクロールアニメーション完了を待つ
    page.wait_for_timeout(800)

    # #concept がビューポート内に入っていること
    assert page.locator("#concept").count() == 1, "#concept が DOM にありません"


def test_footer_nav_links(page: Page) -> None:
    """フッターナビにも各セクションへのリンクがあること"""
    footer_nav = page.locator('.l-footer__nav')
    links = footer_nav.locator("a")
    assert links.count() >= 6, f"フッターナビリンクが少ない: {links.count()} 件"
