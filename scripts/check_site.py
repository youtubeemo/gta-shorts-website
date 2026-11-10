"""Prüft die Website: Platzhalter, interne Links + Anker, externe Links und (optional) die Live-Seite per HTTPS.

Aufruf:  python scripts/check_site.py                 # nur Dateien + externe Links
         python scripts/check_site.py --live          # zusätzlich https://youtubeemo.github.io/gta-shorts-website/
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://youtubeemo.github.io/gta-shorts-website/"
PAGES = ["index.html", "datenschutz.html", "nutzungsbedingungen.html", "impressum.html", "404.html"]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.links.append(a[key])
        if a.get("srcset"):
            self.links += [p.strip().split(" ")[0] for p in a["srcset"].split(",")]


def parse(page: Path) -> Links:
    p = Links()
    p.feed(page.read_text(encoding="utf-8"))
    return p


def fetch(url: str) -> int:
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "Mozilla/5.0 (Link-Pruefung)"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except (urllib.error.URLError, OSError):
        return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--allow-placeholders", action="store_true")
    ap.add_argument("--offline", action="store_true", help="externe Links nicht abrufen")
    args = ap.parse_args()
    errors, external = [], set()
    parsed = {p: parse(ROOT / p) for p in PAGES}
    for name, p in parsed.items():
        text = (ROOT / name).read_text(encoding="utf-8")
        if not args.allow_placeholders and re.search(r"\{\{[A-Z_]+\}\}", text):
            errors.append(f"{name}: enthält noch Platzhalter {sorted(set(re.findall(r'{{[A-Z_]+}}', text)))}")
        for link in p.links:
            if link.startswith(("mailto:", "{{")):
                continue
            if link.startswith("http://"):
                errors.append(f"{name}: unverschlüsselter Link {link}")
            elif link.startswith("https://"):
                if not link.startswith(BASE):
                    external.add(link)
            else:
                target, _, anchor = link.partition("#")
                if target.startswith("/gta-shorts-website/"):
                    target = target[len("/gta-shorts-website/"):]
                target = target or (name if link.startswith("#") else "index.html")
                if target in ("./", ""):
                    target = "index.html"
                path = ROOT / target
                if not path.exists():
                    errors.append(f"{name}: Ziel fehlt {link}")
                elif anchor and target.endswith(".html") and anchor not in parse(path).ids:
                    errors.append(f"{name}: Anker fehlt {link}")
    for url in sorted(external) if not args.offline else []:
        code = fetch(url)
        ok = 0 < code < 400 or code in (403, 429)          # manche Seiten blocken Bots – kein toter Link
        print(("✅" if ok else "❌"), code, url)
        if not ok:
            errors.append(f"externer Link nicht erreichbar ({code}): {url}")
    if args.live:
        for page in ["", "datenschutz.html", "nutzungsbedingungen.html", "impressum.html"]:
            code = fetch(BASE + page)
            print(("✅" if code == 200 else "❌"), code, BASE + page)
            if code != 200:
                errors.append(f"Live-Seite nicht erreichbar ({code}): {BASE + page}")
    for e in errors:
        print("❌", e)
    print("Ergebnis:", "OK" if not errors else f"{len(errors)} Fehler")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
