# gta-shorts-website – Regeln für KI-Agenten

Statische Website für GTA-Shorts.Germany auf GitHub Pages (HTML/CSS, keine Cookies, keine Tracker, keine externen Schriften).

- Datenschutz, Impressum und Nutzungsbedingungen sind rechtlich relevant: nur auf ausdrücklichen Wunsch inhaltlich ändern.
- Keine externen Skripte, Fonts oder Tracker einbinden.

<!-- agent-rules:start v1.0.0 — zentral gepflegt in claude-config, nicht hier von Hand ändern -->
## Kosten und Sicherheit (gilt für jeden KI-Agenten)

- Keine kostenpflichtigen API-Aufrufe oder -Tests ohne ausdrückliche Freigabe im Chat. Nur kostenlose Prüfungen (lokale Tests, Lint, Trockenläufe).
- Keine Zahlungen, Guthabenaufladungen, Abonnements, Testphasen mit Zahlungsmittel.
- API-Schlüssel, Secrets, Budgets und Produktionsgrenzen nicht ändern. `.env` niemals committen.
- Keine Secrets, Kundendaten oder personenbezogenen Daten an fremde Dienste senden.
- Keine ungeprüften Installationsskripte ausführen (`curl … | sh`, `npx <paket>@latest` u. ä.).
- Laufende Produktions-Workflows (GitHub Actions, Zeitpläne, Uploads) nicht unterbrechen, deaktivieren oder auslösen, außer auf ausdrücklichen Wunsch.
- Änderungen über einen eigenen Branch und Pull Request, nicht direkt auf `main`.
<!-- agent-rules:end -->
