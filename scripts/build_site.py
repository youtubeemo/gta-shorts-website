"""Baut die veröffentlichte Website nach _site/ und setzt die Pflichtangaben ein.

Die persönlichen Angaben stehen NICHT im Repository. Sie werden in GitHub hinterlegt:
Settings → Secrets and variables → Actions → Variables

  IMPRESSUM_NAME       Vor- und Nachname
  IMPRESSUM_STRASSE    Straße und Hausnummer
  IMPRESSUM_PLZ_ORT    PLZ und Ort
  KONTAKT_EMAIL        öffentliche Kontakt-E-Mail
  KANAL_URL            (optional) Link zum YouTube-Kanal, z. B. https://www.youtube.com/@…

Fehlt eine Pflichtangabe, bricht der Bau ab – es wird nie eine unvollständige Seite veröffentlicht.
"""
from __future__ import annotations

import html
import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
COPY = ["index.html", "datenschutz.html", "nutzungsbedingungen.html", "impressum.html", "404.html",
        "robots.txt", "sitemap.xml", ".nojekyll", "assets"]
REQUIRED = ["IMPRESSUM_NAME", "IMPRESSUM_STRASSE", "IMPRESSUM_PLZ_ORT", "KONTAKT_EMAIL"]
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober",
          "November", "Dezember"]


def env(name: str) -> str:
    return " ".join(os.environ.get(name, "").split())     # Zeilenumbrüche/Mehrfach-Leerzeichen glätten


def main() -> int:
    missing = [n for n in REQUIRED if not env(n)]
    if missing:
        print("::error::Pflichtangaben fehlen (GitHub → Settings → Secrets and variables → Actions → "
              f"Variables): {', '.join(missing)}. Es wird nichts veröffentlicht.")
        return 1
    email = env("KONTAKT_EMAIL")
    if not re.fullmatch(r"[^@\s<>\"']+@[^@\s<>\"']+\.[A-Za-z]{2,}", email):
        print("::error::KONTAKT_EMAIL sieht nicht wie eine E-Mail-Adresse aus.")
        return 1
    kanal = env("KANAL_URL")
    if kanal and not re.fullmatch(r"https://(www\.)?youtube\.com/[A-Za-z0-9@._/\-]+", kanal):
        print("::error::KANAL_URL muss mit https://www.youtube.com/ beginnen.")
        return 1
    stand = env("STAND") or f"{date.today().day}. {MONATE[date.today().month - 1]} {date.today().year}"
    values = {
        "NAME": html.escape(env("IMPRESSUM_NAME")),
        "ANSCHRIFT": f"{html.escape(env('IMPRESSUM_STRASSE'))}<br>\n      {html.escape(env('IMPRESSUM_PLZ_ORT'))}",
        "EMAIL": html.escape(email),
        "KANAL_URL": html.escape(kanal),
        "STAND": html.escape(stand),
    }
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for item in COPY:
        src = ROOT / item
        if src.is_dir():
            shutil.copytree(src, OUT / item)
        else:
            shutil.copy2(src, OUT / item)
    for page in OUT.glob("*.html"):
        text = page.read_text(encoding="utf-8")
        if not kanal:      # Zeile mit dem Kanal-Link entfernen, wenn keiner angegeben ist
            text = re.sub(r"\s*<p>YouTube: <a href=\"\{\{KANAL_URL\}\}\"[^\n]*</p>", "", text)
        for key, val in values.items():
            text = text.replace("{{" + key + "}}", val)
        page.write_text(text, encoding="utf-8")
    left = [p.name for p in OUT.glob("*.html") if re.search(r"\{\{[A-Z_]+\}\}", p.read_text(encoding="utf-8"))]
    if left:
        print(f"::error::Platzhalter nicht ersetzt in: {left}")
        return 1
    print(f"Website gebaut: {OUT} (Stand {stand})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
