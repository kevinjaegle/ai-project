"""Training eines einfachen Klassifikationsmodells."""

from __future__ import annotations

from typing import Sequence

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression


def run(
    train_path: str = "train.csv",
    *,
    feature_columns: Sequence[str] = ("feature1", "feature2"),
    target_column: str = "label",
    model_output_path: str = "model.joblib",
    max_iter: int = 200,
) -> LogisticRegression:
    """Trainiere ein ``LogisticRegression``-Modell und speichere es als Joblib-Datei."""

    train_df = pd.read_csv(train_path)

    X = train_df[list(feature_columns)]
    y = train_df[target_column]

    model = LogisticRegression(max_iter=max_iter)
    model.fit(X, y)

    joblib.dump(model, model_output_path)
    return model


if __name__ == "__main__":
    run()
