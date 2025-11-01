# Production‑Grade AI App (FastAPI • scikit‑learn • Docker)

**Kurzfassung:**
Eine kleine, saubere KI‑Anwendung von 0 → produktionsreif: Daten vorbereiten, Modell trainieren (scikit‑learn), über eine FastAPI bereitstellen, mit Tests, Logging, `.env`‑Konfiguration und Docker‑Image. Ideal zum Vorzeigen für Arbeitgeber (Code‑Qualität, Struktur, DevOps‑Basics).

---

## 🔥 Highlights (für Leser & Arbeitgeber)

* **Klare Projektstruktur:** Trennung von API (`src/app`) und ML‑Code (`src/ml`).
* **Production‑Basics:** Health‑Check, Eingabe‑Validierung (Pydantic), Logging, `.env`‑Konfiguration.
* **Qualität:** Pytest‑Tests (z. B. `/health`, `/predict`).
* **Portabilität:** Dockerfile, läuft lokal & bei Hostern (Render/Railway) → `${PORT}` wird unterstützt.
* **Nachvollziehbarkeit:** Minimaler, gut kommentierter Code – leicht erweiterbar.

---

## 🧭 Projektstruktur

```text
.
├─ .dockerignore
├─ .gitignore
├─ .env.example
├─ Dockerfile
├─ README.md
├─ requirements.txt
├─ scripts/
│  └─ run_dev.ps1
└─ src/
   ├─ app/
   │  ├─ __init__.py
   │  └─ main.py          # FastAPI: /health, /predict, Logging, .env
   ├─ ml/
   │  ├─ __init__.py
   │  ├─ data_prep.py     # (Beispiel) Daten laden/teilen
   │  └─ train.py         # Modell trainieren → model.joblib
   └─ tests/
      ├─ test_health.py
      └─ test_predict.py
```

---

## 🚀 Schnellstart (lokal)

**Voraussetzungen:** Python 3.10+, pip, (optional) Docker.

```powershell
# 1) Repository klonen
# git clone <dein-repo>
cd <dein-repo>

# 2) Virtuelle Umgebung & Pakete
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt

# 3) (Optional) Daten vorbereiten
# python src/ml/data_prep.py          # erzeugt train.csv/test.csv
# # oder in Python:
# # from src.ml import data_prep
# # data_prep.run()

# 4) Modell trainieren
python src/ml/train.py               # erzeugt model.joblib
# # oder in Python:
# # from src.ml import train
# # train.run()

# 5) API starten (Entwicklung)
uvicorn src.app.main:app --reload --port 8000
# → http://127.0.0.1:8000/health
```

**Gesundheitscheck:**

```text
GET /health  →  {"status":"ok","model_loaded":true,"error":null}
```

---

## 📡 API – Endpunkte

### `GET /health`

* **Zweck:** Läuft der Dienst? Ist das Modell geladen?
* **Antwort (Beispiel):**

  ```json
  { "status": "ok", "model_loaded": true, "error": null }
  ```

### `POST /predict`

* **Body (Beispiel):**

  ```json
  { "feature1": 1.2, "feature2": 3.4 }
  ```
* **Antwort (Beispiel):**

  ```json
  { "prediction": 1 }
  ```
* **Hinweis:** Passe die Felder (`feature1`, `feature2`, …) an **deine Trainingsspalten** an. Namen/Typen müssen 1:1 zu `train.py` passen.

**Schnelltest (PowerShell/curl):**

```powershell
curl -X POST "http://127.0.0.1:8000/predict" `
  -H "Content-Type: application/json" `
  -d "{""feature1"": 1.2, ""feature2"": 3.4}"
```

---

## ⚙️ Konfiguration (.env)

Beispiel: `.env.example`

```ini
APP_PORT=8000
ENV=development
LOG_LEVEL=INFO
MODEL_PATH=model.joblib
```

> Kopiere zu `.env` und passe nach Bedarf an. **Hinweis:** `.env` wird nicht eingecheckt.

---

## 🧪 Tests

```powershell
pip install pytest
pytest -q
```

* `test_health.py`: Erwartet HTTP 200 und `{ "status": "ok" }`.
* `test_predict.py`: Erwartet 200 + `prediction` (wenn `model.joblib` existiert), sonst 503.

---

## 📜 Logging

* Konfiguriert via `logging.basicConfig` und `LOG_LEVEL` (z. B. `DEBUG`, `INFO`).
* Beispiel‑Logereignisse: App‑Start, Modell geladen/nicht gefunden, Anfragen an `/predict`, Fehler mit Stacktrace.

---

## 📦 Docker

**Einfaches Image bauen & starten:**

```powershell
docker build -t ai-app:latest .
docker run --rm -p 8000:8000 --name ai-app ai-app:latest
# → http://127.0.0.1:8000/health
```

**Dockerfile (Startbefehl mit Host‑Port):**

```dockerfile
CMD ["sh", "-c", "uvicorn src.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

> Hoster übergeben `PORT` (z. B. 10000). Lokal bleibt 8000 Standard.

---

## ☁️ Deployment (kurz)

* **Render/Railway**: Neues Web‑Service erstellen → Repo verbinden → Docker verwenden → `HealthCheck: /health` → Env‑Variablen setzen (`MODEL_PATH`, `LOG_LEVEL`, …) → Deploy.
* **Wichtig:** Achte darauf, dass `model.joblib` im Image landet (nicht von `.dockerignore` ausgeschlossen).

---

## 🔧 Technischer Stack

* **Backend:** FastAPI, Uvicorn
* **ML:** scikit‑learn, pandas, joblib
* **Qualität:** pytest, Pydantic (Validierung)
* **Konfig:** python‑dotenv (`.env`)
* **Container:** Docker (Multi‑Stage optional)

---

## 🧱 Design‑Entscheidungen (kurz)

* **Trennung von Belangen:** API ≠ ML‑Training → klare Verantwortlichkeiten.
* **Validierung am Rand:** Pydantic‐Modelle schützen das Modell vor fehlerhaften Eingaben.
* **„Fail fast“:** Startup prüft Modellpfad; `/health` zeigt Diagnose.
* **12‑Factor‑Style:** Config via Env; keine Secrets im Code/Repo.

---

## 🗺️ Roadmap (Ideen)

* Mehr Features/Eingaben + Modell‑Versionierung (`MODEL_VERSION`).
* Metriken/Monitoring (z. B. `/metrics`, Prometheus).
* CI/CD (GitHub Actions: Tests + Docker Build + Auto‑Deploy).
* Caching/Batch‑Predict.
* Input‑Schema‑Dokumentation mit Beispielen (OpenAPI/Swagger‑Erweiterungen).

---

## ❓ FAQ / Troubleshooting

* **`/predict` liefert 503 („Modell nicht geladen“) …**

  * `model.joblib` existiert? Name/Pfad mit `MODEL_PATH` korrekt? Nicht in `.dockerignore`?
* **`KeyError: 'feature1'`**

  * Spaltennamen beim Training (`train.py`) und beim Request identisch halten.
* **Port/502‑Probleme beim Hoster**

  * CMD nutzt `${PORT:-8000}`? Health‑Pfad `/health` gesetzt?
* **Zu wenig Logs**

  * `LOG_LEVEL=DEBUG` in Env setzen.

---

## 🙌 Dank & Quellen

* Dieses Projekt orientiert sich an einem praxisnahen „Production‑Grade AI“‑Tutorial (Struktur/Ideen). Code & Struktur sind allgemein gehalten und können frei angepasst/erweitert werden.

---

> Pull Requests & Feedback sind willkommen! 😊
