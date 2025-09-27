# src/ml/train.py
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

# Trainingsdaten laden
train_df = pd.read_csv('train.csv')

# Eingaben (Features) und Ziel (Label) auswählen
X = train_df[['feature1', 'feature2']]
y = train_df['label']

# Model erstellen
model = LogisticRegression(max_iter=200)

# Model trainieren
model.fit(X, y)

# Model speichern
joblib.dump(model, 'model.joblib')