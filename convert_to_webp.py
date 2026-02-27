#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert_to_webp.py - Webサイト用画像一括WebP変換スクリプト

サイト完成後に実行する。
output/{案件名}/assets/images/ 内の JPG/PNG を WebP に変換し、
index.html の拡張子参照も一括置換する。

使い方:
  python convert_to_webp.py

機能:
  - JPG / PNG -> WebP 変換（元ファイルは残す or 削除を選択）
  - index.html の .jpg / .png 参照を .webp に自動置換
  - 変換結果レポートを表示
"""

import io
import shutil
import sys
from io import BytesIO
from pathlib import Path

# Windows ターミナルの文字化け対策
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

try:
    from PIL import Image
except ImportError:
    print("エラー: Pillow がインストールされていません")
    print("実行してください: pip install Pillow")
    sys.exit(1)


# ============================================================
# 設定（案件ごとにここを変更する）
# ============================================================

PROJECT_NAME = "THE-CORNER-CAFE"
IMAGES_DIR   = Path(f"output/{PROJECT_NAME}/assets/images")
HTML_PATH    = Path(f"output/{PROJECT_NAME}/index.html")

WEBP_QUALITY    = 85    # 1~100（85 が品質・サイズのバランス推奨）
DELETE_ORIGINALS = False  # True にすると変換後に元ファイルを削除


# ============================================================
# 変換対象の拡張子
# ============================================================

SOURCE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


# ============================================================
# 変換処理
# ============================================================

def convert_image(src: Path, quality: int) -> tuple:
    """
    1枚の画像を WebP に変換する。
    戻り値: (成功フラグ, 元ファイルサイズ[KB], 変換後サイズ[KB])
    """
    dst = src.with_suffix(".webp")

    try:
        with Image.open(src) as img:
            # RGBA / P -> RGB 変換（JPEG などアルファなし形式への対応）
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")

            buf = BytesIO()
            img.save(buf, format="WEBP", quality=quality, method=6)
            webp_bytes = buf.getvalue()

        dst.write_bytes(webp_bytes)

        src_kb = src.stat().st_size // 1024
        dst_kb = len(webp_bytes) // 1024
        return True, src_kb, dst_kb

    except Exception as e:
        print(f"    [NG] エラー: {e}")
        return False, 0, 0


# ============================================================
# HTML 置換処理
# ============================================================

def update_html(html_path: Path) -> int:
    """
    HTML 内の .jpg / .jpeg / .png を .webp に置換する。
    戻り値: 置換件数
    """
    if not html_path.exists():
        print(f"  HTML が見つかりません: {html_path}")
        return 0

    original = html_path.read_text(encoding="utf-8")
    updated  = original

    for ext in (".jpg", ".jpeg", ".png"):
        updated = updated.replace(ext, ".webp")

    count = updated.count(".webp") - original.count(".webp")

    if count > 0:
        # バックアップを作成してから書き込む
        backup = html_path.with_suffix(".html.bak")
        shutil.copy2(html_path, backup)
        html_path.write_text(updated, encoding="utf-8")
        print(f"  [OK] {count} 箇所を置換しました（バックアップ: {backup.name}）")
    else:
        print("  変更なし（すでに .webp 参照済み、または画像参照なし）")

    return count


# ============================================================
# メイン
# ============================================================

def main():
    if not IMAGES_DIR.exists():
        print(f"エラー: 画像ディレクトリが見つかりません: {IMAGES_DIR}")
        sys.exit(1)

    targets = sorted(
        p for p in IMAGES_DIR.iterdir()
        if p.suffix.lower() in SOURCE_EXTENSIONS
    )

    if not targets:
        print("変換対象の画像が見つかりません（JPG/PNG）")
        sys.exit(0)

    total = len(targets)
    print(f"\n{'='*50}")
    print(f"  {PROJECT_NAME} - WebP 変換")
    print(f"  品質:         {WEBP_QUALITY}")
    print(f"  対象:         {total} 枚")
    print(f"  元ファイル削除: {'する' if DELETE_ORIGINALS else 'しない'}")
    print(f"{'='*50}\n")

    results = {"success": [], "fail": []}
    total_src_kb = 0
    total_dst_kb = 0

    for i, src in enumerate(targets, 1):
        print(f"[{i:02d}/{total}] {src.name}")
        ok, src_kb, dst_kb = convert_image(src, WEBP_QUALITY)

        if ok:
            saved_kb = src_kb - dst_kb
            ratio    = (1 - dst_kb / src_kb) * 100 if src_kb else 0
            print(f"    [OK] {src_kb} KB -> {dst_kb} KB  (-{saved_kb} KB / {ratio:.0f}% 削減)")
            results["success"].append(src.name)
            total_src_kb += src_kb
            total_dst_kb += dst_kb

            if DELETE_ORIGINALS:
                src.unlink()
        else:
            results["fail"].append(src.name)

    # HTML 置換
    print("\n-- index.html 更新 --")
    update_html(HTML_PATH)

    # サマリー
    saved_total = total_src_kb - total_dst_kb
    ratio_total = (1 - total_dst_kb / total_src_kb) * 100 if total_src_kb else 0

    print(f"\n{'='*50}")
    print(f"  完了")
    print(f"  成功: {len(results['success'])} 枚")
    print(f"  失敗: {len(results['fail'])} 枚")
    print(f"  合計削減: {total_src_kb} KB -> {total_dst_kb} KB  (-{saved_total} KB / {ratio_total:.0f}%)")
    print(f"{'='*50}\n")

    if results["fail"]:
        print("  失敗ファイル:")
        for fn in results["fail"]:
            print(f"    - {fn}")


if __name__ == "__main__":
    main()
