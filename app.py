"""
A Streamlit alkalmazás főoldala.

Betölti:
- az adatokat
- a betanított modelleket
- az alap információs és statisztikai elemeket

Innen érhető el az alkalmazás többi oldala.
"""

import streamlit as st

from modules.data_processing import load_raw_data
from modules.predictor import load_artifacts

st.set_page_config(
    page_title="Hallgatói Lemorzsolódás Elemző",
    page_icon="🎓",
    layout="wide",
)

# Kezdőoldal címe és leírása
st.title("Hallgatói Lemorzsolódás Elemző Rendszer")
st.caption("Szakdolgozati projekt - Gépi tanulás alapú dropout predikció")

st.markdown(
    """
Ez az alkalmazás egy olasz felsőoktatási hallgatói adathalmaz
(UCI *Predict Students' Dropout and Academic Success* alapú)
elemzésére és lemorzsolódási kockázat előrejelzésére épül.

**Két predikciós szint áll rendelkezésre:**
- **Beiratkozás előtti modell** - beiratkozáskor elérhető adatok alapján
- **1. félév utáni modell** - tanulmányi eredményekkel kiegészített előrejelzés

Használd a bal oldali menüt a navigációhoz:
1. **Leíró statisztikák** - adatfeltárás és összefüggések vizsgálata
2. **Dropout előrejelzés** - egyéni hallgatói kockázatbecslés
3. **Modell információ** - modellek teljesítményének összehasonlítása
"""
)

# Modellek betöltése
artifacts = load_artifacts()

# Fő statisztikák megjelenítése
st.divider()

col1, col2, col3, col4 = st.columns(4)

try:
    df = load_raw_data()

    with col1:
        st.metric(
            "Hallgatók száma (elemzésben)",
            f"{len(df):,}"
        )

    with col2:
        st.metric(
            "Lemorzsolódási arány",
            f"{df['dropout'].mean() * 100:.1f}%"
        )

    with col3:
        st.metric(
            "Szakok száma",
            df["Course"].nunique()
        )

    with col4:
        if artifacts:
            best_f1 = (
                artifacts["metrics"]["midterm"]["results"]
                [artifacts["metrics"]["midterm"]["best_model"]]
                ["f1_score"]
            )

            st.metric(
                "Legjobb modell F1-score",
                f"{best_f1:.2f}"
            )
        else:
            st.metric(
                "Legjobb modell F1-score",
                "—"
            )


except FileNotFoundError:
    st.error(
        "Nem található a student_data.csv a data/ mappában."
    )

# Modell állapot visszajelzés
if artifacts is None:
    st.warning(
        "A predikciós modellek még nincsenek betanítva. "
        "Futtasd le a projekt gyökeréből:\n\n"
        "```\npython train_models.py\n```"
    )
else:
    st.success(
        "A modellek betöltve, a Dropout előrejelzés oldal használatra kész."
    )
