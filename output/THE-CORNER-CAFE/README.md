# THE CORNER CAFE

## 概要
東京・世田谷区さくら台にあるスペシャルティコーヒーカフェの公式サイト。
新規来店促進とコーヒー文化の発信を目的としたランディングページ。

## ファイル構成

```
THE-CORNER-CAFE/
├── index.html                       # メインページ（SEO最適化済み）
├── assets/
│   ├── css/
│   │   └── styles.css               # スタイルシート（FLOCSS / モバイルファースト）
│   ├── js/
│   │   └── script.js                # バニラJS（ES6+）
│   └── images/
│       └── 画像プレースホルダー一覧.md  # 必要画像の一覧
├── php/
│   └── form_handler.php             # お問い合わせフォームハンドラー
├── logs/
│   └── .htaccess                    # ログディレクトリへのブラウザアクセス禁止
└── README.md
```

## フォーム設定

- 送信先メール: `info@thecornercafe.jp`
- ログ保存先: `logs/form_log.txt`（フォーム送信のたびに追記）
- セキュリティ: Honeypot / IPレート制限（60秒/3回） / XSSサニタイズ / ヘッダーインジェクション対策

## 画像生成

```bash
# プロジェクトルートで実行（Gemini Imagen API が必要）
python generate_images.py

# 生成後に WebP 変換する場合
python convert_to_webp.py
```

生成される画像は `assets/images/` に配置してください。

## 動作確認環境

- Chrome / Safari / Firefox 最新版
- iOS Safari / Android Chrome

## ローカルプレビュー（XAMPP）

```
http://localhost/claude-code-website/output/THE-CORNER-CAFE/
```

## 納品日

2026-02-27
