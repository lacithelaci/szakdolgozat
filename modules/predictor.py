"""
Modell betöltés és predikció kezelése.
"""

import json
import os

import joblib
import pandas as pd
import streamlit as st

import config


@st.cache_resource
def load_artifacts():
    """Modellek, skálázási paraméterek és metrikák betöltése."""

    early_path = os.path.join(
        config.MODELS_DIR,
        "early_model.pkl"
    )

    midterm_path = os.path.join(
        config.MODELS_DIR,
        "midterm_model.pkl"
    )

    scaling_path = os.path.join(
        config.MODELS_DIR,
        "scaling_params.json"
    )

    metrics_path = os.path.join(
        config.MODELS_DIR,
        "metrics.json"
    )

    # Hiányzó fájlok esetén nincs predikció
    missing = [
        p
        for p in [
            early_path,
            midterm_path,
            scaling_path,
            metrics_path,
        ]
        if not os.path.exists(p)
    ]

    if missing:
        return None

    early_model = joblib.load(early_path)
    midterm_model = joblib.load(midterm_path)

    with open(scaling_path, encoding="utf-8") as f:
        scaling_params = json.load(f)

    with open(metrics_path, encoding="utf-8") as f:
        metrics = json.load(f)

    return {
        "early_model": early_model,
        "midterm_model": midterm_model,
        "scaling_params": scaling_params,
        "metrics": metrics,
    }


def _scale_value(
        col: str,
        value: float,
        scaling_params: dict
) -> float:
    """Egy érték standardizálása mentett paraméterek alapján."""

    stats = scaling_params.get(col)

    if stats is None:
        return value

    return (
            value - stats["mean"]
    ) / stats["std"]


def _build_feature_row(
        engineered_input: dict,
        feature_list: list,
        scaling_params: dict
) -> pd.DataFrame:
    """Predikcióhoz szükséges modell bemeneti sor létrehozása."""

    row = {}

    for feat in feature_list:
        raw_val = engineered_input.get(feat, 0)

        if feat in scaling_params:
            row[feat] = _scale_value(
                feat,
                raw_val,
                scaling_params
            )
        else:
            row[feat] = raw_val

    return pd.DataFrame(
        [row],
        columns=feature_list,
    )


def predict(
        stage: str,
        engineered_input: dict,
        artifacts: dict
):
    """
    Predikció készítése az adott modell segítségével.

    stage:
    - early: beiratkozás előtti modell
    - midterm: első félév utáni modell
    """

    if stage == "early":
        model = artifacts["early_model"]
        feature_list = config.EARLY_FEATURES
    else:
        model = artifacts["midterm_model"]
        feature_list = config.MIDTERM_FEATURES

    X = _build_feature_row(
        engineered_input,
        feature_list,
        artifacts["scaling_params"],
    )

    proba = float(
        model.predict_proba(X)[0][1]
    )

    label = (
        "Dropout (lemorzsolódás)"
        if proba >= 0.5
        else "Graduate (végzés)"
    )

    # Feature fontosságok, ha a modell támogatja
    importances = {}

    if hasattr(model, "feature_importances_"):
        importances = dict(
            zip(
                feature_list,
                model.feature_importances_.tolist(),
            )
        )

    return proba, label, importances
