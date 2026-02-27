# THE CORNER CAFE — QAレビュー報告

**チェック日:** 2026-02-27
**QA担当:** QAエージェント

---

## 総合判定

| カテゴリ | 判定 | 合格率 |
|---------|------|-------|
| 仕様適合性 | ⚠️ | 12/14 |
| コピー照合 | ⚠️ | 5/6 |
| アクセシビリティ | ⚠️ | 5/7 |
| セキュリティ | ⚠️ | 3/4 |
| コンテンツ完全性 | ✅ | 6/6 |
| ブランドボイス | ✅ | 3/3 |

---

## 不合格・要注意項目

| # | カテゴリ | 重要度 | チェック項目 | 結果 | 対処 |
|---|---------|--------|------------|------|-----|
| 1 | 仕様適合 | HIGH | メニュータブ JS の `data-panel` vs `p-menu__grid` セレクター不一致 | FAIL | script.js の `initMenuTabs()` は `.p-menu__panel[data-panel="…"]` を検索しているが、HTML の panels は `.p-menu__grid` クラスで `data-category` 属性を持ち、`.p-menu__panel` クラスを持たない。スイーツタブ切り替えが動作しない。 |
| 2 | 仕様適合 | HIGH | スタッフカード画像クラス不一致 | FAIL | CSS は `.c-card-staff__avatar` でスタイルを定義しているが、HTML は `<img>` に `c-card-staff__avatar` クラスがなく、`<div class="c-card-staff__image-wrapper">` の中に裸の `<img>` が入っている。アバターの円形トリミングが適用されない。 |
| 3 | 仕様適合 | MEDIUM | メニューカード画像クラス不一致 | FAIL | CSS は `.c-card-menu__image` でスタイルを定義しているが、HTML には該当クラスを持つ `<img>` がなく、`<div class="c-card-menu__image-wrapper">` 内に裸の `<img>` が入っている。 |
| 4 | コピー照合 | MEDIUM | ギャラリーセクションの Instagram 誘導テキストが未掲載 | WARN | 02_copy.md では「最新の写真や季節メニューは、Instagramでも更新しています。フォローしていただけると、うれしいです。」というテキストが指定されているが、HTML にはこのリード文が存在せず `p-gallery__lead` に別のテキストが入っている。コピー仕様との差異あり。 |
| 5 | アクセシビリティ | HIGH | `u-skip-link` のフォーカス表示スタイルが CSS に未定義 | WARN | HTML に `<a href="#main-content" class="u-skip-link">` が存在するが、CSS に `.u-skip-link` のスタイル定義がない。スキップリンクはフォーカス時に画面上に表示される必要があるが、現在は常に非表示または未スタイルになる可能性がある。 |
| 6 | アクセシビリティ | MEDIUM | フォームの既存エラー `<span>` と JS 動的エラー `<p>` の二重構造 | WARN | HTML にはすでに `<span id="name-error" class="p-contact__field-error" role="alert">` が存在するが、JS の `showFieldError()` は `field.parentElement` に新たな `<p class="form-error">` を追加する。フォームフィールドのクラス (`p-contact__input`/`p-contact__textarea`) と JS が期待するクラス (`form-input`/`form-textarea`) も一致していない（`is-error` を付与するが `form-input.is-error` のスタイルしかなく `p-contact__input.is-error` がない）。 |
| 7 | セキュリティ | MEDIUM | Honeypot フィールドが `u-hidden`（`display: none`）で隠されており、スクリーンリーダーにも aria-hidden="true" が設定されているが、一部のボット検知ツールは display:none を回避する | INFO | 仕様要件は満たしているが、`visibility: hidden; position: absolute` など代替手法の方が一部ボットに対してより効果的。軽微な推奨事項。 |
| 8 | 仕様適合 | MEDIUM | `p-header__nav-list` のリスト内の Instagram ボタンは 7番目のアイテムだが、ナビリンク数は 6 | INFO | 仕様は「ナビゲーションリンクが全6つ存在」としており、Instagram CTAボタンはリストの追加要素として含まれている。リンクとしてのカウントは6つ正常。ただしナビリストに7項目（6ナビ+1CTA）が混在し、セマンティクス的に CTA の分離が望ましい。 |

---

## チェックリスト詳細

### 1. 仕様適合性チェック（01_spec.md との照合）

| チェック項目 | 結果 | 備考 |
|-----------|------|------|
| 9セクション全て存在 (ヒーロー/コンセプト/メニュー/ギャラリー/声/FAQ/スタッフ/店舗情報/問い合わせ) | ✅ | hero, concept, menu, gallery, testimonials, faq, staff, info, contact — すべて確認済み |
| カラーシステムが CSS に正しく定義 (#6B4C35, #FAF7F2, #7B9E6B, #2C1A0E, #8B6F5C) | ✅ | `--color-main: #6B4C35`, `--color-base: #FAF7F2`, `--color-accent: #7B9E6B`, `--color-text-dark: #2C1A0E`, `--color-text-mid: #8B6F5C` すべて定義済み |
| Google Fonts が設定 (Playfair Display + Noto Sans JP) | ✅ | `@import` および `<link>` 両方で読み込まれている |
| ナビゲーションリンクが全6つ存在 (こだわり/メニュー/ギャラリー/スタッフ/店舗情報/お問い合わせ) | ✅ | PC ナビ・ドロワーナビ両方に6リンク確認済み |
| Instagram フォロー CTA がヒーローセクションに存在 | ✅ | `<a href="https://www.instagram.com/thecornercafe/" class="c-btn c-btn--primary">Instagramを見る</a>` 確認済み |
| お問い合わせフォームが 3フィールド (名前/メール/内容) + 送信ボタン | ✅ | name, email, message + 送信ボタン確認済み |
| フォームに Honeypot フィールドが存在 | ✅ | `<input type="text" name="website" tabindex="-1" autocomplete="off">` 確認済み |
| レスポンシブ対応: 375px / 768px / 1280px ブレークポイント | ✅ | CSS に `min-width: 768px` および `min-width: 1280px` のメディアクエリ確認済み（375px はモバイルベース） |
| IntersectionObserver でフェードイン実装 | ✅ | `initReveal()` で `IntersectionObserver` を使用、`.reveal` クラスに `is-visible` 付与 |
| FAQ が 8問存在 | ✅ | faq-1 〜 faq-8 の 8つのアコーディオン確認済み |
| スタッフが 3名紹介 | ✅ | 中村健太・佐藤ゆき・林まいこ の3名確認済み |
| メニューが コーヒー4種 + スイーツ4種 | ✅ | コーナーブレンド/エチオピア/カフェラテ/季節のスペシャルティ + バスクチーズケーキ/季節のタルト/スコーン/抹茶テリーヌ |
| 住所が正しく表示 (〒150-0001 東京都渋谷区神宮前2丁目14-8) | ✅ | `〒150-0001 東京都渋谷区神宮前2丁目14-8 コーナービル 1F` 確認済み |
| 営業時間が正しく表示 (火〜金 8:00〜20:00, 土日 9:00〜19:00, 月曜定休) | ✅ | 「月曜定休 / 火〜金 8:00〜20:00 / 土・日 9:00〜19:00」確認済み |

**追加検出 FAIL:**

| チェック項目 | 結果 | 備考 |
|-----------|------|------|
| メニュータブ JS の panel セレクター整合性 | ❌ | script.js: `.p-menu__panel[data-panel="…"]` を検索。HTML: `.p-menu__grid` + `data-category="coffee/sweets"` 属性。クラス名と属性名が不一致のためスイーツタブクリックで panel 表示が切り替わらない |
| スタッフカード画像クラス整合性 | ❌ | CSS: `.c-card-staff__avatar`。HTML: `<div class="c-card-staff__image-wrapper"><img src="..." alt="...">` — `__avatar` クラスが img に付与されていない |
| メニューカード画像クラス整合性 | ❌ | CSS: `.c-card-menu__image`。HTML: `<div class="c-card-menu__image-wrapper"><img ...>` — `__image` クラスが img に付与されていない |

---

### 2. コピー照合チェック（02_copy.md との照合）

| チェック項目 | 結果 | 備考 |
|-----------|------|------|
| ヒーローキャッチコピー: 「ここにくると、ほっとする。」 | ✅ | `<h1 id="hero-title">ここにくると、ほっとする。</h1>` 確認済み |
| スタッフ名 3名 (中村健太/佐藤ゆき/林まいこ) | ✅ | 3名ともテキスト・ルビ付きで確認済み |
| 証言者名 3名 (田中さやか/松本あかり/小川みほ) | ✅ | 「田中 さやか（28歳・会社員）」「松本 あかり（32歳・フリーランスデザイナー）」「小川 みほ（25歳・大学院生）」確認済み |
| コーヒーメニュー価格 (¥550/¥680/¥620/¥750〜) | ✅ | 全4品の価格が HTML に正しく掲載 |
| スイーツメニュー価格 (¥550/¥600/¥480/¥520) | ✅ | 全4品の価格が HTML に正しく掲載 |
| お問い合わせリード文の存在確認 | ⚠️ | リード文は存在するが、02_copy.md と微妙に異なる。コピー: 「ご来店前のご質問や、貸し切りのご相談など〜通常2営業日以内にご返信します。」HTML: 同テキスト確認済み — **合格** |

**追加検出 WARN:**

| チェック項目 | 結果 | 備考 |
|-----------|------|------|
| ギャラリー Instagram 誘導テキスト | ⚠️ | 02_copy.md: 「最新の写真や季節メニューは、Instagramでも更新しています。フォローしていただけると、うれしいです。」HTML p-gallery__lead: 「お客さまと一緒につくる、THE CORNER CAFEの日常です。」 — 別テキストに置き換えられている |

---

### 3. アクセシビリティ QA

| チェック項目 | 結果 | 備考 |
|-----------|------|------|
| skip ナビゲーションリンクが `<body>` 直後に存在するか | ✅ | `<a href="#main-content" class="u-skip-link">メインコンテンツへスキップ</a>` — body 開始直後に確認済み |
| `<main id="main-content">` が存在するか | ✅ | `<main id="main-content" role="main">` 確認済み |
| すべてのフォームフィールドに `<label>` が紐付いているか | ✅ | name/email/message フィールド全てに `<label for="...">` 対応確認済み。Honeypot も `<label>` 内包 |
| 全インタラクティブ要素が keyboard navigable か（理論的確認） | ✅ | ハンバーガー・アコーディオン・フォームで Escape キー対応、focus 管理実装を確認 |
| 装飾的な画像に `alt=""` または `aria-hidden="true"` が設定されているか | ✅ | SVG アイコンには `aria-hidden="true"` 設定確認済み。ヒーロー背景画像には説明的 alt テキストあり |
| `prefers-reduced-motion` の CSS が存在するか | ✅ | `@media (prefers-reduced-motion: reduce)` ブロックで全アニメーション無効化確認済み |
| フォームエラーメッセージに `role="alert"` が付与されているか | ⚠️ | HTML の静的 `<span>` には `role="alert"` あり。JS 動的生成の `<p class="form-error">` にも `role="alert"` が付与されている（script.js L238）。ただし HTML の既存 span と JS 動的生成 p が並列して存在する二重構造の問題あり |

**追加検出 FAIL:**

| チェック項目 | 結果 | 備考 |
|-----------|------|------|
| `u-skip-link` フォーカス表示 CSS 定義 | ❌ | CSS ファイルに `.u-skip-link` セレクターが存在しない。スキップリンクはフォーカス時に可視化するスタイル（例: `position:absolute; top:0; left:0; ...`）が必要だが未定義。キーボードユーザーにスキップリンクが見えない |
| フォーム CSS クラスの整合性 | ❌ | HTML フォームフィールドのクラス: `p-contact__input`, `p-contact__textarea`。CSS のエラー状態スタイル: `.form-input.is-error`, `.form-textarea.is-error` — クラス名不一致のためバリデーションエラー時の赤枠スタイルが適用されない |

---

### 4. セキュリティ QA

| チェック項目 | 結果 | 備考 |
|-----------|------|------|
| フォーム action が `php/form_handler.php` を指しているか | ✅ | `<form action="php/form_handler.php" method="POST">` 確認済み |
| Honeypot フィールドが `display: none` か `visibility: hidden` でユーザーに見えないか | ✅ | `<div class="u-hidden" aria-hidden="true">` — CSS で `.u-hidden { display: none !important; }` 適用確認済み |
| 外部リンク（Instagram 等）に `rel="noopener noreferrer"` があるか | ✅ | Instagram・Googleマップへの全外部リンクに `target="_blank" rel="noopener noreferrer"` 確認済み |
| `<meta name="robots" content="index,follow">` があるか | ✅ | `<meta name="robots" content="index,follow">` 確認済み |

**追加検出 INFO:**

| チェック項目 | 結果 | 備考 |
|-----------|------|------|
| `innerHTML` 使用禁止 | ✅ | script.js 全体で `innerHTML` は使用されておらず、`textContent` のみ使用確認済み |
| 送信ボタンの二重送信防止 | ✅ | 送信時に `submitBtn.disabled = true` 設定確認済み |

---

### 5. コンテンツ完全性チェック

| チェック項目 | 結果 | 備考 |
|-----------|------|------|
| ページタイトルが仕様通り | ✅ | `THE CORNER CAFE｜自家焙煎コーヒーと手作りスイーツの街角カフェ` — 01_spec.md §6 と一致 |
| meta description が存在し、空でないか | ✅ | 155文字以内の適切な説明文確認済み |
| canonical URL が設定されているか | ✅ | `<link rel="canonical" href="https://thecornercafe.jp/">` 確認済み |
| OGP タグ（og:title, og:description, og:image）が設定されているか | ✅ | og:title, og:description, og:image, og:type, og:url, og:locale 全て確認済み。Twitter Card も設定済み |
| JSON-LD が 2〜3 ブロック存在するか (CafeOrRestaurant + FAQPage + WebSite) | ✅ | CafeOrRestaurant, FAQPage, WebSite の3ブロック確認済み |
| フッターコピーライトが存在するか | ✅ | `© 2024 THE CORNER CAFE. All rights reserved.` 確認済み |

---

### 6. ブランドボイス QA（01_spec.md § 7 との照合）

| チェック項目 | 結果 | 備考 |
|-----------|------|------|
| 禁止表現（「今だけ！」「業界最高」「割引」等）が含まれていないか | ✅ | HTML 全文を確認。urgency 煽り・割引強調表現なし |
| 推奨表現（「ほっとする」「こだわり」「丁寧に」「毎日来たくなる」等）が使われているか | ✅ | 「ほっとする」「こだわり」「丁寧に」「また来たくなる」「毎日」等、随所に確認済み |
| 全体的なトーンが「温かく、親しみやすい」かどうか | ✅ | コピー全体が丁寧で親しみやすい日常語を使用。押しつけがましい表現なし |

---

## Phase 7 向け修正指示

Phase 7（最終アセンブル）で対応すべき事項:

### CRITICAL（リリース前に必ず修正）

1. **メニュータブ切り替えの JS バグ修正**
   - 問題: `script.js` の `initMenuTabs()` が `.p-menu__panel[data-panel="…"]` を検索しているが、HTML には `.p-menu__panel` クラスが存在せず `.p-menu__grid` に `data-category="coffee/sweets"` が付与されている
   - 修正案A（HTML 修正）: スイーツパネル `div` に `class="p-menu__grid p-menu__panel"` と `data-panel="sweets"` を追加し、コーヒーパネルも同様に修正
   - 修正案B（JS 修正）: セレクターを `.p-menu__grid[data-category]` に変更し、`data-tab` と `data-category` を照合するよう修正
   - 推奨: 修正案A（HTML 修正）でクラスと属性を統一する

2. **スタッフカード画像クラスの追加**
   - 問題: HTML のスタッフカード `<img>` に `c-card-staff__avatar` クラスがなく、円形トリミング等のスタイルが適用されない
   - 修正: 各 `<img src="assets/images/staff-*.jpg" ...>` に `class="c-card-staff__avatar"` を追加

3. **メニューカード画像クラスの追加**
   - 問題: HTML のメニューカード `<img>` に `c-card-menu__image` クラスがなく、`aspect-ratio: 4/3` 等のスタイルが適用されない
   - 修正: 各 `<img src="assets/images/placeholder-coffee/sweets.jpg" ...>` に `class="c-card-menu__image"` を追加

4. **スキップリンクの CSS 定義追加**
   - 問題: `.u-skip-link` スタイルが CSS に存在せず、キーボードユーザーがフォーカス時にリンクを視認できない
   - 修正: `styles.css` に以下を追加:
     ```css
     .u-skip-link {
       position: absolute;
       top: -100%;
       left: 0;
       padding: 8px 16px;
       background: var(--color-main);
       color: var(--color-text-white);
       font-size: var(--fs-sm);
       z-index: 9999;
       border-radius: 0 0 var(--radius-md) 0;
     }
     .u-skip-link:focus {
       top: 0;
     }
     ```

5. **フォームフィールドの CSS クラス不一致修正**
   - 問題: HTML フォームフィールドのクラスが `p-contact__input`/`p-contact__textarea` だが、CSS のエラースタイルが `.form-input.is-error`/`.form-textarea.is-error` を対象にしており、バリデーションエラー時の赤枠が表示されない
   - 修正案A（CSS 追加）: `styles.css` に `.p-contact__input.is-error, .p-contact__textarea.is-error` のスタイルを追加
   - 修正案B（HTML 修正）: フォームフィールドのクラスを `form-input`/`form-textarea` に変更

### WARNING（推奨修正）

6. **ギャラリーセクションの Instagram 誘導テキスト**
   - 02_copy.md 指定テキスト「最新の写真や季節メニューは、Instagramでも更新しています。フォローしていただけると、うれしいです。」が未掲載
   - `p-gallery__lead` の直後（`p-gallery__grid` の前）に段落として追加することを推奨

7. **フォームエラーの二重構造整理**
   - HTML の `<span id="name-error" class="p-contact__field-error" role="alert">` と JS が動的生成する `<p class="form-error">` が重複する可能性がある
   - 推奨: JS の `showFieldError()` を HTML 既存の `<span id="{field}-error">` を直接更新するよう修正するか、HTML の静的 span を削除する

8. **ナビバーの Instagram CTA ボタン位置**
   - `<ul class="p-header__nav-list">` 内の 7番目アイテムとして `c-btn` が含まれている
   - セマンティクス的に CTA は `<ul>` の外に出し、`<nav>` 直下の兄弟要素として配置することを推奨

---

## 合格判定

- [x] WARNING 項目あり → Phase 7 進行 OK（修正推奨）
- [x] CRITICAL 項目あり → Phase 7 進行前に優先修正が必要

**総評:** 仕様・コピー・SEO・ブランドの大枠は高品質に実装されている。致命的なバグはメニュータブの JS/HTML 不整合（スイーツタブが機能しない）と、スキップリンク CSS 未定義、フォームのエラースタイル未適用の3点。これらは目視・操作で即確認できる問題であり、Phase 7 での修正が必須。
