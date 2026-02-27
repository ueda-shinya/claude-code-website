# コードレビュー結果

## サマリー
- 🔴 CRITICAL: 10件
- 🟡 WARNING: 7件
- 🟢 INFO: 12件

---

## 1. HTML・CSS・JS 整合性

### 🔴 CRITICAL

**1-1. `js-privacy-open` クラスが HTML ボタンに付与されていない**
JS の `document.querySelector('.js-privacy-open')` はクラスセレクタで検索しているが、フッターのボタンには `id="js-privacy-open"` のみで `class="js-privacy-open"` が付与されていない。`openBtn` が `null` になり、プライバシーポリシーモーダルが一切開かない。

**1-2. フォームの `inquiry_type` セレクト値と PHP の `$allowed_types` が不一致**
HTML: `<option value="rental">貸切・団体利用について</option>`
PHP: `$allowed_types = ['visit', 'private', 'gift', 'other']`
`rental` が PHP の許可リストにないため、「貸切・団体利用について」を選択して送信するとサーバーサイドでバリデーションエラーとなり送信不可。

**1-3. `l-footer__logo` クラス未定義**
HTML の `<p class="l-footer__logo">` に対する CSS セレクタが存在しない。フッターのロゴに Playfair Display フォントが適用されない。

**1-4. `l-footer__tagline` クラス未定義**
HTML の `<p class="l-footer__tagline">` に対応する CSS セレクタが存在しない。

**1-5. `l-footer__sns-link` クラス未定義**
HTML の `<a class="l-footer__sns-link">` に対応する CSS セレクタが存在しない（CSS には `.l-footer__sns a` のみ）。

**1-6. `p-contact__heading` クラス未定義**
HTML の `<h2 class="p-contact__heading">` に対応するクラスが CSS にない。CSS は `.p-contact__header h2` と要素セレクタで記述されており、FLOCSS 命名規則との不整合。

**1-7. `p-contact__lead` クラス未定義**
HTML の `<p class="p-contact__lead">` に対応するクラスが CSS にない。CSS は `.p-contact__header p` と要素セレクタで記述。

**1-8. `p-staff__info` クラス未定義**
HTML の `<div class="p-staff__info">` に対応する CSS セレクタが存在しない。

**1-9. `c-form__privacy-check` クラスが `<label>` に誤適用**
HTML の `<label class="c-form__privacy-check">` は CSS で `width: 20px; height: 20px` のスタイルが当たるが、これは `input[type="checkbox"]` 向けのサイズ定義。`<label>` 要素に適用されるため、ラベル全体が縮小する。

**1-10. プライバシー同意の表示制御が `hidden` 属性と `style.display` の混用**
HTML では `hidden` 属性を使用しているが、JS では `style.display = 'block'` で表示を試みている。モーダルでは `removeAttribute('hidden')` を使用しており不統一。`hidden` 属性が優先され、JS による表示切替が正常動作しない可能性がある。

### 🟡 WARNING

- `u-sr-only` と `u-visually-hidden` の重複定義（`u-sr-only` は HTML で未使用）
- stats 要素の「毎日」「200kg以上」に `js-stats-counter` が付与されていない（仕様確認が必要）
- `p-menu__panel` の `position: absolute`→`relative` 切り替えによる高さジャンプ（CLS発生の可能性）
- フォームの `aria-describedby` が参照する error 要素 ID の整合性要確認
- `<link rel="preload" as="style">` の冗長な設定（preload した後に同じ URL を stylesheet として再読み込み）
- PHP レート制限のファイル書き込みに排他制御（flock）がない
- `og-image.jpg` が HTML 内で `<img>` としては参照されていない（OGP専用は正常だが generate_images.py には含める必要あり）

### 🟢 INFO

- FLOCSS レイヤー構造は概ね正しく実装されている
- `is-` プレフィックスの状態クラスは統一されている
- アコーディオン・タブ・ハンバーガーの ARIA 属性は JS で正しく更新されている
- モーダルの role/aria 属性は適切
- CSS アニメーションは `transform` と `opacity` のみ使用（layout プロパティなし）✅
- モバイルファースト（min-width のみ）が守られている ✅
- PHP: XSS サニタイズ (`htmlspecialchars`) 全フィールドに適用 ✅
- PHP: ヘッダーインジェクション対策 (`str_replace(["\r","\n"]...)`) 実施済み ✅
- PHP: POST メソッドチェックあり ✅
- PHP: Honeypot チェックあり ✅
- JS: `innerHTML` 不使用、`textContent` のみ使用 ✅
- skip ナビゲーションあり ✅

---

## 2. セキュリティ

### 🟢 INFO
- PHP XSS サニタイズ: 全入力フィールドに `htmlspecialchars()` 適用 ✅
- PHP ヘッダーインジェクション防止: `str_replace(["\r","\n"],'',$email)` ✅
- PHP レート制限: JSON ファイルによる IP 別タイムスタンプ管理 ✅
- PHP メソッドチェック: POST のみ許可 ✅
- PHP Honeypot: `$_POST['website']` チェック ✅
- JS innerHTML 禁止: textContent のみ使用 ✅
- JS 二重送信防止: `isSubmitting` フラグ実装 ✅

---

## 3. アクセシビリティ

### 🟡 WARNING
- gallery 画像の alt が空文字（装飾目的ならば可だが、コンテンツ画像なら説明が必要）

### 🟢 INFO
- 全フォーム入力に `<label>` または `aria-label` あり ✅
- ランドマーク（header/nav/main/footer）存在 ✅
- `aria-expanded`/`aria-selected` を JS で動的更新 ✅
- skip ナビ `#main` リンクあり ✅
- `<nav aria-label="メインナビゲーション">` あり ✅

---

## 4. 画像・アセット整合性（最重要）

### HTML内の画像リスト（22件）
- assets/images/hero.jpg
- assets/images/menu-signature.jpg
- assets/images/menu-deep.jpg
- assets/images/menu-single.jpg
- assets/images/menu-latte.jpg
- assets/images/menu-float.jpg
- assets/images/menu-au-lait.jpg
- assets/images/sweets-gateau.jpg
- assets/images/sweets-lemon.jpg
- assets/images/sweets-pound.jpg
- assets/images/sweets-basque.jpg
- assets/images/sweets-scone.jpg
- assets/images/sweets-tart.jpg
- assets/images/gallery-1.jpg 〜 gallery-6.jpg（6件）
- assets/images/staff-kimura.jpg
- assets/images/staff-hayashi.jpg
- assets/images/staff-watanabe.jpg

### generate_images.py の生成リスト（20件）
- hero.jpg
- concept.jpg
- coffee-01.jpg 〜 coffee-04.jpg（4件）
- sweets-01.jpg 〜 sweets-04.jpg（4件）
- gallery-01.jpg 〜 gallery-06.jpg（6件、ゼロパディングあり）
- staff-01.jpg 〜 staff-03.jpg（3件、番号形式）
- og-image.jpg

### 照合結果

#### 🔴 CRITICAL: HTMLにあるがgenerate_images.pyにない（21件）
- menu-signature.jpg, menu-deep.jpg, menu-single.jpg, menu-latte.jpg, menu-float.jpg, menu-au-lait.jpg
- sweets-gateau.jpg, sweets-lemon.jpg, sweets-pound.jpg, sweets-basque.jpg, sweets-scone.jpg, sweets-tart.jpg
- gallery-1.jpg 〜 gallery-6.jpg（ゼロパディングなし版 — generate_images.py は gallery-01.jpg 形式）
- staff-kimura.jpg, staff-hayashi.jpg, staff-watanabe.jpg（人名形式 — generate_images.py は staff-01〜03.jpg）

#### 🟡 WARNING: generate_images.pyにあるがHTMLから未参照（18件）
- concept.jpg
- coffee-01.jpg 〜 coffee-04.jpg（4件）
- sweets-01.jpg 〜 sweets-04.jpg（4件）
- gallery-01.jpg 〜 gallery-06.jpg（ゼロパディング版 6件）
- staff-01.jpg 〜 staff-03.jpg（3件）

> **対応方針（Phase 9）:** generate_images.py の IMAGE_LIST を HTML の参照ファイル名に完全一致させる。og-image.jpg のみ OGP 専用として保持する。

---

## 5. パフォーマンス

### 🟢 INFO
- ヒーロー画像: `loading="lazy"` なし ✅（正しい）
- フォールド以下の画像: `loading="lazy"` あり ✅
- CSS アニメーション: `transform`/`opacity` のみ ✅
- 外部 JS/CSS ライブラリなし ✅（Google Fonts のみ）

---

## 6. モバイルファーストCSS

### 🟢 INFO
- `max-width` メディアクエリ: 不使用 ✅
- ブレークポイント: 768px / 1280px の 2段階（375px は base として扱い） ✅
- タップターゲット 44px 以上: ボタン類に `min-height: 44px` 適用 ✅

---

## 修正推奨事項（優先順）

1. 🔴 **generate_images.py の IMAGE_LIST を HTML の参照ファイル名に完全一致させる**（Phase 9 ステップ2 の必須対応）
2. 🔴 **フッターボタンを `class="js-privacy-open"` に修正**（または JS を `getElementById` に変更）
3. 🔴 **PHP の `$allowed_types` に `'rental'` を追加、`$inquiry_labels` にも `'rental' => '貸切・団体利用について'` を追加**
4. 🔴 **CSS に不足クラスを追加**: `l-footer__logo`, `l-footer__tagline`, `l-footer__sns-link`, `p-contact__heading`, `p-contact__lead`, `p-staff__info`
5. 🔴 **プライバシー同意の表示制御を統一**: `hidden` 属性を使うか `display:none` に統一し、JS の表示切替と整合させる
6. 🔴 **`c-form__privacy-check` をチェックボックス入力要素に適用**（label でなく input に付与）
7. 🟡 **gallery 画像の alt に説明テキストを追加**
8. 🟡 **generate_images.py の孤立エントリ（concept.jpg, coffee-*, sweets-0x, gallery-0x, staff-0x）を削除または更新**
