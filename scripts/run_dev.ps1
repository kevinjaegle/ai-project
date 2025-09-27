# scripts/run_dev.ps1
# Aktiviert venv (wenn nicht aktiv) und startet den Server im Dev-Modus

if (-not $env:VIRTUAL_ENV) {
    ..\.venv\Scripts\Activate
}
uvicorn src.app.main:app --reload --host 127.0.0.1 --port 8000