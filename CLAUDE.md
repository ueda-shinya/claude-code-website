# Webサイト制作マルチエージェントチーム

ユーザーからWebサイト制作の依頼があったら、以下のワークフローに従って
**Task ツールでサブエージェントを起動し**、チームで協力してサイトを制作する。

## 出力先
- 作業ファイル: `workspace/`
- 最終成果物: `output/{案件名}/index.html`, `output/{案件名}/assets/css/styles.css`, `output/{案件名}/assets/js/script.js`

---

## ワークフロー

### Phase 0 — インタラクティブヒアリング（制作開始前に必ず実行）

ユーザーからWebサイト制作の依頼があったら、まず `hearing_sheet.md` を読み込む。

#### 対話型ヒアリングの進め方

1. **空欄の検出**
   `hearing_sheet.md` を読み、回答が空・「未定」・未チェックの項目を全て洗い出す。

2. **セクションごとに順番に質問する**
   空欄が多くても一度に全部聞かず、**1セクションずつ進める**。
   各セクションの冒頭に「〇〇について確認します」と宣言してから質問する。

3. **各質問の形式**
   空欄の項目ごとに、**すでに記入された他の情報から推測した提案を3つ**と
   「その他（自由入力）」を必ずセットで提示する。

   ```
   例）業種が「カフェ」と記入されている場合の「デザインスタイル」の質問:

   デザインの雰囲気はどのようにしますか？

   1. ナチュラル・温かみ  — 木目・グリーン・手書き風フォントで居心地の良さを表現
   2. スタイリッシュ・都会的 — モノトーン＋アクセントカラーでトレンド感を演出
   3. ポップ・カジュアル  — 明るい配色とイラストで気軽に入れる雰囲気を表現
   4. その他（自由に教えてください）
   ```

4. **回答の即時反映**
   クライアントが選択・回答したら、その内容を `hearing_sheet.md` に書き込んでから次の質問へ進む。
   「1」「2」「3」の数字だけの回答でも対応する。

5. **提案の根拠**
   提案3つは必ず「既記入の情報（業種・ターゲット・目的など）」から論理的に導くこと。
   汎用的な選択肢ではなく、そのクライアント固有の文脈に合わせる。

6. **全項目が埋まったら確認**
   全セクションのヒアリングが完了したら、記入内容をサマリーして確認を取る:
   > 「以上の内容で制作を進めてよいですか？修正があればお知らせください。」
   確認が取れたら Phase 1 へ進む。

#### 既に全て記入済みの場合
`hearing_sheet.md` の内容を確認し、不明点があれば上記の形式で最大3点だけ質問する。
問題なければ即 Phase 1 へ進む。

---

### Phase 1 — PM（自分で実行）
`hearing_sheet.md` の内容をベースに、以下を含む仕様書を `workspace/01_spec.md` に作成する:
- ビジネス目標・ターゲット・バリュープロポジション
- ページ構成・セクション一覧
- デザイン方向性（カラー・フォント・スタイル）
- 必要な機能・インタラクション
- ブランドボイス・トーン

### Phase 2 — 並列（Task ツールで3エージェントを同時起動）
以下の3つを **1つのメッセージで並列に** Task ツール呼び出しする:

**UI/UXデザイナー** (`workspace/02_ux.md`)
- カラーシステム（HEXコード付き）、タイポグラフィスケール（rem値）
- レイアウト・グリッド・ブレークポイント（375px / 768px / 1280px）
- コンポーネント仕様（ボタン・カード・ナビ）
- アニメーション・トランジション仕様

**マーケター** (`workspace/02_marketing.md`)
- プライマリバリュープロポジション（1文）
- メッセージング階層・CTA戦略・配置
- ソーシャルプルーフ・信頼シグナル
- 緊急性・感情的トリガー

**セールスライター** (`workspace/02_copy.md`)
- 全セクションの実際のコピー（プレースホルダー厳禁）
- ヒーロー・問題提起・ソリューション・フィーチャー・FAQ・CTA・フッター

### Phase 3 — HTMLデザイナー（Task ツール）
`workspace/01_spec.md`, `02_ux.md`, `02_marketing.md`, `02_copy.md` を参照して
完全な `workspace/03_index.html` を作成:
- セマンティックHTML5（header / nav / main / section / footer）
- BEM命名規則のクラス名
- セールスライターのコピーをそのまま使用
- styles.css と script.js をリンク

### Phase 4 — 並列（Task ツールで2エージェントを同時起動）

**スタイリスト** (`workspace/04_styles.css`)
- CSS カスタムプロパティ（--変数）でデザインシステム定義
- モバイルファースト（min-widthメディアクエリ）
- CSS Grid / Flexbox レイアウト
- ホバー・トランジション・アニメーション
- 外部依存なし（純粋CSS）

**フロントエンドエンジニア** (`workspace/04_script.js`)
- バニラJS（ES6+、ライブラリなし）
- ハンバーガーメニュー・スムーズスクロール
- IntersectionObserver スクロールリビール
- フォームバリデーション・送信処理
- 画像遅延読み込み

### Phase 5 — SEO担当者（Task ツール）
`workspace/03_index.html` を強化して `workspace/05_seo.html` を作成:
- タイトル・メタディスクリプション・OGP・Twitter Card
- JSON-LD構造化データ（Organization・FAQPage）
- h1が1つ、見出し階層が正しいことを確認

### Phase 6 — レビュワー（Task ツール）
全ファイルを確認して `workspace/06_review.md` を作成:
- HTML・CSS・JSの整合性（クラス名・IDの一致）
- アクセシビリティ（ARIA・altテキスト・フォームラベル）
- セキュリティ（XSS・インラインイベントハンドラ）
- モバイル対応・パフォーマンス

### Phase 7 — 最終組み立て（自分で実行）
レビュー結果を反映しながら、**ファイル管理ルール**に従って納品物を書き出す（後述）。

---

## エージェントへの指示の原則

- 各 Task エージェントには **役割・参照ファイルの内容・出力ファイル名** を明示する
- HTMLエージェントには必ずコピーのテキストを渡す（プレースホルダー排除）
- CSSエージェントにはHTMLのクラス名/ID一覧を渡す（整合性確保）
- JSエージェントにはHTMLの構造を渡す（セレクター整合性確保）
- `general-purpose` エージェントタイプを使用する

---

## 制作品質ルール

全エージェントは以下のルールを**絶対に守る**こと。レビュワーはこのルールへの準拠を必ず確認する。

### モバイルファースト（必須）
- CSS は `min-width` メディアクエリのみ使用（`max-width` 禁止）
- 基準ブレークポイント: 375px（スマホ）→ 768px（タブレット）→ 1280px（デスクトップ）
- タップターゲットは最小 44px × 44px

### パフォーマンス基準
- 外部CSSライブラリ・JSライブラリの読み込み禁止（バニラのみ）
- CSSアニメーションは `transform` と `opacity` のみ使用（`top/left/width` などlayoutプロパティ禁止）
- フォールド以下の画像は `loading="lazy"` を必ず付与
- `<link rel="preload">` でクリティカルなフォントを先読み

### CSSクラス命名規則：FLOCSS
以下のレイヤー構造と命名規則を厳守する:

```
Foundation  : リセット・ベーススタイル（クラスなし、要素セレクタのみ）
Layout      : l-header / l-footer / l-main / l-sidebar  （プレフィックス: l-）
Component   : c-button / c-card / c-form               （プレフィックス: c-）
Project     : p-hero / p-about / p-service / p-contact  （プレフィックス: p-）
Utility     : u-mt-16 / u-text-center / u-hidden        （プレフィックス: u-）
```

- Modifier は `c-button--primary` のようにダブルハイフン
- 状態変化は `is-active` / `is-open` / `is-error` のように `is-` プレフィックス

### フォームセキュリティ（必須）
入力フォームが1つでもある場合、以下を**全て実装**すること:

**フロントエンド（script.js）:**
- 全入力値をHTMLエスケープ処理してからDOMに挿入（`innerHTML` 禁止、`textContent` を使用）
- 送信ボタンの二重送信防止（送信後に `disabled` 化）
- クライアントサイドバリデーション（メール形式・必須チェック・文字数制限）
- reCAPTCHA v3 または Honeypot フィールドによるbot対策

**バックエンド（php/form_handler.php）:**
- `htmlspecialchars()` によるXSSサニタイズ
- `filter_var()` によるメールアドレス検証
- IPベースのレート制限（同一IPから60秒以内に3回以上の送信をブロック）
- POSTメソッド・Content-Typeの確認（CSRFトークン検証推奨）

### フォームログ（必須）
フォームの全送信試行を `logs/form_log.txt` に記録すること。

**ログ形式（1行1件、TSV）:**
```
{ISO8601日時}  {IPアドレス}  {ステータス}  {名前}  {メールアドレス}  {UA}
```

**ステータスの種類:**
- `SUCCESS`  : 正常送信完了
- `BLOCKED`  : セキュリティ機能（レート制限・bot検知）によりブロック
- `ERROR`    : バリデーションエラーで送信不可
- `SPAM`     : スパム判定でブロック

**実装例（PHP）:**
```php
function write_form_log(string $status, array $data): void {
    $log_dir = __DIR__ . '/../logs';
    if (!is_dir($log_dir)) mkdir($log_dir, 0750, true);
    $line = implode("\t", [
        date('c'),
        $_SERVER['REMOTE_ADDR'] ?? 'unknown',
        $status,
        $data['name']  ?? '',
        $data['email'] ?? '',
        $_SERVER['HTTP_USER_AGENT'] ?? '',
    ]);
    file_put_contents($log_dir . '/form_log.txt', $line . PHP_EOL, FILE_APPEND | LOCK_EX);
}
```

> **注意:** `logs/` ディレクトリは `.htaccess` でブラウザから直接アクセスできないよう保護すること。

---

## ファイル管理ルール

### 案件ごとのフォルダ構成
納品物は `output/{案件名}/` に格納する。案件名はヒアリングシートの「サイト名」を使用。

```
output/
└── {案件名}/
    ├── index.html
    ├── assets/
    │   ├── css/
    │   │   └── styles.css
    │   ├── js/
    │   │   └── script.js
    │   └── images/
    │       └── （画像プレースホルダー一覧.md）
    ├── php/
    │   └── form_handler.php    ← フォームがある場合のみ
    ├── logs/
    │   └── .htaccess           ← ブラウザアクセス禁止
    └── README.md
```

### README.md の必須記載内容
```markdown
# {サイト名}

## 概要
{業種・目的の1〜2文}

## ファイル構成
{ファイルツリー}

## フォーム設定
- 送信先メール: {hearing_sheet.md の値}
- ログ保存先: logs/form_log.txt

## 動作確認環境
- Chrome / Safari / Firefox 最新版
- iOS Safari / Android Chrome

## 納品日
{日付}
```

### 既存 output/ の上書き禁止
同名フォルダが既に存在する場合は上書きせず、`{案件名}_v2/` のように連番で保存すること。

### workspace/ の自動リセット
新しい案件を開始する前に `workspace/` の内容を削除してよいか確認する:
> 「前回の workspace/ が残っています。削除して新しい案件を始めますか？」

---

## XAMPPプレビュー
完成後は以下のURLで確認できる:
`http://localhost/claude-code-website/output/{案件名}/`
