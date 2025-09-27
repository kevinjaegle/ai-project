# src/ml/data_prep.py
import pandas as pd
from sklearn.model_selection import train_test_split

# Datei lesen
df = pd.read_csv('data.csv')

# In Trainings- und Testdaten aufteilen
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Dataien speichern
train_df.to_csv('train.csv', index=False)
test_df.to_csv('test.csv', index=False)