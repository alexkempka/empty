#!/bin/sh
# Prüft Weiterleitungen, Zugriffssperren und Sicherheits-Header gegen einen LOKALEN Apache-Testserver.
# Alle Anfragen gehen ausschließlich an 127.0.0.1 (nie an die Live-Website).
HTTP=127.0.0.1:8080; HTTPS_PORT=8443; CA=/etc/apache2/itc/cert.pem
req() { # Schema Host Pfad
  if [ "$1" = https ]; then
    curl -sS --noproxy '*' --max-time 10 --cacert "$CA" --resolve "$2:$HTTPS_PORT:127.0.0.1" -o /dev/null -w "%{http_code} %{redirect_url}" "https://$2:$HTTPS_PORT$3"
  else
    curl -sS --noproxy '*' --max-time 10 -H "Host: $2" -o /dev/null -w "%{http_code} %{redirect_url}" "http://$HTTP$3"
  fi
}
check() { # Schema Host Pfad Erwartung
  got=$(req "$1" "$2" "$3"); case "$got" in "$4"*) s=OK;; *) s=FEHLER;; esac
  printf "%-7s %-6s %-18s %-30s → %s\n" "$s" "$1" "$2" "$3" "$got"
}
check http  www.itcorenet.com /                       "301 https://www.itcorenet.com/"
check http  itcorenet.com     /de/                    "301 https://www.itcorenet.com/de/"
check https itcorenet.com     /de/                    "301 https://www.itcorenet.com/de/"
check https www.itcorenet.de  /irgendwas              "301 https://www.itcorenet.com/de/"
check http  itcorenet.de      /                       "301 https://www.itcorenet.com/de/"
check https www.itcorenet.com /                       "301 https://www.itcorenet.com:$HTTPS_PORT/de/"
check https www.itcorenet.com /index.html             "301 https://www.itcorenet.com:$HTTPS_PORT/en/"
check https www.itcorenet.com /de/                    "200"
check https www.itcorenet.com /en/contact/            "200"
check https www.itcorenet.com /de/leistungen          "301"
check https www.itcorenet.com /gibtsnicht             "404"
check https www.itcorenet.com /formular/handler.php   "403"
check https www.itcorenet.com /formular/config.php    "403"
check https www.itcorenet.com /formular/daten/rate.json "403"
check https www.itcorenet.com /.htaccess              "403"
check https www.itcorenet.com /assets/                "403"
check https www.itcorenet.com /sitemap.xml            "200"
check https www.itcorenet.com /robots.txt             "200"
echo "--- Header /de/:"
curl -sS --noproxy '*' --max-time 10 --cacert "$CA" --resolve "www.itcorenet.com:$HTTPS_PORT:127.0.0.1" -H "Accept-Encoding: gzip" -D - -o /dev/null "https://www.itcorenet.com:$HTTPS_PORT/de/" | grep -iE "^(strict|content-security|x-|referrer|permissions|cross|cache|content-encoding|set-cookie)"
echo "--- Header Kontaktseite (PHP):"
curl -sS --noproxy '*' --max-time 10 --cacert "$CA" --resolve "www.itcorenet.com:$HTTPS_PORT:127.0.0.1" -D - -o /dev/null "https://www.itcorenet.com:$HTTPS_PORT/de/kontakt/" | grep -iE "^(set-cookie|x-powered|cache|content-security)"
echo "--- Header CSS:"
curl -sS --noproxy '*' --max-time 10 --cacert "$CA" --resolve "www.itcorenet.com:$HTTPS_PORT:127.0.0.1" -H "Accept-Encoding: gzip" -D - -o /dev/null "https://www.itcorenet.com:$HTTPS_PORT/assets/css/style.css" | grep -iE "^(cache|content-encoding)"
