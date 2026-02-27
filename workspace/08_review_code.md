# THE CORNER CAFE — コードレビュー

**対象:** 07_seo.html / 06_styles.css / 06_script.js / 06_form_handler.php
**総合:** 🔴 CRITICAL=4 / 🟡 WARNING=6 / 🟢 INFO=5

---

## 🔴 CRITICAL

**CRITICAL-01 — PHP メールヘッダーインジェクション（form_handler.php）**
`Reply-To` ヘッダーに `$email` を直接使用。`filter_var(FILTER_VALIDATE_EMAIL)` は通過するが `\r\n` を除去しない。
```php
$email_safe = str_replace(["\r", "\n"], '', $email);
$headers .= "Reply-To: {$email_safe}\r\n";
```

**CRITICAL-02 — `max-height` アニメーション（styles.css アコーディオン）**
`transition: max-height 0.35s ease` はlayoutプロパティでCLAUDE.md の「transform/opacityのみ」ルール違反。
→ JSで `maxHeight` を動的に設定する方式に変更。

**CRITICAL-03 — ヒーロー背景画像の preload 不足（07_seo.html）**
CSS背景画像はHTMLパース時に発見されずLCPが劣化。
```html
<link rel="preload" as="image" href="assets/images/hero.jpg">
```

**CRITICAL-04 — CSS未定義クラス（styles.css）**
以下のクラスがHTMLで使用されているがCSSに定義なし:
- `l-header__nav-item`
- `l-drawer__nav-item`
- `l-footer__nav-item`
- `p-stats__item`
- `c-form__server-error`（JSで動的生成）

---

## 🟡 WARNING

**WARNING-01 — CSRFトークン未実装（form_handler.php）**
CLAUDE.md「CSRFトークン検証推奨」に未対応。

**WARNING-02 — `session_regenerate_id()` 未呼び出し（form_handler.php）**
セッション固定攻撃への対策として、セッション開始後に `session_regenerate_id(true)` を推奨。

**WARNING-03 — ドロワーフォーカストラップ未実装（script.js）**
WCAG 2.1 AA はdialogのフォーカストラップを要求。Tabキーがドロワー外に抜ける。

**WARNING-04 — メニュータブのキーボード操作不足（script.js）**
WAI-ARIA Tabs パターンは ArrowLeft/ArrowRight キー対応を要求。クリックのみ実装。

**WARNING-05 — `escapeHtml()` が未使用（script.js）**
エラー表示は `textContent` を使用しており関数は不要。削除推奨。

**WARNING-06 — JSON-LDの priceRange 不一致（07_seo.html）**
`"¥600〜¥800"` だが実メニュー価格は ¥520〜¥750。

---

## 🟢 INFO / PASS

- `innerHTML` によるDOM挿入なし（全て `textContent`）— OK
- `htmlspecialchars(ENT_QUOTES | ENT_HTML5)` — OK
- `filter_var(FILTER_VALIDATE_EMAIL)` + 長さチェック — OK
- Honeypot: HTML/JS/PHP 全層実装 — OK
- レート制限（60秒/3回）— OK
- `aria-expanded` ハンバーガー・FAQ全ボタン — OK
- `role="alert" aria-live="polite"` 全エラー要素 — OK
- フォーム `for/id` 紐付け全フィールド — OK
- スキップナビゲーション — OK
- メディアクエリ `min-width` のみ — OK
- フォールド以下画像 `loading="lazy"` — OK
- FLOCSS命名規則 — OK
- `scroll` イベント `{ passive: true }` — OK
