<?php
declare(strict_types=1);

// ============================================================
// 設定
// ============================================================
define('MAIL_TO',            'info@thecornercafe.jp');
define('MAIL_FROM',          'noreply@thecornercafe.jp');
define('MAIL_SUBJECT_PREFIX', '[THE CORNER CAFE] お問い合わせ: ');
define('RATE_LIMIT_COUNT',   3);    // 同一IPの最大送信回数
define('RATE_LIMIT_WINDOW',  60);   // レート制限ウィンドウ（秒）
define('LOG_DIR',            __DIR__ . '/../logs');
define('RATE_LIMIT_FILE',    LOG_DIR . '/rate_limit.json');
define('LOG_FILE',           LOG_DIR . '/form_log.txt');

// ============================================================
// ヘッダー
// ============================================================
header('Content-Type: application/json; charset=UTF-8');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');

// ============================================================
// ユーティリティ
// ============================================================

/**
 * フォームログを書き込む
 */
function write_form_log(string $status, string $name = '', string $email = ''): void {
    if (!is_dir(LOG_DIR)) {
        mkdir(LOG_DIR, 0750, true);
    }
    $ip   = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    $ua   = $_SERVER['HTTP_USER_AGENT'] ?? '';
    $line = implode("\t", [
        date('c'),
        $ip,
        $status,
        $name,
        $email,
        $ua,
    ]);
    file_put_contents(LOG_FILE, $line . PHP_EOL, FILE_APPEND | LOCK_EX);
}

/**
 * JSONレスポンスを返して終了
 */
function respond(bool $success, string $message): never {
    echo json_encode(
        ['success' => $success, 'message' => $message],
        JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR
    );
    exit;
}

/**
 * 文字列をサニタイズ（XSS防止）
 */
function sanitize(string $value): string {
    return htmlspecialchars(trim($value), ENT_QUOTES | ENT_HTML5, 'UTF-8');
}

/**
 * IPベースのレート制限チェック
 * 同一IPからRATE_LIMIT_WINDOW秒以内にRATE_LIMIT_COUNT回以上の送信をブロック
 */
function check_rate_limit(): bool {
    $ip  = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    $now = time();

    if (!is_dir(LOG_DIR)) {
        mkdir(LOG_DIR, 0750, true);
    }

    $data = [];
    if (file_exists(RATE_LIMIT_FILE)) {
        $content = file_get_contents(RATE_LIMIT_FILE);
        if ($content !== false) {
            $data = json_decode($content, true) ?? [];
        }
    }

    // 期限切れのエントリを削除
    if (isset($data[$ip])) {
        $data[$ip] = array_values(array_filter($data[$ip], function ($timestamp) use ($now) {
            return ($now - $timestamp) < RATE_LIMIT_WINDOW;
        }));
    }

    // 現在のカウント確認
    $count = count($data[$ip] ?? []);
    if ($count >= RATE_LIMIT_COUNT) {
        return false; // レート制限に引っかかった
    }

    // タイムスタンプを追加
    $data[$ip][] = $now;
    file_put_contents(RATE_LIMIT_FILE, json_encode($data, JSON_THROW_ON_ERROR), LOCK_EX);
    return true;
}

// ============================================================
// メインロジック
// ============================================================

// POSTメソッドのみ許可
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    write_form_log('ERROR', '', '');
    respond(false, '不正なリクエストです。');
}

// Honeypot チェック（botが入力する罠フィールド）
$honeypot = $_POST['website'] ?? '';
if (!empty($honeypot)) {
    write_form_log('SPAM', '', '');
    // botには成功レスポンスを返す（検知を悟らせない）
    respond(true, 'お問い合わせを受け付けました。');
}

// レート制限チェック
if (!check_rate_limit()) {
    write_form_log('BLOCKED', '', '');
    respond(false, 'しばらく時間をおいてから再度お試しください。');
}

// ============================================================
// バリデーション
// ============================================================
$errors = [];

// お名前
$name_raw = $_POST['name'] ?? '';
$name     = sanitize($name_raw);
if (empty($name)) {
    $errors[] = 'お名前を入力してください。';
} elseif (mb_strlen($name_raw, 'UTF-8') > 50) {
    $errors[] = 'お名前は50文字以内で入力してください。';
}

// メールアドレス
$email_raw = $_POST['email'] ?? '';
$email     = sanitize($email_raw);
if (empty($email)) {
    $errors[] = 'メールアドレスを入力してください。';
} elseif (strlen($email_raw) > 254 || !filter_var($email_raw, FILTER_VALIDATE_EMAIL)) {
    $errors[] = '正しいメールアドレスを入力してください。';
}

// 電話番号（任意）
$tel_raw = $_POST['tel'] ?? '';
$tel     = sanitize($tel_raw);
if (!empty($tel_raw) && !preg_match('/^[\d\-+\s()]+$/', $tel_raw)) {
    $errors[] = '電話番号の形式が正しくありません。';
}

// お問い合わせの種類
$inquiry_type_raw = $_POST['inquiry_type'] ?? '';
$allowed_types    = ['visit', 'private', 'gift', 'other'];
$inquiry_type     = in_array($inquiry_type_raw, $allowed_types, true) ? $inquiry_type_raw : '';
if (empty($inquiry_type)) {
    $errors[] = 'お問い合わせの種類を選択してください。';
}

$inquiry_labels = [
    'visit'   => '来店・予約について',
    'private' => '貸切・団体利用について',
    'gift'    => 'ギフト・テイクアウトについて',
    'other'   => 'その他',
];
$inquiry_label = $inquiry_labels[$inquiry_type] ?? $inquiry_type;

// メッセージ
$message_raw = $_POST['message'] ?? '';
$message     = sanitize($message_raw);
if (empty($message)) {
    $errors[] = 'メッセージを入力してください。';
} elseif (mb_strlen($message_raw, 'UTF-8') > 1000) {
    $errors[] = 'メッセージは1000文字以内で入力してください。';
}

// プライバシー同意
$privacy = $_POST['privacy'] ?? '';
if (empty($privacy)) {
    $errors[] = 'プライバシーポリシーへの同意が必要です。';
}

// バリデーションエラーがある場合
if (!empty($errors)) {
    write_form_log('ERROR', $name, $email);
    respond(false, implode(' ', $errors));
}

// ============================================================
// メール送信
// ============================================================

// ヘッダーインジェクション対策: \r\n を除去
$email_safe = str_replace(["\r", "\n"], '', $email);
$name_safe  = str_replace(["\r", "\n"], '', $name);
$subject    = MAIL_SUBJECT_PREFIX . $inquiry_label;

// 送信時刻とIPを先に取得
$now_str   = date('Y-m-d H:i:s');
$client_ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';

$mail_body = <<<EOT
THE CORNER CAFE お問い合わせフォームより受信しました。

■ お名前
{$name}

■ メールアドレス
{$email}

■ 電話番号
{$tel}

■ お問い合わせの種類
{$inquiry_label}

■ メッセージ
{$message}

----
送信日時: {$now_str}
IPアドレス: {$client_ip}
EOT;

$headers  = "From: " . MAIL_FROM . "\r\n";
$headers .= "Reply-To: {$email_safe}\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "Content-Transfer-Encoding: 8bit\r\n";
$headers .= "X-Mailer: PHP/" . phpversion() . "\r\n";

$mail_result = mail(MAIL_TO, $subject, $mail_body, $headers);

if ($mail_result) {
    write_form_log('SUCCESS', $name, $email);
    respond(true, 'お問い合わせを受け付けました。');
} else {
    write_form_log('ERROR', $name, $email);
    respond(false, 'メール送信に失敗しました。お電話でお問い合わせください。');
}
