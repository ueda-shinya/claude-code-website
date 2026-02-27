# THE CORNER CAFE

## 概要
東京・世田谷・三軒茶屋の自家焙煎コーヒーと手作りスイーツのカフェ（ONE PAGE LP）。
地域密着5年、リピーター率80%以上を訴求するコンバージョン最適化サイト。

## ファイル構成

```
THE-CORNER-CAFE_v3/
├── index.html              ← メインページ（SEO強化版）
├── assets/
│   ├── css/
│   │   └── styles.css      ← FLOCSS / モバイルファースト / CSS Custom Properties
│   ├── js/
│   │   └── script.js       ← バニラJS (ハンバーガー/タブ/アコーディオン/フォーム/モーダル)
│   └── images/
│       ├── hero.webp
│       ├── menu-*.webp     ← コーヒーメニュー 6枚
│       ├── sweets-*.webp   ← スイーツメニュー 6枚
│       ├── gallery-*.webp  ← ギャラリー 6枚
│       ├── staff-*.webp    ← スタッフ 3枚
│       ├── og-image.webp   ← OGP用（1200×630）
│       └── 画像プレースホルダー一覧.md
├── php/
│   └── form_handler.php    ← お問い合わせフォームハンドラー
├── logs/
│   ├── .htaccess           ← ブラウザアクセス禁止
│   └── form_log.txt        ← 送信ログ（自動生成）
└── README.md
```

## フォーム設定
- 送信先メール: info@thecornercafe.jp
- ログ保存先: logs/form_log.txt
- セキュリティ: Honeypot + IP レート制限 (60秒/3回) + XSS対策

## 動作確認環境
- Chrome / Safari / Firefox 最新版
- iOS Safari / Android Chrome

## 使用技術
- HTML5（セマンティックマークアップ / FLOCSS）
- CSS3（モバイルファースト / CSS Custom Properties）
- JavaScript（バニラ ES6+ / IntersectionObserver / Fetch API）
- PHP 8.x（フォームハンドラー）
- 画像: WebP（Gemini Imagen 4 生成 → 95%圧縮）

## 確認URL（XAMPP）
http://localhost/claude-code-website/output/THE-CORNER-CAFE_v3/

## 納品日
2026-02-28
