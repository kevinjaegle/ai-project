# AI Project (Production-Grade Skeleton)

## Ziel
- Saubere Struktur (API + ML)
- Reproduzierbarer Start (requirements, venv)
- Health-Check-Endpunkt

## Quickstart
1) Python-Env aktivieren: `.venv\Scripts\Activate`
2) Pakete: `pip install -r requirements.txt`
3) Start: `uvicorn src.app.main:app --reload --port 8000`
4) Test: Browser `http://127.0.0.1:8000/health`
