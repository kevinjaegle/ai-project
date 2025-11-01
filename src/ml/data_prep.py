"""Hilfsfunktionen zur Aufbereitung von Trainings- und Testdaten."""

from __future__ import annotations

import pandas as pd
from sklearn.model_selection import train_test_split


def run(
    input_path: str = "data.csv",
    *,
    train_output_path: str = "train.csv",
    test_output_path: str = "test.csv",
    test_size: float = 0.2,
    random_state: int | None = 42,
):
    """Splitte die Rohdaten in Trainings- und Testdaten und speichere sie als CSV.

    Args:
        input_path: Pfad zur Eingabedatei mit den Rohdaten.
        train_output_path: Zieldatei für die Trainingsdaten.
        test_output_path: Zieldatei für die Testdaten.
        test_size: Anteil der Daten, der in den Testdatensatz wandert.
        random_state: Zufalls-Seed für deterministische Splits.

    Returns:
        Tuple aus dem Trainings- und Test-``DataFrame``.
    """

    df = pd.read_csv(input_path)
    train_df, test_df = train_test_split(
        df, test_size=test_size, random_state=random_state
    )

    train_df.to_csv(train_output_path, index=False)
    test_df.to_csv(test_output_path, index=False)

    return train_df, test_df


if __name__ == "__main__":
    run()
