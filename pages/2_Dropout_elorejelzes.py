"""
Egyedi hallgatói dropout előrejelzés oldala.
"""

import streamlit as st

import config
from modules import charts
from modules.data_processing import engineer_input_row
from modules.predictor import load_artifacts, predict

st.set_page_config(
    page_title="Dropout előrejelzés",
    page_icon="🎯",
    layout="wide",
)

st.title("Egyedi hallgatói dropout előrejelzés")

# Modellek betöltése
artifacts = load_artifacts()

if artifacts is None:
    st.error(
        "A modellek nincsenek betanítva. Futtasd le a projekt gyökeréből:\n\n"
        "```\npython train_models.py\n```\n\n"
        "majd töltsd be újra ezt az oldalt."
    )
    st.stop()

stage = st.radio(
    "Melyik szakaszban vagyunk?",
    options=["early", "midterm"],
    format_func=lambda s: (
        "Beiratkozás előtt (csak alap adatok)"
        if s == "early"
        else "1. félév után (tanulmányi eredményekkel - pontosabb)"
    ),
    horizontal=True,
)

st.divider()

# Hallgatói adatbekérő űrlap
with st.form("prediction_form"):
    st.subheader("Alap adatok")

    c1, c2, c3 = st.columns(3)

    with c1:
        age = st.number_input(
            "Életkor beiratkozáskor",
            min_value=16,
            max_value=80,
            value=20,
        )

        gender = st.selectbox(
            "Nem",
            options=[0, 1],
            format_func=lambda x: config.GENDER_LABELS[x],
        )

        marital_status = st.selectbox(
            "Családi állapot",
            options=list(config.MARITAL_STATUS_LABELS.keys()),
            format_func=lambda x: config.MARITAL_STATUS_LABELS[x],
        )

    with c2:
        application_mode = st.selectbox(
            "Jelentkezési mód",
            options=list(config.APPLICATION_MODE_LABELS.keys()),
            format_func=lambda x: config.APPLICATION_MODE_LABELS[x],
        )

        application_order = st.number_input(
            "Jelentkezési sorrend (0=első preferencia)",
            min_value=0,
            max_value=9,
            value=0,
        )

        course = st.selectbox(
            "Szak",
            options=list(config.COURSE_LABELS.keys()),
            format_func=lambda x: config.COURSE_LABELS[x],
        )

    with c3:
        displaced = st.selectbox(
            "Elköltözött otthonról",
            options=[0, 1],
            format_func=lambda x: config.YES_NO[x],
        )

        international = st.selectbox(
            "Nemzetközi hallgató",
            options=[0, 1],
            format_func=lambda x: config.YES_NO[x],
        )

    st.subheader("Pénzügyi helyzet")

    c4, c5, c6 = st.columns(3)

    with c4:
        scholarship = st.selectbox(
            "Ösztöndíjas",
            options=[0, 1],
            format_func=lambda x: config.YES_NO[x],
        )

    with c5:
        debtor = st.selectbox(
            "Van tartozása",
            options=[0, 1],
            format_func=lambda x: config.YES_NO[x],
        )

    with c6:
        tuition_paid = st.selectbox(
            "Tandíj rendezve",
            options=[0, 1],
            format_func=lambda x: config.YES_NO[x],
        )

    st.subheader("Szülők végzettsége")

    c7, c8 = st.columns(2)

    with c7:
        mother_qual = st.selectbox(
            "Édesanya végzettsége",
            options=list(config.QUALIFICATION_LABELS.keys()),
            format_func=lambda x: config.QUALIFICATION_LABELS[x],
        )

    with c8:
        father_qual = st.selectbox(
            "Édesapa végzettsége",
            options=list(config.QUALIFICATION_LABELS.keys()),
            format_func=lambda x: config.QUALIFICATION_LABELS[x],
        )

    # Csak midterm modellnél jelennek meg a féléves eredmények
    midterm_values = {}

    if stage == "midterm":
        st.subheader("1. féléves tanulmányi eredmények")

        c9, c10, c11 = st.columns(3)

        with c9:
            midterm_values["Curricular units 1st sem (enrolled)"] = st.number_input(
                "Felvett tárgyak száma",
                min_value=0,
                max_value=30,
                value=6,
            )

            midterm_values["Curricular units 1st sem (credited)"] = st.number_input(
                "Beszámított (kreditált) tárgyak",
                min_value=0,
                max_value=30,
                value=0,
            )

        with c10:
            midterm_values["Curricular units 1st sem (evaluations)"] = st.number_input(
                "Vizsgázott tárgyak (evaluations)",
                min_value=0,
                max_value=50,
                value=6,
            )

            midterm_values["Curricular units 1st sem (approved)"] = st.number_input(
                "Sikeresen teljesített tárgyak",
                min_value=0,
                max_value=30,
                value=5,
            )

        with c11:
            midterm_values["Curricular units 1st sem (grade)"] = st.number_input(
                "Átlagjegy (0-20)",
                min_value=0.0,
                max_value=20.0,
                value=12.0,
                step=0.1,
            )

            midterm_values["Curricular units 1st sem (without evaluations)"] = st.number_input(
                "Vizsga nélkül maradt tárgyak",
                min_value=0,
                max_value=20,
                value=0,
            )

    submitted = st.form_submit_button(
        "Előrejelzés futtatása",
        type="primary",
        use_container_width=True,
    )

if submitted:

    # Modell bemenet összeállítása
    raw_input = {
        "Age at enrollment": age,
        "Gender": gender,
        "Marital status": marital_status,
        "Application mode": application_mode,
        "Application order": application_order,
        "Course": course,
        "Displaced": displaced,
        "International": international,
        "Scholarship holder": scholarship,
        "Debtor": debtor,
        "Tuition fees up to date": tuition_paid,
        "Mother's qualification": mother_qual,
        "Father's qualification": father_qual,
    }

    raw_input.update(midterm_values)

    engineered = engineer_input_row(raw_input)

    proba, label, importances = predict(
        stage,
        engineered,
        artifacts,
    )

    # Eredmények megjelenítése
    st.divider()

    res_col1, res_col2 = st.columns([1, 1.3])

    with res_col1:

        st.plotly_chart(
            charts.probability_gauge(proba),
            use_container_width=True,
        )

        if proba >= 0.66:
            st.error(
                f"**Magas kockázat** - előrejelzett kimenetel: {label}"
            )

        elif proba >= 0.33:
            st.warning(
                f"**Közepes kockázat** - előrejelzett kimenetel: {label}"
            )

        else:
            st.success(
                f"**Alacsony kockázat** - előrejelzett kimenetel: {label}"
            )

        st.caption(
            "A modell valószínűségi becslése, nem determinisztikus döntés - "
            "korai beavatkozási jelzésre alkalmas, önmagában nem elég egyéni döntéshez."
        )

    with res_col2:

        if importances:
            st.plotly_chart(
                charts.feature_importance_bar(
                    importances,
                    "Mely tényezők számítanak legtöbbet ennél a modellnél?",
                ),
                use_container_width=True,
            )
