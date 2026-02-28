"""
汎用ブラウザ品質チェック

どの生成サイトでも使える。サイト固有のクラス名・ID に依存しない。

Phase 9 で以下のように実行する:
    python -m pytest tests/test_generic.py -v --tb=short
（TEST_BASE_URL 環境変数でテスト先を指定）
"""
import re
from playwright.sync_api import Page, expect, Request, Response


# ── 1. ページ基本 ────────────────────────────────────────────

def test_page_returns_200(page: Page, base_url: str) -> None:
    """トップページが HTTP 200 で返ること"""
    resp = page.request.get(base_url)
    assert resp.status == 200, f"HTTP {resp.status} が返りました（200 を期待）"


def test_title_exists(page: Page) -> None:
    """title タグが存在し、空でないこと"""
    title = page.title()
    assert title and len(title.strip()) > 0, "title が空です"


def test_h1_exactly_once(page: Page) -> None:
    """h1 がページ内に1つだけ存在すること（SEO 基本要件）"""
    count = page.locator("h1").count()
    assert count == 1, f"h1 が {count} 個あります（1つだけにすること）"


def test_meta_description_exists(page: Page) -> None:
    """meta description が存在し、内容が50文字以上あること"""
    meta = page.locator('meta[name="description"]')
    assert meta.count() == 1, "meta[name=description] が存在しません"
    content = meta.get_attribute("content") or ""
    assert len(content) >= 50, f"meta description が短すぎます ({len(content)}文字)"


def test_ogp_tags_exist(page: Page) -> None:
    """OGP 必須タグ（og:title / og:description / og:image）が揃っていること"""
    for prop in ("og:title", "og:description", "og:image"):
        tag = page.locator(f'meta[property="{prop}"]')
        assert tag.count() == 1, f'{prop} が見つかりません'
        assert tag.get_attribute("content"), f'{prop} の content が空です'


# ── 2. アセット読み込み ──────────────────────────────────────

def test_stylesheet_loads(page: Page) -> None:
    """CSS ファイルが正常に読み込まれること"""
    links = page.locator('link[rel="stylesheet"][href]')
    assert links.count() > 0, "link[rel=stylesheet] が見つかりません"

    for i in range(links.count()):
        href = links.nth(i).get_attribute("href") or ""
        if href.startswith("http"):
            url = href
        else:
            url = page.url.rstrip("/") + "/" + href.lstrip("/")
        resp = page.request.get(url)
        assert resp.status == 200, f"CSS の読み込みに失敗: {href} → HTTP {resp.status}"


def test_javascript_loads(page: Page) -> None:
    """JS ファイルが正常に読み込まれること"""
    scripts = page.locator('script[src]')
    if scripts.count() == 0:
        return  # JS なしサイトはスキップ

    for i in range(scripts.count()):
        src = scripts.nth(i).get_attribute("src") or ""
        if src.startswith("http"):
            url = src
        else:
            url = page.url.rstrip("/") + "/" + src.lstrip("/")
        resp = page.request.get(url)
        assert resp.status == 200, f"JS の読み込みに失敗: {src} → HTTP {resp.status}"


def test_all_images_load(page: Page) -> None:
    """全画像が読み込まれること（lazy-load も含む）"""
    # lazy-load をトリガーするためページ最下部にスクロール
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(600)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_load_state("networkidle")

    broken = page.evaluate("""() => {
        return Array.from(document.images)
            .filter(img => !img.complete || img.naturalWidth === 0)
            .map(img => img.src);
    }""")
    assert broken == [], "読み込めない画像:\n" + "\n".join(broken)


def test_images_have_alt(page: Page) -> None:
    """全 img 要素に alt 属性が設定されていること（アクセシビリティ）"""
    missing = page.evaluate("""() => {
        return Array.from(document.images)
            .filter(img => img.alt === undefined || img.alt === null)
            .map(img => img.src);
    }""")
    # alt="" は許容（装飾画像）、属性なしは NG
    assert missing == [], "alt 属性がない画像:\n" + "\n".join(missing)


# ── 3. モバイル表示 ──────────────────────────────────────────

def test_no_horizontal_overflow_mobile(mobile_page: Page) -> None:
    """モバイル (375px) で横スクロールが発生しないこと"""
    overflow = mobile_page.evaluate("""() => {
        return document.documentElement.scrollWidth > document.documentElement.clientWidth;
    }""")
    assert not overflow, "モバイル幅 (375px) で横スクロールが発生しています"


def test_no_horizontal_overflow_tablet(tablet_page: Page) -> None:
    """タブレット (768px) で横スクロールが発生しないこと"""
    overflow = tablet_page.evaluate("""() => {
        return document.documentElement.scrollWidth > document.documentElement.clientWidth;
    }""")
    assert not overflow, "タブレット幅 (768px) で横スクロールが発生しています"


# ── 4. JavaScript エラー ─────────────────────────────────────

def test_no_console_errors(page: Page, base_url: str) -> None:
    """JavaScript の console.error / uncaught error がないこと"""
    errors: list[str] = []

    def handle_console(msg):
        if msg.type == "error":
            errors.append(msg.text)

    def handle_pageerror(exc):
        errors.append(str(exc))

    # 新しいページで再読み込みして監視
    context = page.context
    new_page = context.new_page()
    new_page.on("console", handle_console)
    new_page.on("pageerror", handle_pageerror)
    new_page.goto(base_url)
    new_page.wait_for_load_state("networkidle")
    new_page.close()

    assert errors == [], "JavaScript エラーが検出されました:\n" + "\n".join(errors)


# ── 5. フォーム（存在する場合のみ） ──────────────────────────

def test_form_honeypot_hidden(page: Page) -> None:
    """フォームが存在する場合、Honeypot フィールドが非表示であること"""
    honeypot = page.locator('input[name="website"]')
    if honeypot.count() == 0:
        return  # フォームなしサイトはスキップ
    assert not honeypot.is_visible(), "Honeypot フィールドがユーザーに見えています"


def test_form_empty_submit_blocked(page: Page) -> None:
    """フォームが存在する場合、空送信でエラーが表示されること"""
    form = page.locator("form").first
    if form.count() == 0:
        return  # フォームなしサイトはスキップ

    # フォームまでスクロール
    form.scroll_into_view_if_needed()
    page.wait_for_timeout(200)

    # 送信ボタンを探してクリック
    submit = form.locator('button[type="submit"], input[type="submit"]').first
    if submit.count() == 0:
        return  # 送信ボタンが見つからない場合はスキップ

    submit.click()
    page.wait_for_timeout(400)

    # 成功メッセージが表示されていないことを確認（空送信でCVさせない）
    success_selectors = ["#form-success", ".form-success", "[data-success]"]
    for sel in success_selectors:
        el = page.locator(sel)
        if el.count() > 0 and el.is_visible():
            assert False, f"空送信なのにフォーム成功メッセージが表示されています ({sel})"


# ── 6. アクセシビリティ基本 ──────────────────────────────────

def test_skip_nav_exists(page: Page) -> None:
    """スキップナビゲーション（skip-to-content）リンクが存在すること"""
    skip = page.locator('a[href="#main"], a[href^="#skip"], .skip-nav, [class*="skip"]')
    assert skip.count() > 0, "スキップナビゲーションリンクが見つかりません"


def test_lang_attribute_exists(page: Page) -> None:
    """html 要素に lang 属性が設定されていること"""
    lang = page.locator("html").get_attribute("lang")
    assert lang and len(lang) > 0, 'html 要素に lang 属性がありません'
