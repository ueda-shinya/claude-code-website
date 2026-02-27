<?php
declare(strict_types=1);

/**
 * THE CORNER CAFE — お問い合わせフォームハンドラー
 *
 * POST リクエストを受け取り、バリデーション・セキュリティチェック・
 * ログ記録・メール送信を行い、JSON レスポンスを返す。
 *
 * 動作要件: PHP 7.4+、XAMPP
 */

// ============================================================
// 初期設定
// ============================================================

// エラー表示をオフ（本番環境向け）
ini_set('display_errors', '0');
ini_set('log_errors', '1');

// セッション開始（将来的な CSRF トークン対応のため）
session_start();

// 定数定義
define('MAIL_TO',   'info@thecornercafe.jp');
define('MAIL_FROM', 'noreply@thecornercafe.jp');
define('SITE_NAME', 'THE CORNER CAFE');

// ログディレクトリ（このファイルの親ディレクトリ配下の logs/）
define('LOG_DIR',        __DIR__ . '/../logs/');
define('LOG_FILE',       LOG_DIR . 'form_log.txt');
define('RATE_LIMIT_FILE', LOG_DIR . 'rate_limit.json');

// レート制限設定
define('RATE_LIMIT_MAX',    10);     // ウィンドウ内の最大送信回数
define('RATE_LIMIT_WINDOW', 3600);   // ウィンドウ幅（秒）

// ============================================================
// セキュリティヘッダー（レスポンス冒頭で設定）
// ============================================================

header('Content-Type: application/json; charset=UTF-8');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header('X-XSS-Protection: 1; mode=block');
header('Referrer-Policy: strict-origin-when-cross-origin');

// ============================================================
// メイン処理
// ============================================================

/**
 * JSON レスポンスを出力してスクリプトを終了する
 *
 * @param bool   $success  成否
 * @param string $message  メッセージ
 * @param int    $httpCode HTTP ステータスコード
 */
function sendResponse(bool $success, string $message, int $httpCode = 200): void
{
    http_response_code($httpCode);
    echo json_encode(
        ['success' => $success, 'message' => $message],
        JSON_UNESCAPED_UNICODE
    );
    exit;
}

// POST メソッドのみ受け付ける
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Allow: POST');
    sendResponse(false, 'Method Not Allowed', 405);
}

// ------------------------------------------------------------
// 1. Referer チェック（簡易 CSRF 対策）
// ------------------------------------------------------------
// 静的 HTML 環境のため、Referer に localhost または thecornercafe.jp が
// 含まれることを確認する。
// ※ 本番運用では SameSite=Lax Cookie の設定を推奨。
// ------------------------------------------------------------
checkReferer();

// ------------------------------------------------------------
// 2. Honeypot チェック
// ------------------------------------------------------------
$website = $_POST['website'] ?? '';
if (checkHoneypot($website)) {
    // ボットを欺くためサイレント成功を返す
    writeLog('HONEYPOT', '', '', '');
    sendResponse(true, 'お問い合わせを受け付けました。2営業日以内にご返信します。');
}

// ------------------------------------------------------------
// 3. IP アドレス取得
// ------------------------------------------------------------
$ip = getClientIp();

// ------------------------------------------------------------
// 4. レート制限チェック
// ------------------------------------------------------------
if (!checkRateLimit($ip)) {
    writeLog('RATE_LIMIT', '', '', '', $ip);
    sendResponse(false, '送信回数が上限を超えました。しばらく時間をおいてから再度お試しください。', 429);
}

// ------------------------------------------------------------
// 5. 入力バリデーション
// ------------------------------------------------------------
$validationResult = validateInput($_POST);
if ($validationResult['error'] !== '') {
    writeLog('VALIDATION_ERROR', '', '', '', $ip);
    sendResponse(false, $validationResult['error'], 400);
}

$name    = $validationResult['name'];
$email   = $validationResult['email'];
$message = $validationResult['message'];

// ------------------------------------------------------------
// 6. メール送信
// ------------------------------------------------------------
$isLocalhost = (
    ($_SERVER['SERVER_NAME'] ?? '') === 'localhost' ||
    ($_SERVER['HTTP_HOST']   ?? '') === 'localhost' ||
    strpos(($_SERVER['HTTP_HOST'] ?? ''), '127.0.0.1') !== false
);

if ($isLocalhost) {
    // ローカル環境ではメール送信をスキップ
    writeLog('MAIL_SKIPPED', $name, $email, $message, $ip);
} else {
    $mailSent = sendMail($name, $email, $message, $ip);
    if (!$mailSent) {
        writeLog('MAIL_ERROR', $name, $email, $message, $ip);
        sendResponse(false, 'メール送信に失敗しました。お手数ですが、直接 ' . MAIL_TO . ' までご連絡ください。', 500);
    }
    writeLog('SUCCESS', $name, $email, $message, $ip);
}

sendResponse(true, 'お問い合わせを受け付けました。2営業日以内にご返信します。');

// ============================================================
// 関数定義
// ============================================================

/**
 * Referer ヘッダーによる簡易 CSRF チェック
 * 問題があれば 403 を返してスクリプトを終了する
 */
function checkReferer(): void
{
    $referer = $_SERVER['HTTP_REFERER'] ?? '';

    $allowed = ['thecornercafe.jp', 'localhost', '127.0.0.1'];
    $ok = false;
    foreach ($allowed as $host) {
        if (strpos($referer, $host) !== false) {
            $ok = true;
            break;
        }
    }

    // Referer が空の場合も拒否（厳格モード）
    if (!$ok || $referer === '') {
        http_response_code(403);
        echo json_encode(
            ['success' => false, 'message' => 'Forbidden'],
            JSON_UNESCAPED_UNICODE
        );
        exit;
    }
}

/**
 * Honeypot チェック
 * website フィールドに値が入っていればボットと判定する
 *
 * @param  string $honeypotValue Honeypot フィールドの値
 * @return bool   ボットであれば true
 */
function checkHoneypot(string $honeypotValue): bool
{
    return $honeypotValue !== '';
}

/**
 * クライアント IP アドレスを取得する
 * リバースプロキシ環境では X-Forwarded-For を優先する
 *
 * @return string IP アドレス文字列
 */
function getClientIp(): string
{
    $forwarded = getenv('HTTP_X_FORWARDED_FOR');
    if ($forwarded !== false && $forwarded !== '') {
        // カンマ区切りの先頭が実際のクライアント IP
        $parts = explode(',', $forwarded);
        $ip = trim($parts[0]);
    } else {
        $ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
    }

    // IPv4/IPv6 の基本的な形式チェック
    return filter_var($ip, FILTER_VALIDATE_IP) !== false ? $ip : '0.0.0.0';
}

/**
 * ファイルベースのレート制限チェック
 * 1時間以内に同一 IP から RATE_LIMIT_MAX 回を超えた場合に false を返す
 *
 * @param  string $ip クライアント IP アドレス
 * @return bool   送信を許可する場合 true、超過した場合 false
 */
function checkRateLimit(string $ip): bool
{
    // logs/ ディレクトリがなければ作成
    ensureLogDir();

    $now = time();

    // ファイルを排他ロックで開く（存在しなければ作成）
    $fp = fopen(RATE_LIMIT_FILE, 'c+');
    if ($fp === false) {
        // ファイルを開けない場合はレート制限をスキップ（フェイルオープン）
        return true;
    }

    flock($fp, LOCK_EX);

    // 既存データを読み込む
    $contents = stream_get_contents($fp);
    $data = [];
    if ($contents !== false && $contents !== '') {
        $decoded = json_decode($contents, true);
        if (is_array($decoded)) {
            $data = $decoded;
        }
    }

    // 期限切れエントリを削除（メモリ節約）
    foreach ($data as $storedIp => $entry) {
        if (($now - ($entry['window_start'] ?? 0)) > RATE_LIMIT_WINDOW) {
            unset($data[$storedIp]);
        }
    }

    // 現在 IP のカウントを取得・更新
    if (!isset($data[$ip]) || ($now - $data[$ip]['window_start']) > RATE_LIMIT_WINDOW) {
        // 新規ウィンドウ開始
        $data[$ip] = ['count' => 1, 'window_start' => $now];
        $allowed = true;
    } else {
        $data[$ip]['count']++;
        $allowed = ($data[$ip]['count'] <= RATE_LIMIT_MAX);
    }

    // ファイルに書き戻す
    ftruncate($fp, 0);
    rewind($fp);
    fwrite($fp, json_encode($data, JSON_UNESCAPED_UNICODE));

    flock($fp, LOCK_UN);
    fclose($fp);

    return $allowed;
}

/**
 * フォーム入力値のバリデーションとサニタイズ
 *
 * @param  array $post $_POST 配列
 * @return array ['name' => string, 'email' => string, 'message' => string, 'error' => string]
 *               error が空文字ならバリデーション成功
 */
function validateInput(array $post): array
{
    $result = ['name' => '', 'email' => '', 'message' => '', 'error' => ''];

    // --- name ---
    $rawName = trim($post['name'] ?? '');
    if ($rawName === '') {
        $result['error'] = 'お名前を入力してください。';
        return $result;
    }
    if (mb_strlen($rawName, 'UTF-8') > 200) {
        $result['error'] = 'お名前は200文字以内で入力してください。';
        return $result;
    }
    // ヘッダーインジェクション対策：改行文字を除去
    $rawName = str_replace(["\r", "\n"], '', $rawName);

    // --- email ---
    $rawEmail = trim($post['email'] ?? '');
    if ($rawEmail === '') {
        $result['error'] = 'メールアドレスを入力してください。';
        return $result;
    }
    if (mb_strlen($rawEmail, 'UTF-8') > 255) {
        $result['error'] = 'メールアドレスは255文字以内で入力してください。';
        return $result;
    }
    if (filter_var($rawEmail, FILTER_VALIDATE_EMAIL) === false) {
        $result['error'] = '有効なメールアドレスを入力してください。';
        return $result;
    }
    // ヘッダーインジェクション対策：改行文字を除去
    $rawEmail = str_replace(["\r", "\n"], '', $rawEmail);

    // --- message ---
    $rawMessage = trim($post['message'] ?? '');
    if ($rawMessage === '') {
        $result['error'] = 'お問い合わせ内容を入力してください。';
        return $result;
    }
    if (mb_strlen($rawMessage, 'UTF-8') > 3000) {
        $result['error'] = 'お問い合わせ内容は3000文字以内で入力してください。';
        return $result;
    }

    // XSS 対策：htmlspecialchars でサニタイズ
    $result['name']    = htmlspecialchars($rawName,    ENT_QUOTES | ENT_HTML5, 'UTF-8');
    $result['email']   = htmlspecialchars($rawEmail,   ENT_QUOTES | ENT_HTML5, 'UTF-8');
    $result['message'] = htmlspecialchars($rawMessage, ENT_QUOTES | ENT_HTML5, 'UTF-8');
    $result['error']   = '';

    return $result;
}

/**
 * フォームログを TSV 形式でファイルに記録する
 *
 * @param string $status  ステータス種別（SUCCESS / HONEYPOT / RATE_LIMIT / VALIDATION_ERROR / MAIL_ERROR / MAIL_SKIPPED）
 * @param string $name    送信者名（サニタイズ済み）
 * @param string $email   メールアドレス（サニタイズ済み）
 * @param string $message メッセージ本文（先頭50文字のみ記録）
 * @param string $ip      クライアント IP アドレス
 */
function writeLog(
    string $status,
    string $name,
    string $email,
    string $message,
    string $ip = ''
): void {
    ensureLogDir();

    $datetime    = date('c');                                      // ISO 8601
    $ipLog       = $ip !== '' ? $ip : ($_SERVER['REMOTE_ADDR'] ?? 'unknown');
    // メッセージは先頭50文字のみ記録（改行をスペースに置換してTSVを壊さないようにする）
    $messagePart = mb_substr(str_replace(["\r\n", "\r", "\n", "\t"], [' ', ' ', ' ', ' '], $message), 0, 50, 'UTF-8');

    // TSV の各フィールドからタブ文字を除去
    $nameLog  = str_replace("\t", ' ', $name);
    $emailLog = str_replace("\t", ' ', $email);
    $uaLog    = str_replace("\t", ' ', $_SERVER['HTTP_USER_AGENT'] ?? '');

    $line = implode("\t", [
        $datetime,
        $ipLog,
        $status,
        $nameLog,
        $emailLog,
        $messagePart,
        $uaLog,
    ]) . PHP_EOL;

    file_put_contents(LOG_FILE, $line, FILE_APPEND | LOCK_EX);
}

/**
 * お問い合わせ内容をメールで送信する
 *
 * @param  string $name    送信者名（サニタイズ済み）
 * @param  string $email   返信先メールアドレス（サニタイズ済み）
 * @param  string $message お問い合わせ内容（サニタイズ済み）
 * @param  string $ip      クライアント IP アドレス
 * @return bool   送信成功なら true
 */
function sendMail(string $name, string $email, string $message, string $ip): bool
{
    $datetime = date('Y-m-d H:i:s T');

    // 件名
    $subject = mb_encode_mimeheader(
        '[' . SITE_NAME . '] お問い合わせ: ' . $name . '様より',
        'UTF-8',
        'B'
    );

    // 本文（テキスト形式）
    // htmlspecialchars_decode でメール本文に HTML エンティティが混入しないようにする
    $namePlain    = htmlspecialchars_decode($name,    ENT_QUOTES | ENT_HTML5);
    $emailPlain   = htmlspecialchars_decode($email,   ENT_QUOTES | ENT_HTML5);
    $messagePlain = htmlspecialchars_decode($message, ENT_QUOTES | ENT_HTML5);

    $body = SITE_NAME . " お問い合わせフォームより送信されました。\n"
          . "──────────────────────────\n"
          . "お名前: {$namePlain}\n"
          . "メールアドレス: {$emailPlain}\n"
          . "送信日時: {$datetime}\n"
          . "IP アドレス: {$ip}\n"
          . "──────────────────────────\n"
          . "お問い合わせ内容:\n\n"
          . "{$messagePlain}\n"
          . "──────────────────────────\n";

    // メールヘッダー
    // Reply-To にはサニタイズ済みの email を使用（改行はすでに除去済み）
    $headers = implode("\r\n", [
        'From: ' . MAIL_FROM,
        'Reply-To: ' . $emailPlain,
        'Content-Type: text/plain; charset=UTF-8',
        'X-Mailer: PHP/' . phpversion(),
    ]);

    return mail(MAIL_TO, $subject, $body, $headers);
}

/**
 * ログディレクトリが存在しない場合は作成する
 * パーミッションを 0750 に設定してブラウザからのアクセスを制限する
 */
function ensureLogDir(): void
{
    if (!is_dir(LOG_DIR)) {
        mkdir(LOG_DIR, 0750, true);

        // .htaccess でブラウザからのアクセスを禁止
        $htaccess = LOG_DIR . '.htaccess';
        if (!file_exists($htaccess)) {
            file_put_contents(
                $htaccess,
                "# ブラウザからの直接アクセスを禁止\nDeny from all\n"
            );
        }
    }
}
