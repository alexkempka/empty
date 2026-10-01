<?php
/**
 * OPTIONAL: Abweichende Einstellungen für das Kontaktformular.
 *
 * Ohne diese Datei gilt: Empfänger und Absender = support@itcorenet.com,
 * der geheime Schlüssel wird beim ersten Aufruf automatisch erzeugt (formular/daten/schluessel.php).
 * Nur wenn etwas abweichen soll, diese Datei als "config.php" im selben Ordner anlegen.
 * config.php wird nie ins Repository eingecheckt und ist per .htaccess gesperrt.
 */
return [
    'to' => 'support@itcorenet.com',     // Empfänger der Anfragen
    'from' => 'support@itcorenet.com',   // Absender (muss ein Postfach der eigenen Domain sein)
];
