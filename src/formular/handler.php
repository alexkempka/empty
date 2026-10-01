<?php
/**
 * ITCoreNet – Verarbeitung des Kontaktformulars.
 *
 * Wird von /de/kontakt/index.php und /en/contact/index.php eingebunden.
 * - Versand über PHP mail() und den Mailserver von IONOS
 * - Kein externer Dienst, kein CAPTCHA, keine Cookies
 * - Spam-Schutz: verstecktes Fallen-Feld, signierter Zeitstempel (Mindest-/Höchstdauer),
 *   Begrenzung auf 5 Nachrichten pro Stunde und IP-Adresse (IP nur als HMAC-Wert, max. 1 Stunde gespeichert)
 */
declare(strict_types=1);

const ITC_MIN_SECONDS = 3;      // schneller ausgefüllt = vermutlich Bot
const ITC_MAX_SECONDS = 7200;   // Formular höchstens 2 Stunden gültig
const ITC_RATE_LIMIT = 5;       // Nachrichten pro Stunde und IP-Adresse
const ITC_RATE_WINDOW = 3600;

function itc_h(?string $s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function itc_messages(string $lang): array
{
    $de = [
        'name' => 'Bitte geben Sie Ihren Namen ein.',
        'email' => 'Bitte geben Sie eine gültige E-Mail-Adresse ein.',
        'message' => 'Bitte geben Sie eine Nachricht ein.',
        'too_long' => 'Ihre Nachricht ist zu lang. Bitte kürzen Sie sie auf höchstens 5.000 Zeichen.',
        'field_long' => 'Diese Angabe ist zu lang.',
        'token' => 'Das Formular war zu lange geöffnet oder wurde zu schnell abgeschickt. Bitte senden Sie es noch einmal.',
        'rate' => 'Sie haben in kurzer Zeit mehrere Nachrichten gesendet. Bitte versuchen Sie es in einigen Minuten erneut.',
        'send' => 'Die Nachricht konnte nicht gesendet werden. Bitte versuchen Sie es später erneut oder schreiben Sie direkt an support@itcorenet.com.',
        'subject' => 'Kontaktanfrage über itcorenet.com',
        'thanks' => '/de/kontakt/danke/',
        'labels' => ['Name', 'Unternehmen', 'E-Mail', 'Nachricht'],
    ];
    $en = [
        'name' => 'Please enter your name.',
        'email' => 'Please enter a valid e-mail address.',
        'message' => 'Please enter a message.',
        'too_long' => 'Your message is too long. Please shorten it to a maximum of 5,000 characters.',
        'field_long' => 'This entry is too long.',
        'token' => 'The form was open for too long or was sent too quickly. Please send it again.',
        'rate' => 'You have sent several messages in a short time. Please try again in a few minutes.',
        'send' => 'Your message could not be sent. Please try again later or write directly to support@itcorenet.com.',
        'subject' => 'Contact enquiry via itcorenet.com',
        'thanks' => '/en/contact/thank-you/',
        'labels' => ['Name', 'Company', 'E-mail', 'Message'],
    ];
    return $lang === 'en' ? $en : $de;
}

function itc_clean(string $s, bool $multiline = false): string
{
    $s = str_replace("\r\n", "\n", $s);
    // Steuerzeichen entfernen (Zeilenumbrüche nur im Nachrichtenfeld erlaubt)
    $s = (string) preg_replace($multiline ? '/[\x00-\x09\x0B-\x1F\x7F]/u' : '/[\x00-\x1F\x7F]/u', '', $s);
    return trim($s);
}

function itc_len(string $s): int
{
    return function_exists('mb_strlen') ? mb_strlen($s, 'UTF-8') : strlen($s);
}

function itc_token(string $lang, string $secret): array
{
    $ts = (string) time();
    return ['ts' => $ts, 'sig' => hash_hmac('sha256', $ts . '|' . $lang, $secret)];
}

/** true = Anfrage erlaubt; zählt sie gleichzeitig mit. */
function itc_rate_ok(string $secret): bool
{
    $dir = __DIR__ . '/daten';
    if (!is_dir($dir) && !@mkdir($dir, 0750, true)) {
        return true; // ohne Speicherort keine Begrenzung, Formular soll trotzdem funktionieren
    }
    if (!is_file($dir . '/.htaccess')) {
        @file_put_contents($dir . '/.htaccess', "Require all denied\n");
    }
    $fh = @fopen($dir . '/rate.json', 'c+');
    if ($fh === false) {
        return true;
    }
    flock($fh, LOCK_EX);
    $raw = stream_get_contents($fh);
    $data = json_decode($raw ?: '{}', true);
    if (!is_array($data)) {
        $data = [];
    }
    $now = time();
    foreach ($data as $k => $times) {
        $data[$k] = array_values(array_filter((array) $times, fn($t) => is_int($t) && $t > $now - ITC_RATE_WINDOW));
        if (!$data[$k]) {
            unset($data[$k]);
        }
    }
    $key = hash_hmac('sha256', (string) ($_SERVER['REMOTE_ADDR'] ?? ''), $secret);
    $ok = count($data[$key] ?? []) < ITC_RATE_LIMIT;
    if ($ok) {
        $data[$key][] = $now;
    }
    ftruncate($fh, 0);
    rewind($fh);
    fwrite($fh, json_encode($data));
    fflush($fh);
    flock($fh, LOCK_UN);
    fclose($fh);
    return $ok;
}

function itc_contact_form(string $lang): array
{
    $msg = itc_messages($lang);
    $configFile = __DIR__ . '/config.php';
    $config = is_file($configFile) ? require $configFile : null;
    $secret = is_array($config) ? (string) ($config['secret'] ?? '') : '';

    $form = ['values' => ['name' => '', 'company' => '', 'email' => '', 'message' => ''],
             'errors' => [], 'general' => '', 'token' => ['ts' => '', 'sig' => '']];

    if (strlen($secret) < 32) {
        $form['general'] = $msg['send'];
        error_log('ITCoreNet-Kontaktformular: config.php fehlt oder Geheimschlüssel zu kurz.');
        return $form;
    }

    if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'POST') {
        $form['token'] = itc_token($lang, $secret);
        return $form;
    }

    $v = [
        'name' => itc_clean((string) ($_POST['name'] ?? '')),
        'company' => itc_clean((string) ($_POST['company'] ?? '')),
        'email' => itc_clean((string) ($_POST['email'] ?? '')),
        'message' => itc_clean((string) ($_POST['message'] ?? ''), true),
    ];
    $form['values'] = $v;
    $form['token'] = itc_token($lang, $secret);

    // Fallen-Feld: Menschen sehen es nicht. Ausgefüllt = Bot -> so tun, als ob alles geklappt hat.
    if (trim((string) ($_POST['website'] ?? '')) !== '') {
        header('Location: ' . $msg['thanks'], true, 303);
        exit;
    }

    $ts = (string) ($_POST['ts'] ?? '');
    $sig = (string) ($_POST['sig'] ?? '');
    $age = ctype_digit($ts) ? time() - (int) $ts : -1;
    if (!hash_equals(hash_hmac('sha256', $ts . '|' . $lang, $secret), $sig)
        || $age < ITC_MIN_SECONDS || $age > ITC_MAX_SECONDS) {
        $form['general'] = $msg['token'];
        return $form;
    }

    if ($v['name'] === '') {
        $form['errors']['name'] = $msg['name'];
    } elseif (itc_len($v['name']) > 100) {
        $form['errors']['name'] = $msg['field_long'];
    }
    if (itc_len($v['company']) > 150) {
        $form['errors']['company'] = $msg['field_long'];
    }
    if ($v['email'] === '' || itc_len($v['email']) > 254 || filter_var($v['email'], FILTER_VALIDATE_EMAIL) === false) {
        $form['errors']['email'] = $msg['email'];
    }
    if ($v['message'] === '') {
        $form['errors']['message'] = $msg['message'];
    } elseif (itc_len($v['message']) > 5000) {
        $form['errors']['message'] = $msg['too_long'];
    }
    if ($form['errors']) {
        return $form;
    }

    if (!itc_rate_ok($secret)) {
        $form['general'] = $msg['rate'];
        return $form;
    }

    $to = (string) $config['to'];
    $from = (string) $config['from'];
    [$lName, $lCompany, $lEmail, $lMessage] = $msg['labels'];
    $body = "{$lName}: {$v['name']}\n"
        . "{$lCompany}: " . ($v['company'] !== '' ? $v['company'] : '–') . "\n"
        . "{$lEmail}: {$v['email']}\n"
        . 'Sprache / Language: ' . strtoupper($lang) . "\n\n"
        . "{$lMessage}:\n{$v['message']}\n";
    $subject = function_exists('mb_encode_mimeheader')
        ? mb_encode_mimeheader($msg['subject'], 'UTF-8', 'B')
        : $msg['subject'];
    // E-Mail-Adresse ist validiert und enthält keine Zeilenumbrüche (Schutz vor Header-Injection).
    $headers = [
        'From' => 'ITCoreNet Website <' . $from . '>',
        'Reply-To' => $v['email'],
        'MIME-Version' => '1.0',
        'Content-Type' => 'text/plain; charset=UTF-8',
        'Content-Transfer-Encoding' => '8bit',
    ];
    $sent = @mail($to, $subject, $body, $headers, '-f' . $from);
    if (!$sent) {
        error_log('ITCoreNet-Kontaktformular: mail() fehlgeschlagen.');
        $form['general'] = $msg['send'];
        return $form;
    }
    header('Location: ' . $msg['thanks'], true, 303);
    exit;
}
