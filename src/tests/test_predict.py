import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_behavior_depends_on_model():
    payload = {"feature1": 1.0, "feature2": 2.0}
    r = client.post("/predict", json=payload)

    # Wenn ein Modell existiert, erwarten wir 200 und eine "prediction"
    # Wenn kein Modell existiert, erwarten wir 503 und eine Fehlermeldung
    model_path = os.getenv("MODEL_PATH", "model.joblib")
    if os.path.exists(model_path):
        assert r.status_code == 200
        assert "prediction" in r.json()
    else:
        assert r.status_code == 503