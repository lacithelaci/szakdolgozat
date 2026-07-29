"""
Modell információs oldal.

A betanított modellek teljesítményének és jellemzőinek bemutatása.
"""

import pandas as pd
import streamlit as st

from modules import charts
from modules.predictor import load_artifacts

st.set_page_config(
    page_title="Modell információ",
    page_icon="🤖",
    layout="wide",
)

st.title("Modellek teljesítménye és összehasonlítása")

# Modellek és metrikák betöltése
artifacts = load_artifacts()

if artifacts is None:
    st.error(
        "A modellek nincsenek betanítva. Futtasd le a projekt gyökeréből:\n\n"
        "```\npython train_models.py\n```"
    )
    st.stop()

metrics = artifacts["metrics"]

stage_labels = {
    "early": "Beiratkozás előtti modell",
    "midterm": "1. félév utáni modell",
}

# Modell eredmények megjelenítése
for stage, stage_data in metrics.items():

    st.header(
        stage_labels[stage]
    )

    st.caption(
        f"Győztes modell: **{stage_data['best_model']}** "
        f"({len(stage_data['features'])} feature)"
    )

    results_df = pd.DataFrame(
        [
            {
                "Modell": name,
                "Accuracy": r["accuracy"],
                "F1-Score": r["f1_score"],
            }
            for name, r in stage_data["results"].items()
        ]
    ).sort_values(
        "F1-Score",
        ascending=False,
    )

    c1, c2 = st.columns([1, 1])

    with c1:

        st.dataframe(
            results_df.style.format(
                {
                    "Accuracy": "{:.3f}",
                    "F1-Score": "{:.3f}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        best_cm = stage_data["results"][
            stage_data["best_model"]
        ]["confusion_matrix"]

        st.plotly_chart(
            charts.confusion_matrix_heatmap(
                best_cm,
                f"Konfúziós mátrix - {stage_data['best_model']}",
            ),
            use_container_width=True,
        )

    with c2:

        model_obj = (
            artifacts["early_model"]
            if stage == "early"
            else artifacts["midterm_model"]
        )

        if hasattr(model_obj, "feature_importances_"):
            importances = dict(
                zip(
                    stage_data["features"],
                    model_obj.feature_importances_.tolist(),
                )
            )

            st.plotly_chart(
                charts.feature_importance_bar(
                    importances,
                    "Jellemzők fontossága",
                ),
                use_container_width=True,
            )

    st.divider()

st.subheader("Módszertani megjegyzések")

st.markdown(
    """
- Mindkét szinten **3 modellt** hasonlítottunk össze: Logisztikus Regresszió,
  Random Forest és Gradient Boosting. A kiválasztás F1-score alapján történt,
  mivel kiegyensúlyozottabb értékelést ad osztály-egyensúlytalanság esetén.
- A **beiratkozás előtti modell** kizárólag olyan adatokat használ,
  amelyek a jelentkezés időpontjában elérhetők, így elkerüli az adatbeszivárgást.
- Az **1. félév utáni modell** az első féléves tanulmányi eredményekkel egészül ki,
  ami pontosabb előrejelzést tesz lehetővé, és megerősíti a korai tanulmányi
  teljesítmény fontosságát a dropout kockázat becslésében.
"""
)
