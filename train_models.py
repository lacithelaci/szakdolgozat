"""
A modellek betanítása és mentése a Streamlit alkalmazás számára.

Létrehozott fájlok:
- early_model.pkl       -> beiratkozás előtti modell
- midterm_model.pkl     -> első félév utáni modell
- scaling_params.json   -> skálázási paraméterek
- metrics.json          -> modell eredmények
"""

import json
import os

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split

import config

RANDOM_STATE = 42


def load_and_engineer():
    """Adatok betöltése és új jellemzők létrehozása."""
    df = pd.read_csv(config.DATA_PATH, sep=";")

    # Csak a végleges kimenettel rendelkező hallgatók maradnak
    df = df[df["Output"].isin(["Dropout", "Graduate"])].copy()

    # Célváltozó: 1 = lemorzsolódás, 0 = végzés
    df["dropout"] = (df["Output"] == "Dropout").astype(int)

    # Szülők felsőfokú végzettsége
    df["mother_has_degree"] = (
        df["Mother's qualification"].isin(config.HIGHER_EDU_CODES).astype(int)
    )
    df["father_has_degree"] = (
        df["Father's qualification"].isin(config.HIGHER_EDU_CODES).astype(int)
    )

    return df


def compute_scaling_params(df):
    """Numerikus változók átlagának és szórásának mentése."""
    params = {}

    for col in config.NUMERIC_COLS:
        params[col] = {
            "mean": float(df[col].mean()),
            "std": float(df[col].std(ddof=0)) or 1.0,
        }

    return params


def scale_df(df, scaling_params):
    """Adatok standardizálása a mentett paraméterek alapján."""
    scaled = df.copy()

    for col, stats in scaling_params.items():
        if col in scaled.columns:
            scaled[col] = (
                                  scaled[col] - stats["mean"]
                          ) / stats["std"]

    return scaled


def train_and_select_best(X_train, y_train, X_test, y_test):
    """Modellek tanítása és legjobb modell kiválasztása F1 alapján."""

    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            random_state=RANDOM_STATE
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            random_state=RANDOM_STATE
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=100,
            random_state=RANDOM_STATE
        ),
    }

    results = {}
    fitted_models = {}

    for name, model in models.items():
        model.fit(X_train, y_train)

        pred = model.predict(X_test)

        results[name] = {
            "accuracy": float(accuracy_score(y_test, pred)),
            "f1_score": float(f1_score(y_test, pred)),
            "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
        }

        fitted_models[name] = model

    # Legjobb modell kiválasztása F1 érték alapján
    best_model = max(
        results,
        key=lambda x: results[x]["f1_score"]
    )

    return fitted_models, results, best_model


def main():
    os.makedirs(config.MODELS_DIR, exist_ok=True)

    df = load_and_engineer()

    # Skálázási paraméterek mentése
    scaling_params = compute_scaling_params(df)
    df_scaled = scale_df(df, scaling_params)

    metrics = {}

    # --- Beiratkozás előtti modell ---
    X_early = df_scaled[config.EARLY_FEATURES]
    y = df_scaled["dropout"]

    X_train, X_test, y_train, y_test = train_test_split(
        X_early,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y
    )

    models, results, best = train_and_select_best(
        X_train, y_train, X_test, y_test
    )

    joblib.dump(
        models[best],
        os.path.join(config.MODELS_DIR, "early_model.pkl")
    )

    metrics["early"] = {
        "results": results,
        "best_model": best,
        "features": config.EARLY_FEATURES,
    }

    print(f"[early] {best} | F1={results[best]['f1_score']:.3f}")

    # --- Első félév utáni modell ---
    X_mid = df_scaled[config.MIDTERM_FEATURES]

    X_train, X_test, y_train, y_test = train_test_split(
        X_mid,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y
    )

    models, results, best = train_and_select_best(
        X_train, y_train, X_test, y_test
    )

    joblib.dump(
        models[best],
        os.path.join(config.MODELS_DIR, "midterm_model.pkl")
    )

    metrics["midterm"] = {
        "results": results,
        "best_model": best,
        "features": config.MIDTERM_FEATURES,
    }

    print(f"[midterm] {best} | F1={results[best]['f1_score']:.3f}")

    # Eredmények mentése
    with open(
            os.path.join(config.MODELS_DIR, "scaling_params.json"),
            "w",
            encoding="utf-8"
    ) as f:
        json.dump(scaling_params, f, indent=2)

    with open(
            os.path.join(config.MODELS_DIR, "metrics.json"),
            "w",
            encoding="utf-8"
    ) as f:
        json.dump(metrics, f, indent=2)

    print("\nA modellek sikeresen mentve.")


if __name__ == "__main__":
    main()
