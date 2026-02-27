#!/usr/bin/env python3
"""
generate_images.py — Webサイト用画像一括生成スクリプト

Gemini Imagen 3 API を使用して、Webサイトに必要な画像を一括生成する。

使い方:
  # Windows
  set GEMINI_API_KEY=your_api_key
  python generate_images.py

  # Mac / Linux
  export GEMINI_API_KEY=your_api_key
  python generate_images.py

機能:
  - 既存の画像はスキップ（途中から再開可能）
  - 失敗時は自動リトライ（最大3回）
  - 生成結果を 画像プレースホルダー一覧.md に記録

依存:
  pip install google-genai
"""

import io
import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Windows ターミナルの文字化け対策
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# ── 依存チェック ──────────────────────────────────────────────
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("エラー: google-genai がインストールされていません")
    print("実行してください: pip install google-genai")
    sys.exit(1)


# ============================================================
# 設定（案件ごとにここを変更する）
# ============================================================

PROJECT_NAME = "THE-CORNER-CAFE"
OUTPUT_DIR   = Path(f"output/{PROJECT_NAME}/assets/images")

MODEL       = "imagen-4.0-generate-001"
MAX_RETRIES = 3
RETRY_WAIT  = 15   # リトライまでの待機秒数
API_WAIT    = 3    # 連続生成時のインターバル（レート制限対策）


# ============================================================
# ブランドスタイル（全プロンプト末尾に付加）
# ============================================================

BRAND_STYLE = (
    "warm natural lighting, soft bokeh background, "
    "earthy color palette (warm brown, off-white, muted sage green), "
    "film photography aesthetic, high quality editorial photography, "
    "Japanese neighborhood cafe atmosphere"
)

NEGATIVE_PROMPT = (
    "text, watermark, logo, blurry, low quality, overexposed, "
    "harsh shadows, neon colors, plastic, artificial, cartoon, illustration"
)


# ============================================================
# 画像定義リスト
# ============================================================
# aspect_ratio: "1:1" / "4:3" / "3:4" / "16:9" / "9:16"

IMAGES = [

    # ── ヒーロー ────────────────────────────────────────────
    {
        "filename": "hero.jpg",
        "aspect_ratio": "16:9",
        "prompt": (
            "Inviting corner cafe interior, warm ambient lighting, "
            "wooden furniture and counter, espresso machine gleaming, "
            "potted green plants by large windows, "
            "morning sunlight streaming in, empty before opening, "
            "shot from cafe entrance looking in. "
            + BRAND_STYLE
        ),
    },

    # ── コンセプト ──────────────────────────────────────────
    {
        "filename": "concept.jpg",
        "aspect_ratio": "4:3",
        "prompt": (
            "Close-up of experienced barista hands carefully inspecting "
            "roasted coffee beans in wooden scoop, "
            "coffee roasting equipment in soft background, "
            "artisan craft feel, warm studio lighting. "
            + BRAND_STYLE
        ),
    },

    # ── コーヒーメニュー ────────────────────────────────────
    {
        "filename": "coffee-01.jpg",
        "aspect_ratio": "4:3",
        "prompt": (
            "Classic hand-drip coffee in matte ceramic mug on wooden table, "
            "rich dark brown color, gentle steam rising, "
            "simple clean composition, cafe counter setting. "
            + BRAND_STYLE
        ),
    },
    {
        "filename": "coffee-02.jpg",
        "aspect_ratio": "4:3",
        "prompt": (
            "Single origin pour-over coffee in glass server, "
            "bright amber and gold liquid, gooseneck kettle mid-pour, "
            "visible bloom, specialty coffee presentation. "
            + BRAND_STYLE
        ),
    },
    {
        "filename": "coffee-03.jpg",
        "aspect_ratio": "4:3",
        "prompt": (
            "Cafe latte in large white ceramic cup, "
            "simple tulip latte art on creamy micro-foam, "
            "wooden table, cozy cafe atmosphere. "
            + BRAND_STYLE
        ),
    },
    {
        "filename": "coffee-04.jpg",
        "aspect_ratio": "4:3",
        "prompt": (
            "Specialty filter coffee in transparent glass cup, "
            "golden translucent color showing clarity, "
            "minimalist presentation on marble surface. "
            + BRAND_STYLE
        ),
    },

    # ── スイーツメニュー ────────────────────────────────────
    {
        "filename": "sweets-01.jpg",
        "aspect_ratio": "4:3",
        "prompt": (
            "Basque burnt cheesecake slice on white ceramic plate, "
            "deeply caramelized golden-brown top, "
            "creamy jiggly interior visible at cut edge, "
            "rustic wooden table, dessert fork beside. "
            + BRAND_STYLE
        ),
    },
    {
        "filename": "sweets-02.jpg",
        "aspect_ratio": "4:3",
        "prompt": (
            "Seasonal fruit tart on white ceramic plate, "
            "glossy fresh strawberries and blueberries arranged on "
            "smooth vanilla custard, flaky golden pastry shell, "
            "food styling, top-down angle. "
            + BRAND_STYLE
        ),
    },
    {
        "filename": "sweets-03.jpg",
        "aspect_ratio": "4:3",
        "prompt": (
            "Two freshly baked scones on small wooden serving board, "
            "golden-brown crispy exterior, visible layers, "
            "small ceramic jar of jam and clotted cream beside, "
            "afternoon tea setting. "
            + BRAND_STYLE
        ),
    },
    {
        "filename": "sweets-04.jpg",
        "aspect_ratio": "4:3",
        "prompt": (
            "Matcha terrine slice on dark navy ceramic plate, "
            "deep vibrant green color, smooth dense silky texture, "
            "light dusting of matcha powder on top, "
            "Japanese minimalist aesthetic, side view. "
            + BRAND_STYLE
        ),
    },

    # ── ギャラリー ──────────────────────────────────────────
    {
        "filename": "gallery-01.jpg",
        "aspect_ratio": "1:1",
        "prompt": (
            "Overhead flat lay, coffee cup and cheesecake slice "
            "on wooden cafe table, morning light, lifestyle photography, "
            "square composition. "
            + BRAND_STYLE
        ),
    },
    {
        "filename": "gallery-02.jpg",
        "aspect_ratio": "1:1",
        "prompt": (
            "Coffee cup beside open book on wooden windowsill, "
            "golden hour sunlight, cozy reading atmosphere, "
            "square composition. "
            + BRAND_STYLE
        ),
    },
    {
        "filename": "gallery-03.jpg",
        "aspect_ratio": "1:1",
        "prompt": (
            "Latte art close-up, delicate rosette pattern on "
            "velvety micro-foam milk, matte ceramic cup, "
            "marble cafe surface, square composition. "
            + BRAND_STYLE
        ),
    },
    {
        "filename": "gallery-04.jpg",
        "aspect_ratio": "1:1",
        "prompt": (
            "Cafe interior wide shot, afternoon golden light, "
            "wooden tables and chairs, hanging plants, "
            "warm inviting empty cafe, square composition. "
            + BRAND_STYLE
        ),
    },
    {
        "filename": "gallery-05.jpg",
        "aspect_ratio": "1:1",
        "prompt": (
            "Seasonal sweets display on wooden counter, "
            "cheesecake and tart under glass cloche dome, "
            "handwritten chalkboard menu behind, square composition. "
            + BRAND_STYLE
        ),
    },
    {
        "filename": "gallery-06.jpg",
        "aspect_ratio": "1:1",
        "prompt": (
            "Barista hand-scooping freshly roasted coffee beans "
            "into kraft paper bag, roastery setting, "
            "artisan retail atmosphere, square composition. "
            + BRAND_STYLE
        ),
    },

    # ── スタッフ ────────────────────────────────────────────
    {
        "filename": "staff-01.jpg",
        "aspect_ratio": "1:1",
        "prompt": (
            "Japanese male barista in his early 30s, "
            "wearing natural linen apron, "
            "standing confidently at coffee roaster, "
            "warm friendly professional expression, "
            "chest-up portrait, cafe background softly blurred. "
            + BRAND_STYLE
        ),
    },
    {
        "filename": "staff-02.jpg",
        "aspect_ratio": "1:1",
        "prompt": (
            "Japanese female pastry chef in her late 20s, "
            "wearing white chef apron, "
            "holding a freshly made fruit tart with both hands, "
            "soft smile, bright kitchen background. "
            "Chest-up portrait. "
            + BRAND_STYLE
        ),
    },
    {
        "filename": "staff-03.jpg",
        "aspect_ratio": "1:1",
        "prompt": (
            "Japanese female barista in her mid 20s, "
            "pouring latte art into cup, natural warm smile, "
            "cafe counter with espresso machine behind, "
            "chest-up portrait, candid moment. "
            + BRAND_STYLE
        ),
    },

    # ── OG 画像 ─────────────────────────────────────────────
    {
        "filename": "og-image.jpg",
        "aspect_ratio": "16:9",
        "prompt": (
            "Charming corner cafe exterior at dusk, "
            "warm golden light glowing from windows, "
            "wooden sign, small potted plants by entrance, "
            "quiet residential neighborhood street. "
            + BRAND_STYLE
        ),
    },
]


# ============================================================
# 生成処理
# ============================================================

def generate_image(
    client: "genai.Client",
    image_spec: dict,
    output_path: Path,
) -> bool:
    """1枚の画像を生成して保存する。成功したら True を返す。"""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"    生成中 (試行 {attempt}/{MAX_RETRIES})...", end=" ", flush=True)

            response = client.models.generate_images(
                model=MODEL,
                prompt=image_spec["prompt"],
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio=image_spec.get("aspect_ratio", "4:3"),
                    safety_filter_level="block_low_and_above",
                ),
            )

            if not response.generated_images:
                raise ValueError("画像が返されませんでした（空レスポンス）")

            image_bytes = response.generated_images[0].image.image_bytes
            output_path.write_bytes(image_bytes)

            size_kb = len(image_bytes) // 1024
            print(f"✅  {size_kb} KB")
            return True

        except Exception as e:
            print(f"❌  {e}")
            if attempt < MAX_RETRIES:
                print(f"    {RETRY_WAIT}秒後にリトライします...")
                time.sleep(RETRY_WAIT)

    return False


def write_manifest(results: dict) -> Path:
    """生成結果の一覧 Markdown を書き出す。"""
    manifest_path = OUTPUT_DIR / "画像プレースホルダー一覧.md"
    with manifest_path.open("w", encoding="utf-8") as f:
        f.write(f"# {PROJECT_NAME} — 画像一覧\n\n")
        f.write(f"生成日: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("| ファイル名 | アスペクト比 | 状態 |\n")
        f.write("|-----------|------------|------|\n")
        for img in IMAGES:
            fn = img["filename"]
            ar = img.get("aspect_ratio", "4:3")
            if fn in results["success"]:
                status = "✅ 生成済み"
            elif fn in results["skip"]:
                status = "⏭️  既存スキップ"
            else:
                status = "❌ 失敗"
            f.write(f"| `{fn}` | {ar} | {status} |\n")
    return manifest_path


def main():
    # ── API キー確認 ────────────────────────────────────────
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("\nエラー: GEMINI_API_KEY が設定されていません")
        print("  Windows: set GEMINI_API_KEY=your_key")
        print("  Mac/Linux: export GEMINI_API_KEY=your_key\n")
        sys.exit(1)

    # ── 準備 ────────────────────────────────────────────────
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=api_key)

    total = len(IMAGES)
    print(f"\n{'='*50}")
    print(f"  {PROJECT_NAME} — 画像生成")
    print(f"  モデル: {MODEL}")
    print(f"  合計:   {total} 枚")
    print(f"  出力先: {OUTPUT_DIR.resolve()}")
    print(f"{'='*50}\n")

    # ── 生成ループ ──────────────────────────────────────────
    results: dict[str, list[str]] = {"success": [], "skip": [], "fail": []}

    for i, img in enumerate(IMAGES, 1):
        output_path = OUTPUT_DIR / img["filename"]
        print(f"[{i:02d}/{total}] {img['filename']}")

        # 既存ファイルはスキップ（再開対応）
        if output_path.exists():
            print(f"    ⏭️  スキップ（既存: {output_path.stat().st_size // 1024} KB）")
            results["skip"].append(img["filename"])
        else:
            ok = generate_image(client, img, output_path)
            (results["success"] if ok else results["fail"]).append(img["filename"])

        # インターバル（最後の1枚以外）
        if i < total:
            time.sleep(API_WAIT)

    # ── サマリー ────────────────────────────────────────────
    print(f"\n{'='*50}")
    print(f"  完了")
    print(f"  ✅ 成功:      {len(results['success'])} 枚")
    print(f"  ⏭️  スキップ:  {len(results['skip'])} 枚")
    print(f"  ❌ 失敗:      {len(results['fail'])} 枚")

    if results["fail"]:
        print(f"\n  失敗ファイル（再実行すれば再試行されます）:")
        for fn in results["fail"]:
            print(f"    - {fn}")

    manifest = write_manifest(results)
    print(f"\n  📄 一覧: {manifest}")
    print(f"  🌐 確認: http://localhost/claude-code-website/output/{PROJECT_NAME}/")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
