# THE CORNER CAFE — QAレビュー

**対象ファイル:** 07_seo.html / 01_spec.md / 03_copy.md
**総合:** HIGH=3 / MEDIUM=4 / LOW=3

---

## 1. 仕様書（01_spec.md）との照合 — 全項目PASS

- 全9セクション存在確認: Hero / Concept / Menu（Coffee+Sweets タブ）/ Gallery / Testimonials / Staff / FAQ / Access / Contact — OK
- メインCTA（Instagramフォロー）: `href="https://www.instagram.com/thecornercafe"` — OK
- サブCTA（アクセス確認）: `href="#access"` / テキスト「アクセスを確認する」 — OK
- フォームアクション: `action="php/form_handler.php" method="POST"` — OK
- viewport meta — OK

---

## 2. コピー（03_copy.md）との照合

### PASS 項目
- ヒーロー h1「ここにくると、ほっとする。」 — 完全一致
- 実績バナー4つの数字（5年/80%/2種/毎日焼き上げ）— 完全一致
- コーヒー4品・スイーツ4品の名前・価格 — 完全一致
- お客様の声4件の氏名・属性 — 完全一致
- スタッフ3名の名前・役職 — 完全一致
- FAQ6問の質問文 — 完全一致
- フォームラベル全フィールド — 一致
- CTAボタンテキスト全て — 一致
- フッターキャッチ「今日も、ここで。あなたの「ほっとする」時間を。」 — 完全一致
- 送信完了メッセージ — 一致

### FAIL 項目

**HIGH — FORM-01:** お名前フィールドの `maxlength="100"` に対し、コピーのエラーメッセージが「お名前は50文字以内でご入力ください。」と矛盾。50文字か100文字かに統一が必要。
→ 修正方針: `maxlength="50"` に変更し、JSのバリデーションメッセージも「50文字以内」に合わせる。

**HIGH — FORM-02:** メッセージ textarea の `maxlength="2000"` に対し、コピーのエラーメッセージが「お問い合わせ内容は1000文字以内でご入力ください。」と矛盾。
→ 修正方針: `maxlength="1000"` に変更し、JSのバリデーションも「1000文字以内」に合わせる。

**HIGH — COPY-01:** 営業時間表記が「月〜金」と省略されているが、コピー仕様は「月曜〜金曜」。
→ 修正方針: `月曜〜金曜 8:00〜20:00` に修正。

**MEDIUM — ACCESS-02:** アクセス情報テーブルに「店舗前に駐車スペース2台あり」が記載されていない（コピー仕様に存在）。補足テキストとFAQには記述あり。
→ 修正方針: アクセスDLに駐車場の項目を追加することを推奨。

---

## 3. ブランドボイス確認

**MEDIUM — BRAND-01:** ギャラリーCTAに「季節限定情報」という表現あり（コピー03_copy.md に由来）。禁止ワード「限定」に該当するが、ディスカウント文脈ではなく情報提供文脈のため実害は低い。コピーライターとの確認を推奨。

禁止ワード（安い・激安・お得）: 未検出 — OK
トーン（温かく・誠実・親しみやすい）: 全セクション維持 — OK

---

## 4. SEO確認

- JSON-LD CafeOrRestaurant: 存在 — OK
- JSON-LD FAQPage（6問全て）: 存在 — OK
- JSON-LD WebSite: 存在 — OK
- OGP（og:type/title/description/url/image/site_name/locale）: 全項目存在 — OK
- Twitter Card（card/site/title/description/image）: 全項目存在 — OK
- canonical タグ: 存在 — OK
- h1 が1つのみ: 確認 — OK
- 見出し階層（h1>h2>h3）: 正常 — OK

**MEDIUM — SEO-01:** JSON-LDの `openingHoursSpecification` に火曜定休・祝日翌水曜振替の例外が未反映。`specialOpeningHoursSpecification` の追加を推奨。

**LOW — SEO-02:** JSON-LDの `priceRange: "¥600〜¥800"` が実際のメニュー価格帯（¥520〜¥750）と不一致。`"¥520〜¥750"` に修正推奨。

**LOW — GALLERY-01:** ギャラリーリードの `#thecornercafe` がプレーンテキスト。Instagramのハッシュタグリンクに変更すると利便性向上（任意）。

**LOW — COPY-03:** フッターの著作権表記が `<small>` タグでラップされているが、コピー仕様には記載なし。機能上問題なし。
