# QAレビュー結果

## サマリー
- HIGH: 2件
- MEDIUM: 4件
- LOW: 3件
- PASS: 42件

---

## 1. 仕様書との照合

### HIGH（仕様未達）
- なし

### MEDIUM（部分的な問題）
- **JSON-LD の openingHoursSpecification に火曜日（定休日）の除外記述がない**: 定休日「毎週火曜日」が JSON-LD に反映されていない。火曜日が月〜金のグループに含まれており、実態（火曜定休）と矛盾する。ローカル SEO の精度に影響する。

### LOW（軽微な差異）
- **FAQ Q6「JR○○駅」のプレースホルダーが残存**: コピーに「最寄りのJR○○駅からは徒歩8分です」という未確定情報が記載されており HTML にそのまま反映。実際の駅名への差し替えが必要。
- **og:title と title タグの内容が異なる**: OGP タイトル「THE CORNER CAFE | 自家焙煎コーヒーと手作りスイーツ｜三軒茶屋」と `<title>` タグ「THE CORNER CAFE | 自家焙煎コーヒーと手作りスイーツ」で「｜三軒茶屋」の有無が異なる。統一を推奨。

### PASS
- 仕様書記載の全10セクションが実装されていることを確認（ヒーロー〜お問い合わせ）
- ハンバーガーメニュー（js-hamburger）実装済み
- スムーズスクロール（js-scroll-to クラス）実装済み
- FAQアコーディオン（js-accordion）実装済み
- メニュータブ切り替え（js-tab / role="tablist"）実装済み
- フォームバリデーション用エラー要素実装済み
- Honeypot フィールド実装済み
- メインカラー（#6B4C35）、フォント（Playfair Display + Noto Sans JP）が仕様書通り
- フォーム送信先 php/form_handler.php（仕様書と一致）

---

## 2. コピーとの照合

### HIGH（コピーが欠落・変更されている）
- **禁止ワード「最高」がコーヒーフロートの説明文に使用されている**: コーヒーフロートの説明「甘さと苦さが溶け合う瞬間が最高です」に禁止ワード「最高」が含まれている。コピーファイルの修正が必要。

### MEDIUM（部分的な問題）
- **ヒーローセクションに eyebrow コピー「世田谷・三軒茶屋」が追加されている**: `p-hero__eyebrow` の「世田谷・三軒茶屋」はコピーファイル未記載。HTMLデザイナーが独自に追加したと考えられ、コピーライターの RACI を逸脱しているため確認・承認が必要。

### PASS
- ヒーロー（メインヘッドライン・サブヘッドライン・ボディコピー・CTA2種・画像alt）全て正確に反映
- セクション2 見出し・リードコピー・こだわり1〜3（見出し・本文）全て正確に反映
- セクション3 実績バナー 数字4点・ラベル・キャプション全て正確に反映
- セクション4 見出し・リードコピー・コーヒー6商品・スイーツ6商品（名前・価格・説明文）全て正確に反映、補足コピーも正確に反映
- セクション5 見出し・リードコピー・ギャラリー画像alt（6枚）・Instagram誘導コピー・CTAボタン正確に反映
- セクション6 見出し・リードコピー・お客様の声4件（名前・年齢・本文）全て正確に反映
- セクション7 見出し・リードコピー・スタッフ3名（名前・役職・プロフィール・ひとこと）全て正確に反映
- セクション8 見出し・FAQ Q1〜Q8（質問・回答）全て正確に反映
- セクション9 見出し・店舗情報テーブル全項目・アクセス補足コピー・Googleマップボタン・駐車場情報 全て正確に反映
- セクション10 見出し・リードコピー・成功メッセージ・エラーメッセージ 全て正確に反映
- フォームラベル・プレースホルダー全て正確に反映
- フッター（ロゴ・キャッチ・住所・TEL・営業時間・定休日・ナビ全項目・SNS情報・コピーライト・プライバシーポリシー）全て正確に反映
- プライバシーポリシー本文・最終更新日 正確に反映

---

## 3. 納品物動作確認

### HIGH（動作不可能な問題）
- なし

### MEDIUM（動作に影響する可能性）
- **Google Fonts の preload が onload ハンドラなしで機能しない可能性**: `<link rel="preload" as="style">` しているが、スタイルシートの preload は `onload` ハンドラなしでは自動適用されない。通常のロードは問題なく機能するが、preload の効果が得られていない可能性あり。
- **Instagram アカウント URL の不一致**: JSON-LD は `thecornercafe_sangenjaya`、HTML 内リンクは `thecornercafe` と異なる。正式アカウントを確認の上、全箇所を統一すること。

### LOW（軽微な問題）
- **Twitter Card の twitter:site が @thecornercafe_sangenjaya**: Instagram リンクの `@thecornercafe` と異なる。正式アカウント名を統一すること。

### PASS

#### アセットパス
- `<link rel="stylesheet" href="assets/css/styles.css">` — 正しいパス ✅
- `<script src="assets/js/script.js" defer>` — 正しいパス ✅
- 全 `<img src>` が `assets/images/` 以下のパスを使用（22枚確認） ✅

#### フォーム
- フォームの `action="php/form_handler.php"` — 正しいパス ✅
- `method="POST"` — 正しく設定 ✅
- 全フォームフィールドに name 属性あり（name / email / tel / inquiry_type / message / privacy） ✅
- Honeypot フィールド `name="website"` — 実装済み、u-hidden / tabindex="-1" / aria-hidden="true" で隠蔽 ✅
- プライバシー同意チェックボックス `name="privacy"` — 実装済み ✅
- `id="form-success"` 要素 — 実装済み ✅
- `id="form-error"` 要素 — 実装済み ✅

#### IMAGE_MANIFEST との照合
HTML内の全 `<img src>` と IMAGE_MANIFEST を照合（22ファイル）:
- hero.jpg — HTML参照・MANIFEST記載 ✅
- menu-signature.jpg 〜 menu-au-lait.jpg（6件）— HTML参照・MANIFEST記載 ✅
- sweets-gateau.jpg 〜 sweets-tart.jpg（6件）— HTML参照・MANIFEST記載 ✅
- gallery-1.jpg 〜 gallery-6.jpg（6件）— HTML参照・MANIFEST記載 ✅
- staff-kimura.jpg, staff-hayashi.jpg, staff-watanabe.jpg — HTML参照・MANIFEST記載 ✅
- og-image.jpg — HTML内 img 参照なし（OGP メタタグのみ、OGP専用として除外OK）

**HTML参照と IMAGE_MANIFEST の差分: 完全一致 ✅**

---

## 4. ブランドボイス確認

### 問題点
- **MEDIUM — 禁止ワード「最高」の使用**: コーヒーフロートの説明文「甘さと苦さが溶け合う瞬間が最高です」に禁止ワードが含まれる。コピーファイルの修正が必要。

### PASS
- 過度な敬語・セールス臭の強い表現は全体を通じて見当たらない ✅
- 「ご近所さんに語りかける」温かいトーンが各セクションで一貫して維持されている ✅
- 「当店」「弊店」「是非」「究極」「至高」「驚くほど」「感動するほど」の禁止ワードは使用されていない ✅
- ターゲット（OL・フリーランス・主婦・大学生）に向けた適切な言葉遣い ✅

---

## 5. SEO要素確認

### PASS
- `<title>` タグあり、ターゲットキーワード含む ✅
- `<meta name="description">` あり ✅
- OGPタグ全種（og:type / og:url / og:title / og:description / og:image / og:image:width / og:image:height / og:locale / og:site_name）実装済み ✅
- Twitter Card 全要素実装済み ✅
- JSON-LD 構造化データ3種（CafeOrRestaurant / FAQPage / WebSite）全て実装済み ✅
- FAQPage に全8問の Q&A が構造化されている ✅
- h1 は1つのみ ✅
- 見出し階層（h1 → h2 → h3）が論理的に構成されている ✅
- 全 `<img>` に alt 属性あり（22枚確認） ✅
- 全画像に width / height 属性あり（CLS 防止） ✅
- フォールド以下の画像に `loading="lazy"` あり ✅
- `<link rel="canonical">` あり ✅
- `<meta name="robots" content="index, follow">` あり ✅
- スキップナビゲーション `<a href="#main">` あり ✅

### 問題点（LOW）
- **JSON-LD の openingHoursSpecification で火曜日（定休日）が除外されていない**: Monday〜Friday グループに Tuesday も含まれており実際の火曜定休と矛盾。修正を推奨。

---

## 総合評価

**納品可能か:** 修正後OK

**修正必須項目（HIGH）:**
1. 禁止ワード「最高」の除去: コーヒーフロートの説明文「甘さと苦さが溶け合う瞬間が最高です」を修正（代替案: 「甘さと苦さが溶け合うその瞬間が、たまりません。」等）

**修正推奨項目（MEDIUM）:**
1. JSON-LD openingHoursSpecification から火曜日を除外（月・水〜金グループと土日祝グループの2つに分ける）
2. Instagram アカウント URL を全箇所で統一（JSON-LD の `thecornercafe_sangenjaya` と HTML リンクの `thecornercafe` のどちらが正しいか確認し全箇所修正）
3. ヒーローセクションの `p-hero__eyebrow`「世田谷・三軒茶屋」がコピーファイル未記載のため確認・承認取得または削除
4. Google Fonts の preload 効果確認

**修正参考項目（LOW）:**
1. FAQ Q6「最寄りのJR○○駅から徒歩8分」のプレースホルダーを実際の駅名に差し替える
2. `<title>` タグと og:title の「｜三軒茶屋」の有無を統一する
3. Twitter Card の `twitter:site` を Instagram リンクと合わせて統一する
