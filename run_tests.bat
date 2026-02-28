@echo off
chcp 65001 > nul
echo ========================================
echo  Playwright テスト実行
echo  対象: THE-CORNER-CAFE_v3
echo ========================================
echo.

REM 別のサイトをテストする場合:
REM set TEST_BASE_URL=http://localhost/claude-code-website/output/MY-SITE/

python -m pytest tests/ ^
  --html=test_report.html ^
  --self-contained-html ^
  -v

echo.
echo ----------------------------------------
echo レポートを開きます: test_report.html
echo ----------------------------------------
start test_report.html

pause
