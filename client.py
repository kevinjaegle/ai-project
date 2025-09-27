# client.py
import requests

payload = {"feature1": 1.2, "feature2": 3.4}

# Anfrage an den lokalen Server
r = requests.post("http://127.0.0.1:8000/predict", json=payload)

print("Antwort der API:", r.json())
