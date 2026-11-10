# GTA-Shorts.Germany – Website

Öffentliche Homepage für den YouTube-Kanal GTA-Shorts.Germany und die private Anwendung
„GTA-Shorts Upload“ (Google OAuth 2.0 / YouTube Data API).

- Start: https://youtubeemo.github.io/gta-shorts-website/
- Datenschutzerklärung: https://youtubeemo.github.io/gta-shorts-website/datenschutz.html
- Nutzungsbedingungen: https://youtubeemo.github.io/gta-shorts-website/nutzungsbedingungen.html
- Impressum & Kontakt: https://youtubeemo.github.io/gta-shorts-website/impressum.html

Statisches HTML/CSS, gehostet mit GitHub Pages (kostenlos, HTTPS). Keine Cookies, keine Tracker,
keine externen Schriften. Schrift „Anton“ unter SIL Open Font License (`assets/fonts/OFL-Anton.txt`).

## Veröffentlichung

Workflow **„Website veröffentlichen“** (`.github/workflows/pages.yml`) baut die Seite, setzt die Pflichtangaben
ein, prüft alle Links und veröffentlicht über GitHub Pages (HTTPS). Danach wird die Live-Seite geprüft.

Einmalige Einstellungen:
1. **Settings → Pages → Build and deployment → Source: „GitHub Actions“**
2. **Settings → Secrets and variables → Actions → Variables** – Pflichtangaben für Impressum/Datenschutz
   (stehen bewusst NICHT im Repository):
   `IMPRESSUM_NAME`, `IMPRESSUM_STRASSE`, `IMPRESSUM_PLZ_ORT`, `KONTAKT_EMAIL`, optional `KANAL_URL`

Fehlt eine Pflichtangabe, wird nichts veröffentlicht.

Inoffizielles Fan-Projekt – keine Verbindung zu Rockstar Games, Take-Two Interactive, Google oder YouTube.
