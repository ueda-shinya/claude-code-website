"""
ページ基本確認テスト

- ページが正常に読み込まれること
- タイトル・メタタグが存在すること
- 全画像が HTTP 200 で返ること
- OGP タグが存在すること
"""
from playwright.sync_api import Page, expect


def test_page_loads(page: Page) -> None:
    """ページが正常に応答すること"""
    expect(page).not_to_have_url("about:blank")
    # ヒーローセクションが見えれば読み込み成功
    expect(page.locator(".p-hero")).to_be_visible()


def test_page_title(page: Page) -> None:
    """タイトルに店名が含まれること"""
    assert "THE CORNER CAFE" in page.title()


def test_meta_description(page: Page) -> None:
    """meta description が存在すること"""
    meta = page.locator('meta[name="description"]')
    expect(meta).to_have_count(1)
    content = meta.get_attribute("content")
    assert content and len(content) > 0


def test_ogp_tags(page: Page) -> None:
    """OGP タグ（og:title / og:description / og:image）が存在すること"""
    for prop in ("og:title", "og:description", "og:image"):
        tag = page.locator(f'meta[property="{prop}"]')
        expect(tag).to_have_count(1)
        assert tag.get_attribute("content")


def test_all_images_load(page: Page) -> None:
    """全 img 要素が正常に読み込まれること（broken image がないこと）"""
    # lazy-load 画像を全てトリガーするためページ末尾までスクロール
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    page.evaluate("window.scrollTo(0, 0)")

    # 全リソースの読み込み完了を待つ
    page.wait_for_load_state("networkidle")

    broken = page.evaluate("""() => {
        return Array.from(document.images)
            .filter(img => !img.complete || img.naturalWidth === 0)
            .map(img => img.src);
    }""")
    assert broken == [], "読み込めない画像があります:\n" + "\n".join(broken)


def test_h1_exists_once(page: Page) -> None:
    """h1 が1つだけ存在すること"""
    expect(page.locator("h1")).to_have_count(1)


def test_main_sections_visible(page: Page) -> None:
    """主要セクションが全て DOM に存在すること"""
    sections = ["#concept", "#menu", "#gallery", "#testimonials", "#faq", "#access", "#contact"]
    for section_id in sections:
        assert page.locator(section_id).count() == 1, f"{section_id} が見つかりません"
