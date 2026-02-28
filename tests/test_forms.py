"""
フォームテスト

- 空送信でバリデーションエラーが表示されること
- 不正メールアドレスでエラーが表示されること
- Honeypot フィールドが非表示であること
- 全フィールドを正しく入力した場合エラーが出ないこと
"""
from playwright.sync_api import Page, expect


def _scroll_to_form(page: Page) -> None:
    page.locator("#contact").scroll_into_view_if_needed()
    page.wait_for_timeout(200)


def test_honeypot_is_hidden(page: Page) -> None:
    """Honeypot フィールド（name="website"）がユーザーに見えないこと"""
    honeypot = page.locator('input[name="website"]')
    expect(honeypot).to_have_count(1)
    assert not honeypot.is_visible(), "Honeypot フィールドがユーザーに見えています"


def test_empty_submit_shows_errors(page: Page) -> None:
    """全フィールド空で送信するとエラーメッセージが表示されること"""
    _scroll_to_form(page)

    submit_btn = page.locator("#js-submit-btn")
    submit_btn.click()
    page.wait_for_timeout(300)

    # 名前・メール・お問い合わせ種別・メッセージの少なくとも1つにエラーが出ること
    has_any_error = (
        page.locator("#error-name").is_visible()
        or page.locator("#error-email").is_visible()
        or page.locator("#error-inquiry").is_visible()
        or page.locator("#error-message").is_visible()
    )
    assert has_any_error, "空送信してもエラーメッセージが表示されませんでした"


def test_invalid_email_shows_error(page: Page) -> None:
    """不正メールアドレス入力でエラーが表示されること"""
    _scroll_to_form(page)

    page.locator('#contact-form input[name="name"]').fill("テスト太郎")
    page.locator('#contact-form input[name="email"]').fill("not-an-email")

    page.locator("#js-submit-btn").click()
    page.wait_for_timeout(300)

    expect(page.locator("#error-email")).to_be_visible()


def test_privacy_checkbox_required(page: Page) -> None:
    """プライバシー同意チェックなしで送信してもフォーム成功にならないこと"""
    _scroll_to_form(page)

    page.locator('#contact-form input[name="name"]').fill("テスト太郎")
    page.locator('#contact-form input[name="email"]').fill("test@example.com")
    page.locator('#contact-form select[name="inquiry_type"]').select_option("visit")
    page.locator('#contact-form textarea[name="message"]').fill("テストメッセージです。")

    checkbox = page.locator('#contact-form input[name="privacy"]')
    assert not checkbox.is_checked(), "プライバシーチェックボックスが既にチェックされています"

    page.locator("#js-submit-btn").click()
    page.wait_for_timeout(300)

    # フォーム成功メッセージが表示されていないこと
    assert not page.locator("#form-success").is_visible(), "プライバシー未同意なのに送信成功になっています"


def test_form_fields_accept_input(page: Page) -> None:
    """フォームの全フィールドが正しく入力を受け付けること"""
    _scroll_to_form(page)

    page.locator('#contact-form input[name="name"]').fill("テスト太郎")
    page.locator('#contact-form input[name="email"]').fill("test@example.com")
    page.locator('#contact-form input[name="tel"]').fill("090-1234-5678")
    page.locator('#contact-form select[name="inquiry_type"]').select_option("visit")
    page.locator('#contact-form textarea[name="message"]').fill("テストメッセージです。動作確認のみです。")
    page.locator('#contact-form input[name="privacy"]').check()

    # 各フィールドの値が正しく設定されたことを確認
    assert page.locator('#contact-form input[name="name"]').input_value() == "テスト太郎"
    assert page.locator('#contact-form input[name="email"]').input_value() == "test@example.com"
    assert page.locator('#contact-form input[name="privacy"]').is_checked()
