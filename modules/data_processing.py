"""
Adatbetöltés és feature engineering a modellhez és az elemzésekhez.
"""

import pandas as pd
import streamlit as st

import config


@st.cache_data
def load_raw_data(path: str = config.DATA_PATH) -> pd.DataFrame:
    """CSV betöltése és a szükséges segédváltozók létrehozása."""

    df = pd.read_csv(path, sep=";")

    # Csak végleges kimenetellel rendelkező hallgatók
    df = df[df["Output"].isin(["Dropout", "Graduate"])].copy()

    # Célváltozó létrehozása
    df["dropout"] = (df["Output"] == "Dropout").astype(int)

    # Olvasható címkék
    df["Course_name"] = df["Course"].map(config.COURSE_LABELS)
    df["Marital_status_name"] = (
        df["Marital status"]
        .map(config.MARITAL_STATUS_LABELS)
    )

    # Szülők felsőfokú végzettsége
    df["mother_has_degree"] = (
        df["Mother's qualification"]
        .isin(config.HIGHER_EDU_CODES)
        .astype(int)
    )

    df["father_has_degree"] = (
        df["Father's qualification"]
        .isin(config.HIGHER_EDU_CODES)
        .astype(int)
    )

    # Második félév és első félév közötti jegykülönbség
    df["grade_diff"] = (
        df["Curricular units 2nd sem (grade)"]
        - df["Curricular units 1st sem (grade)"]
    )

    return df


def engineer_input_row(raw_input: dict) -> dict:
    """Űrlapból érkező adatok kiegészítése számított feature-ökkel."""

    result = dict(raw_input)

    result["mother_has_degree"] = int(
        raw_input.get("Mother's qualification")
        in config.HIGHER_EDU_CODES
    )

    result["father_has_degree"] = int(
        raw_input.get("Father's qualification")
        in config.HIGHER_EDU_CODES
    )

    return result