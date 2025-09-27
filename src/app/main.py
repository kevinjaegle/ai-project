# src/app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
import joblib
import pandas as pd
import logging
from dotenv import load_dotenv

# ---------- .env laden ----------
load_dotenv()

# ---------- Logging konfigurieren ----------
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("app")

app = FastAPI()

# Port/Model aus .env (mit Defaults)
APP_PORT = int(os.getenv("APP_PORT", "8000"))
MODEL_PATH = os.getenv("MODEL_PATH", "model.joblib")

# ---------- Eingabe-Schema ----------
class PredictRequest(BaseModel):
    feature1: float = Field(..., description="Erstes Merkmal, z. B. Zahl")
    feature2: float = Field(..., description="Zweites Merkmal, z. B. Zahl")

# ---------- Modell laden ----------
def load_model():
    if not os.path.exists(MODEL_PATH):
        logger.warning("Modellpfad %s nicht gefunden", MODEL_PATH)
        raise FileNotFoundError(f"Modelldatei '{MODEL_PATH}' nicht gefunden. Bitte trainiere zuerst das Modell.")
    logger.info("Lade Modell aus %s", MODEL_PATH)
    return joblib.load(MODEL_PATH)

model = None
try:
    model = load_model()
    logger.info("Modell geladen.")
except FileNotFoundError as e:
    model = None
    startup_error = str(e)
    logger.error("Startup-Fehler: %s", startup_error)
else:
    startup_error = None

# ---------- Endpunkte ----------
@app.get("/health")
def health():
    status = {"status": "ok", "model_loaded": model is not None, "error": startup_error}
    logger.debug("Health-Check: %s", status)
    return status

@app.post("/predict")
def predict(payload: PredictRequest):
    if model is None:
        logger.error("Vorhersage abgelehnt: %s", startup_error)
        raise HTTPException(status_code=503, detail=f"Modell nicht geladen: {startup_error}")

    df = pd.DataFrame([payload.model_dump()])

    try:
        pred = model.predict(df)[0]
    except Exception as ex:
        logger.exception("Vorhersage fehlgeschlagen: %s", ex)
        raise HTTPException(status_code=400, detail=f"Vorhersage fehlgeschlagen: {str(ex)}")

    try:
        out = int(pred)
    except Exception:
        out = str(pred)

    logger.info("Vorhersage erfolgreich: %s -> %s", payload.model_dump(), out)
    return {"prediction": out}
