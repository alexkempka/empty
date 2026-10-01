<?php
/**
 * Vorlage für die Konfiguration des Kontaktformulars.
 *
 * Auf dem Server als "config.php" (gleicher Ordner) anlegen. config.php wird NIE ins Repository
 * eingecheckt (.gitignore) und ist per .htaccess vor Abruf aus dem Internet geschützt.
 *
 * Geheimschlüssel erzeugen, z. B.:  php -r 'echo bin2hex(random_bytes(32)), PHP_EOL;'
 */
return [
    'to' => 'support@itcorenet.com',     // Empfänger der Anfragen
    'from' => 'support@itcorenet.com',   // Absender (muss ein Postfach der eigenen Domain sein)
    'secret' => 'HIER-64-ZEICHEN-ZUFALLSWERT-EINTRAGEN',
];
