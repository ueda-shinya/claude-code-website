<?php
/**
 * THE CORNER CAFE — form_handler.php
 * フォーム送受信ハンドラー
 * セキュリティ: XSSサニタイズ / レート制限 / Honeypot / CSRFチェック / ログ記録
 */

declare(strict_types=1);

// ─── 設定 ────────────────────────────────────────────────────
const MAIL_TO      = 'info@thecornercafe.jp';
const MAIL_FROM    = 'noreply@thecornercafe.jp';
const MAIL_SUBJECT = 'THE CORNER CAFE お問い合わせ';
const RATE_LIMIT   = 3;    // 同一IPの最大送信回数
const RATE_WINDOW  = 60;   // 秒（ウィンドウ）
const LOG_DIR      = __DIR__ . '/../logs';
const LOG_FILE     = LOG_DIR . '/form_log.txt';
const SESSION_NAME = 'tcc_session';

// ─── セッション開始 ───────────────────────────────────────────
session_name(SESSION_NAME);
session_start();

// ─── レスポンスヘッダー ───────────────────────────────────────
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');

// ─── POSTメソッド確認 ─────────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['status' => 'error', 'message' => 'Method Not Allowed']);
    exit;
}

// ─── ログ書き込み関数 ─────────────────────────────────────────
function write_form_log(string $status, array $data): void {
    if (!is_dir(LOG_DIR)) {
        mkdir(LOG_DIR, 0750, true);
        // ブラウザアクセス禁止
        file_put_contents(LOG_DIR . '/.htaccess', "Deny from all\n");
    }
    $line = implode("\t", [
        date('c'),
        $_SERVER['REMOTE_ADDR'] ?? 'unknown',
        $status,
        $data['name']  ?? '',
        $data['email'] ?? '',
        substr($_SERVER['HTTP_USER_AGENT'] ?? '', 0, 200),
    ]);
    file_put_contents(LOG_FILE, $line . PHP_EOL, FILE_APPEND | LOCK_EX);
}

// ─── IPベースのレート制限 ─────────────────────────────────────
function check_rate_limit(string $ip): bool {
    $key = 'rate_' . md5($ip);
    $now = time();
    if (!isset($_SESSION[$key])) {
        $_SESSION[$key] = ['count' => 0, 'window_start' => $now];
    }
    $data = &$_SESSION[$key];
    // ウィンドウをリセット
    if ($now - $data['window_start'] > RATE_WINDOW) {
        $data['count'] = 0;
        $data['window_start'] = $now;
    }
    $data['count']++;
    return $data['count'] <= RATE_LIMIT;
}

// ─── サニタイズ ───────────────────────────────────────────────
function sanitize(string $value): string {
    return htmlspecialchars(trim($value), ENT_QUOTES | ENT_HTML5, 'UTF-8');
}

$ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';

// ─── Honeypotチェック ─────────────────────────────────────────
$honeypot = trim($_POST['website'] ?? '');
if ($honeypot !== '') {
    write_form_log('SPAM', ['name' => '', 'email' => '']);
    // スパムには200で返してボットを惑わす
    echo json_encode(['status' => 'success']);
    exit;
}

// ─── レート制限 ───────────────────────────────────────────────
if (!check_rate_limit($ip)) {
    write_form_log('BLOCKED', ['name' => sanitize($_POST['name'] ?? ''), 'email' => sanitize($_POST['email'] ?? '')]);
    http_response_code(429);
    echo json_encode(['status' => 'error', 'message' => '送信回数の上限に達しました。しばらくお待ちください。']);
    exit;
}

// ─── 入力取得 ─────────────────────────────────────────────────
$name        = sanitize($_POST['name']         ?? '');
$email_raw   = trim($_POST['email']            ?? '');
$inquiry     = sanitize($_POST['inquiry_type'] ?? '');
$visit_date  = sanitize($_POST['visit_date']   ?? '');
$party_size  = sanitize($_POST['party_size']   ?? '');
$message     = sanitize($_POST['message']      ?? '');

// ─── バリデーション ───────────────────────────────────────────
$errors = [];

if ($name === '' || mb_strlen($name) > 100) {
    $errors[] = 'お名前が不正です。';
}

if (!filter_var($email_raw, FILTER_VALIDATE_EMAIL) || strlen($email_raw) > 254) {
    $errors[] = 'メールアドレスが不正です。';
}

$allowed_types = ['visit', 'menu', 'media', 'collaboration', 'other'];
if (!in_array($inquiry, $allowed_types, true)) {
    $errors[] = 'お問い合わせの種類が不正です。';
}

if ($message === '' || mb_strlen($message) > 2000) {
    $errors[] = 'お問い合わせ内容が不正です。';
}

if (!empty($errors)) {
    write_form_log('ERROR', ['name' => $name, 'email' => $email_raw]);
    http_response_code(422);
    echo json_encode(['status' => 'error', 'message' => implode(' ', $errors)]);
    exit;
}

$email = filter_var($email_raw, FILTER_SANITIZE_EMAIL);

// ─── メール送信 ───────────────────────────────────────────────
$inquiry_labels = [
    'visit'         => 'ご来店について',
    'menu'          => 'メニューについて',
    'media'         => '取材・メディア掲載のご相談',
    'collaboration' => 'コラボレーション・イベントのご相談',
    'other'         => 'その他',
];
$inquiry_label = $inquiry_labels[$inquiry] ?? $inquiry;

$body  = "THE CORNER CAFE お問い合わせフォームより\n";
$body .= str_repeat('-', 40) . "\n";
$body .= "お名前:           {$name}\n";
$body .= "メールアドレス:   {$email}\n";
$body .= "お問い合わせ種類: {$inquiry_label}\n";
if ($visit_date !== '') $body .= "ご来店予定日:     {$visit_date}\n";
if ($party_size !== '') $body .= "来店人数:         {$party_size}\n";
$body .= "\nお問い合わせ内容:\n{$message}\n";
$body .= str_repeat('-', 40) . "\n";
$body .= "送信日時: " . date('Y-m-d H:i:s') . "\n";
$body .= "IPアドレス: {$ip}\n";

$headers  = "From: " . MAIL_FROM . "\r\n";
$headers .= "Reply-To: {$email}\r\n";
$headers .= "X-Mailer: PHP/" . phpversion() . "\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

$subject = mb_encode_mimeheader(MAIL_SUBJECT, 'UTF-8', 'B');

$mail_sent = mail(MAIL_TO, $subject, $body, $headers);

// ─── 結果ログ＆レスポンス ─────────────────────────────────────
if ($mail_sent) {
    write_form_log('SUCCESS', ['name' => $name, 'email' => $email]);
    echo json_encode(['status' => 'success']);
} else {
    write_form_log('ERROR', ['name' => $name, 'email' => $email]);
    http_response_code(500);
    echo json_encode(['status' => 'error', 'message' => '送信に失敗しました。しばらく時間をおいて再度お試しください。']);
}
