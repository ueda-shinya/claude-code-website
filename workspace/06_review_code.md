# THE CORNER CAFE — コードレビュー報告

**レビュー日:** 2026-02-27
**レビュアー:** コードレビューエージェント

---

## サマリー

- **HTML**: ⚠️ — 全体的に高品質だが、タブパネルの `aria-labelledby` 参照先ID不一致・`data-panel` 属性欠落・重複 `reveal--delay-4` など複数の軽微な不整合あり
- **CSS**: ⚠️ — モバイルファースト・アクセシビリティ・アニメーション定義はすべて良好。フォームクラス名が HTML と不一致（`p-contact__input` vs `.form-input`）
- **JS**: ⚠️ — 安全性・構造ともに良好。タブ機能の `data-panel` セレクターが HTML の `data-category` と不一致で動作しない
- **PHP**: ✅ — セキュリティ対策が充実。`declare(strict_types=1)`・flock・htmlspecialchars・レート制限・Honeypotすべて実装済み。軽微な改善余地のみ

---

## 問題点一覧

| # | ファイル | 深刻度 | 場所（行数）| 問題内容 | 修正案 |
|---|---------|--------|-------------|----------|--------|
| 1 | HTML | 🔴 CRITICAL | 行 320–321 | タブの `aria-controls="tab-panel-coffee/sweets"` に対応するパネルの `id` は `tab-panel-coffee/sweets` だが、`aria-labelledby="tab-coffee/tab-sweets"` が指す ID `tab-coffee` / `tab-sweets` が HTML に存在しない | タブ `<button>` に `id="tab-coffee"` / `id="tab-sweets"` を追加するか、`aria-labelledby` をボタンの既存属性に合わせて削除または修正する |
| 2 | JS | 🔴 CRITICAL | 行 162 | `initMenuTabs` がパネルを `.p-menu__panel[data-panel="${targetKey}"]` で検索しているが、HTML のパネル要素にはクラス `p-menu__grid` が付いており `p-menu__panel` クラスが存在しない。また属性が `data-panel` ではなく `data-category` | HTML のパネルに `class="p-menu__panel"` と `data-panel="coffee/sweets"` を追加するか、JS のセレクターを `[id="tab-panel-${targetKey}"]` に変更する |
| 3 | HTML | 🔴 CRITICAL | 行 376 | スイーツパネルに `class="u-hidden"` が付いているが、JS は `panel.hidden = true/false` で制御している。`u-hidden` は `display: none !important` のため JS による `hidden` 属性操作が競合し、パネルの表示制御が壊れる恐れがある | スイーツパネルの初期非表示を `u-hidden` ではなく `hidden` 属性のみで実装する（`<div id="tab-panel-sweets" ... hidden>`）|
| 4 | CSS | 🔴 CRITICAL | 行 1644–1707 | CSS に `.form-group` / `.form-label` / `.form-input` / `.form-textarea` / `.form-error` クラスが定義されているが、HTML フォームのクラスは `p-contact__field` / `p-contact__label` / `p-contact__input` / `p-contact__textarea` / `p-contact__field-error` | CSS クラス名を HTML に合わせて修正するか、HTML クラス名を CSS に合わせて統一する |
| 5 | PHP | 🟡 WARNING | 行 130–131 | `MAIL_SKIPPED` 時に成功レスポンスを返さず処理が続行し、最終行 141 で `sendResponse(true, ...)` が呼ばれるが、ローカル環境では成功ログのステータスが `MAIL_SKIPPED` になっている。ログのステータス名が CLAUDE.md 規定の `SUCCESS` と異なる | ローカルスキップ後にも `writeLog('SUCCESS', ...)` を呼ぶか、`MAIL_SKIPPED` を仕様として CLAUDE.md に追加する |
| 6 | PHP | 🟡 WARNING | 行 103 | `writeLog('RATE_LIMIT', ...)` のステータスが CLAUDE.md 規定の `BLOCKED` と異なる | ステータスを `'BLOCKED'` に統一する |
| 7 | PHP | 🟡 WARNING | 行 112 | `writeLog('VALIDATION_ERROR', ...)` のステータスが CLAUDE.md 規定の `ERROR` と異なる | ステータスを `'ERROR'` に統一する |
| 8 | HTML | 🟡 WARNING | 行 760 | `<input type="hidden" name="csrf_token" value="">` の value が空。PHP 側でも CSRF トークン検証は未実装（コメントに「将来的」とある） | PHP の `session_start()` を利用してトークンを生成・埋め込む。または、コメントを実装済みと誤解させないよう明示的に「未実装」と記載する |
| 9 | HTML | 🟡 WARNING | 行 465–468 | `p-gallery__item` の `reveal--delay-4` が2つ重複している（行 460–464 と行 465–468）。意図的でなければ後者は `reveal--delay-5` にすべき | 6番目のギャラリーアイテムを `reveal--delay-5` に変更する |
| 10 | CSS | 🟡 WARNING | 行 400–404 | `.c-card-menu__image` クラスが定義されているが、HTML のメニューカード画像は `c-card-menu__image-wrapper` 内の `<img>` であり直接クラスなし。`aspect-ratio: 4/3; object-fit: cover` などのスタイルが適用されない | HTML の `<img>` に `class="c-card-menu__image"` を追加するか、CSS セレクターを `.c-card-menu__image-wrapper img` に変更する |
| 11 | CSS | 🟡 WARNING | 行 454–461 | `.c-card-staff__avatar` クラスが定義されているが、HTML のスタッフカード画像には `c-card-staff__image-wrapper` 内の `<img>` であり `c-card-staff__avatar` クラスなし。円形スタイルが適用されない | HTML の `<img>` に `class="c-card-staff__avatar"` を追加するか、CSS セレクターを `.c-card-staff__image-wrapper img` に変更する |
| 12 | HTML | 🟡 WARNING | 行 543 | `<p class="p-faq__lead-title" aria-hidden="true">よくあるご質問</p>` はデスクトップ表示時にのみ表示される左カラムの見出し。ただし aria-hidden を付与しているため、スクリーンリーダーがこの見出しを読み上げない。h2 の `faq-title` と重複するため意図的と思われるが、`aria-hidden="true"` ならば `role` / `aria-level` も不要かを確認 | 現状のまま（`aria-hidden="true"` で視覚専用）で問題なし。コメントで意図を明示すると良い |
| 13 | PHP | 🟡 WARNING | 行 322–324 | `htmlspecialchars` した値（HTML エンティティ含む）をそのままメール本文に使用しようとしているが、`sendMail` 関数内で `htmlspecialchars_decode` して元の文字列に戻している（行 393–395）。二重変換は冗長で、デコード忘れ時に `&amp;` がメール本文に混入するリスクがある | `validateInput` では HTML エスケープせずプレーンテキストを返し、HTML への出力時のみエスケープする設計に変更するか、現状の二重変換を維持するならコメントで明示する |
| 14 | JS | 🟡 WARNING | 行 19 | `initNavDrawer` 内でハンバーガーボタンを `document.querySelector('.c-hamburger')` で取得しているが、HTML には `#hamburger-btn` という ID がある。また `closeBtn` は `.c-hamburger--close` で取得しており、これも `#drawer-close-btn` がある。ID 指定にしたほうが確実 | `document.getElementById('hamburger-btn')` / `document.getElementById('drawer-close-btn')` を使用する |
| 15 | HTML | 🟢 INFO | 行 736–744 | Google マップ `<iframe>` に `class` がなく、CSS に `.p-store-info__map-frame` クラスが定義されているが `height: 240px` / `border-radius` が適用されない | `<iframe>` に `class="p-store-info__map-frame"` を追加する |
| 16 | CSS | 🟢 INFO | 行 284–293 | デスクトップ（1280px）で `.c-section-title` の `font-size` が `var(--fs-4xl)` のまま変化なし。意図的であればよいが確認が必要 | 必要に応じてデスクトップ用の大きいフォントサイズ変数を使用する |
| 17 | PHP | 🟢 INFO | 行 411–414 | `From:` ヘッダーに `mb_encode_mimeheader` が適用されていない。ローカライズされたサイト名を From に含める場合、マルチバイト文字が文字化けする可能性がある | `From: =?UTF-8?B?...?= <noreply@...>` 形式にエンコードするか、ASCII のみの From アドレスを使用する |
| 18 | JS | 🟢 INFO | 行 95 | `history.pushState(null, '', hash)` の第2引数 `title` に `''`（空文字）を渡している。現行仕様では無視されるが、将来の互換性のため `document.title` を渡すことが推奨される | `history.pushState(null, document.title, hash)` に変更する |

---

## ファイル別詳細

### HTML（05_seo.html）

#### 基本構造
- **DOCTYPE / lang / charset**: `<!DOCTYPE html>` / `lang="ja"` / `<meta charset="UTF-8">` — すべて OK
- **viewport**: `<meta name="viewport" content="width=device-width, initial-scale=1">` — OK
- **robots / canonical**: OK。canonical は `https://thecornercafe.jp/` に統一されている
- **h1**: 1つのみ（行 265: `ここにくると、ほっとする。`）— OK
- **見出し階層**: h1(hero) → h2(各セクション) → h3(コンセプトポイント・メニューカード名・スタッフ名) の順で正しい

#### img alt / width / height
- 全 `<img>` に alt・width・height 属性あり — OK
- ヒーロー画像に `loading="eager" fetchpriority="high"` — OK
- フォールド以下の画像に `loading="lazy"` — OK

#### フォーム
- `action="php/form_handler.php"` / `method="POST"` / `novalidate` — OK
- 必須フィールドに `required` / `aria-required="true"` / `type` 属性（text / email / textarea）— OK
- Honeypot: `name="website"` / `tabindex="-1"` / `autocomplete="off"` — OK
- **CSRF トークン（行 760）**: `value=""` が空。PHP 側でトークン生成・埋め込みが未実装 — WARNING

#### aria 属性
- `aria-expanded="false"` の初期値: ハンバーガーボタン（行 220）・アコーディオントリガー（行 549 等）ともに文字列 `"false"` で正しい
- **`aria-labelledby` 参照先 ID 不一致（行 325–376）**: パネルの `aria-labelledby="tab-coffee"` / `"tab-sweets"` が指す ID がドキュメント内に存在しない — CRITICAL
- `role="tablist"` / `role="tab"` / `role="tabpanel"` の使用は適切

#### data 属性の一貫性
- タブボタン: `data-tab="coffee/sweets"` — OK
- タブパネル: `data-category="coffee/sweets"` — 属性名が `data-tab` と異なり、JS の `data-panel` セレクターとも不一致 — CRITICAL

#### 外部リンク
- 全外部リンクに `target="_blank" rel="noopener noreferrer"` — OK

#### リソース読み込み順序
- CSS は `<head>` 内、JS は `<body>` 末尾で `defer` 属性付き — OK
- Google Fonts の preconnect / preload / stylesheet の順序 — OK

#### JSON-LD
- `CafeOrRestaurant` / `FAQPage` / `WebSite` の3ブロック — 構文エラーなし
- `FAQPage` の内容が実際の HTML FAQ セクションと対応している — OK

---

### CSS（04_styles.css）

#### CSS カスタムプロパティ
- `:root` に color / font / spacing / border-radius / shadow 全変数が定義されている — OK
- 使用されているすべての CSS 変数（`--color-main`、`--sp-*`、`--radius-*` 等）が `:root` に定義済み — OK

#### モバイルファースト
- 全メディアクエリが `min-width` のみ使用、`max-width` の記述なし — OK
- ブレークポイントは 768px / 1280px（375px の専用クエリなし。375px 未満のデバイスはデフォルトスタイルで対応） — 問題なし

#### reveal / is-visible アニメーション
- `.reveal` に `opacity: 0; transform: translateY(24px); transition: ...` — OK
- `.reveal.is-visible` に `opacity: 1; transform: translateY(0)` — OK
- `.reveal--left` / `.reveal--right` バリアントも定義 — OK
- `@media (prefers-reduced-motion: reduce)` 内で `.reveal { opacity: 1; transform: none; }` — OK

#### FLOCSS 命名規則
- Foundation（要素セレクター）/ Layout（`l-container`）/ Component（`c-btn`、`c-card-*`、`c-accordion` 等）/ Project（`p-hero`、`p-menu` 等）/ Utility（`u-hidden`、`u-visually-hidden`）— 概ね遵守
- Modifier は `c-btn--primary`、`c-section-label--light` 等ダブルハイフン — OK
- 状態は `is-active`、`is-open`、`is-error`、`is-visible` — OK

#### u-hidden
- `.u-hidden { display: none !important; }` — OK（行 179–181）

#### prefers-reduced-motion
- `@media (prefers-reduced-motion: reduce)` 定義あり（行 231–243）— OK

#### :focus-visible
- `:focus-visible { outline: 3px solid var(--color-main); outline-offset: 2px; }` — OK（行 143–147）

#### Google Fonts @import
- `@import url('...')` がファイル先頭（1行目）— OK

#### クラス名不一致（HTML vs CSS）
- **フォーム関連**: CSS は `.form-group` / `.form-label` / `.form-input` / `.form-textarea` / `.form-error` を定義しているが、HTML は `p-contact__field` / `p-contact__label` / `p-contact__input` / `p-contact__textarea` / `p-contact__field-error` を使用 — CRITICAL
- **メニューカード画像**: CSS の `.c-card-menu__image` が HTML 画像要素に付与されていない — WARNING
- **スタッフカード画像**: CSS の `.c-card-staff__avatar` が HTML 画像要素に付与されていない — WARNING
- **Google マップ iframe**: CSS の `.p-store-info__map-frame` が HTML iframe に付与されていない — INFO
- **タブパネル**: CSS に `.p-menu__panel` クラスの定義（行 1145–1151）があるが、HTML パネルのクラスは `p-menu__grid` — WARNING（JS の問題とも連動）

---

### JavaScript（04_script.js）

#### 基本構造
- `'use strict';` — OK（行 1）
- `DOMContentLoaded` でラップ — OK（行 3）
- null チェック: 各関数の冒頭で `if (!element) return;` や `?.` オプショナルチェーン使用 — OK

#### Honeypot チェック
- `if (honeypot && honeypot.value.trim() !== '')` でキャンセル — OK（行 297–300）
- サイレントキャンセル（ユーザーには何も通知しない）— OK

#### フォーム二重送信防止
- 送信中に `submitBtn.disabled = true; submitBtn.textContent = '送信中...'` — OK（行 307–310）
- 失敗またはネットワークエラー時に `disabled = false` で復元 — OK

#### fetch エラーハンドリング
- JSON パースエラー: 内側の try-catch で `result = { success: false, message: '...' }` にフォールバック — OK（行 325–329）
- ネットワークエラー: 外側の catch ブロックで処理 — OK（行 352–362）

#### IntersectionObserver の unobserve
- `observer.unobserve(entry.target)` — OK（行 119）

#### aria-expanded の文字列
- `setAttribute('aria-expanded', 'true')` / `'false'` と文字列で設定 — OK（行 32, 41, 148, 149, 197, 201）

#### history.pushState
- スムーズスクロール時に `history.pushState(null, '', hash)` — OK（行 95）
- 第2引数が `''`（空文字）— INFO（`document.title` 推奨）

#### タブ機能の不具合（CRITICAL）
- `initMenuTabs` が `panels = document.querySelectorAll('.p-menu__panel')` を取得（行 137）
- HTML にはこのクラスが存在しないため `panels.length` は 0 となり `if (!tabs.length || !panels.length) return;`（行 139）で即時リターン
- 加えて、対応パネルの検索が `[data-panel="${targetKey}"]`（行 162）だが、HTML は `data-category` 属性を使用
- **結果: タブ切り替えが完全に動作しない**

#### ヘッダーハンバーガー取得（WARNING）
- `querySelector('.c-hamburger')` はヘッダーのハンバーガーボタンを取得するが、ドロワー内の閉じるボタン `.c-hamburger--close` より前にマッチする前提。現状 HTML の順序（行 220 がヘッダー、行 236 がドロワー）では意図どおりだが、堅牢性のため ID 指定を推奨

---

### PHP（04_form_handler.php）

#### declare(strict_types=1)
- 行 2 に宣言あり — OK

#### display_errors オフ
- `ini_set('display_errors', '0')` — OK（行 18）
- `ini_set('log_errors', '1')` でサーバーログには記録 — OK

#### レート制限の flock
- `flock($fp, LOCK_EX)` / `flock($fp, LOCK_UN)` — OK（行 229, 263）

#### htmlspecialchars(ENT_QUOTES | ENT_HTML5, 'UTF-8')
- `htmlspecialchars($rawName, ENT_QUOTES | ENT_HTML5, 'UTF-8')` 等 — OK（行 322–324）
- ただし `sendMail` 内で `htmlspecialchars_decode` して戻している（行 393–395）— WARNING（二重変換は冗長）

#### ヘッダーインジェクション対策
- `str_replace(["\r", "\n"], '', $rawName)` / `$rawEmail` で改行文字除去 — OK（行 291, 308）
- Reply-To に使用するメールアドレスも改行除去済み — OK

#### ログパス
- `LOG_DIR = __DIR__ . '/../logs/'` — PHP ファイルは `php/form_handler.php` に置かれる想定のため、`../logs/` は `output/{案件名}/logs/` を指す — OK
- `CLAUDE.md` で定めた `logs/form_log.txt` のパス構成と一致 — OK

#### ローカル環境でのメール送信スキップ
- `$isLocalhost` 判定で `localhost` / `127.0.0.1` を検出してスキップ — OK（行 123–131）

#### Content-Type ヘッダー
- `header('Content-Type: application/json; charset=UTF-8')` — OK（行 42）

#### POST 以外への 405 返却
- `if ($_SERVER['REQUEST_METHOD'] !== 'POST')` で `405` を返却 — OK（行 70–73）

#### Honeypot 時の成功偽装
- Honeypot が設定されているとき `sendResponse(true, 'お問い合わせを受け付けました...')` を返す — OK（行 91）

#### ログステータス名の乖離（WARNING）
- CLAUDE.md 規定: `SUCCESS` / `BLOCKED` / `ERROR` / `SPAM`
- PHP 実装: `SUCCESS` / `HONEYPOT` / `RATE_LIMIT` / `VALIDATION_ERROR` / `MAIL_ERROR` / `MAIL_SKIPPED`
- `BLOCKED` に対応するのが `RATE_LIMIT` / `HONEYPOT`、`ERROR` に対応するのが `VALIDATION_ERROR` — 仕様書と乖離あり

---

## Phase 7 向け修正指示

Phase 7（最終アセンブル）で適用すべき修正をプライオリティ順にリストします。

### 必須修正（CRITICAL）

1. **タブパネルのクラス名・data属性を統一する** (ファイル: HTML + JS)
   - HTML の `<div id="tab-panel-coffee" class="p-menu__grid" ...>` を `class="p-menu__panel p-menu__grid"` に変更し、`data-category="coffee"` を `data-panel="coffee"` に変更する。スイーツパネルも同様。
   - HTML の `<div id="tab-panel-sweets" class="p-menu__grid u-hidden" ...>` の `u-hidden` を削除し、`hidden` 属性を追加する。

2. **aria-labelledby 参照先 ID を追加する** (ファイル: HTML, 行 320–321)
   - コーヒータブボタンに `id="tab-coffee"` を追加する。
   - スイーツタブボタンに `id="tab-sweets"` を追加する。

3. **フォームのクラス名を CSS に合わせて統一する** (ファイル: HTML, 行 768–818)
   - CSS に `.p-contact__field` / `.p-contact__label` / `.p-contact__input` / `.p-contact__textarea` / `.p-contact__field-error` が定義されていないため、CSS に以下のエイリアスを追加するか、HTML クラス名を `.form-group` / `.form-label` / `.form-input` / `.form-textarea` / `.form-error` に揃える。
   - **推奨**: CSS の `.form-*` クラスを `.p-contact__*` にリネームして HTML と統一する。

### 推奨修正（WARNING）

4. **メニューカード・スタッフカード画像に CSS クラスを追加する** (ファイル: HTML)
   - 各 `<article class="c-card-menu">` 内の `<img>` に `class="c-card-menu__image"` を追加する（行 328, 340, 352, 364, 378, 391, 403, 415）。
   - 各 `<article class="c-card-staff">` 内の `<img>` に `class="c-card-staff__avatar"` を追加する（行 658, 669, 680）。

5. **Google マップ iframe にクラスを追加する** (ファイル: HTML, 行 735)
   - `<iframe ... class="p-store-info__map-frame">` を追加する。

6. **ギャラリーの重複 delay クラスを修正する** (ファイル: HTML, 行 465)
   - 6番目のギャラリーアイテムを `class="p-gallery__item reveal reveal--delay-5"` に変更する。

7. **PHP ログのステータス名を CLAUDE.md 仕様に合わせる** (ファイル: PHP)
   - `'RATE_LIMIT'` → `'BLOCKED'` (行 103)
   - `'VALIDATION_ERROR'` → `'ERROR'` (行 112)
   - `'HONEYPOT'` → `'BLOCKED'` または `'SPAM'` (行 90)

8. **p-contact__success / p-contact__error の CSS 定義を確認する** (ファイル: CSS)
   - HTML に `id="form-success"` / `id="form-error"` があり CSS に `.p-contact__success` / `.p-contact__error` クラスが定義されているが、JS は `hidden` 属性で表示制御している。CSS の `display` 定義との競合がないか確認する。

### 任意修正（INFO）

9. **initNavDrawer のセレクターを ID 指定に変更する** (ファイル: JS, 行 19–22)
   - `document.querySelector('.c-hamburger')` → `document.getElementById('hamburger-btn')`
   - `document.querySelector('.c-hamburger--close')` → `document.getElementById('drawer-close-btn')`

10. **history.pushState の第2引数を document.title にする** (ファイル: JS, 行 95)
    - `history.pushState(null, '', hash)` → `history.pushState(null, document.title, hash)`

11. **PHP の htmlspecialchars 二重変換を整理する** (ファイル: PHP, 行 322–324 および 393–395)
    - バリデーション関数ではプレーンテキストを返し、メール本文にはサニタイズ不要。HTML 出力が発生する箇所のみエスケープする設計に変更することを推奨する。
