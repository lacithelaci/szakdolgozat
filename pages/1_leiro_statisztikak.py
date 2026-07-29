"""
Leíró statisztikai oldal.

Interaktív elemzéseket és vizualizációkat készít a hallgatói adatokból.
"""

import streamlit as st

import config
from modules import charts
from modules.data_processing import load_raw_data

st.set_page_config(
    page_title="Leíró statisztikák",
    page_icon="📊",
    layout="wide",
)

st.title("Leíró statisztikák és összefüggések")

df = load_raw_data()

# Szűrők
with st.sidebar:
    st.header("Szűrők")

    courses = sorted(
        df["Course_name"]
        .dropna()
        .unique()
    )

    selected_courses = st.multiselect(
        "Szak",
        courses,
        default=courses,
    )

    gender_filter = st.multiselect(
        "Nem",
        options=[0, 1],
        format_func=lambda x: config.GENDER_LABELS[x],
        default=[0, 1],
    )

    scholarship_filter = st.multiselect(
        "Ösztöndíjas",
        options=[0, 1],
        format_func=lambda x: config.YES_NO[x],
        default=[0, 1],
    )

# Szűrt adatállomány
filtered = df[
    df["Course_name"].isin(selected_courses)
    & df["Gender"].isin(gender_filter)
    & df["Scholarship holder"].isin(scholarship_filter)
    ]

if filtered.empty:
    st.warning(
        "A szűrési feltételeknek egyetlen hallgató sem felel meg."
    )
    st.stop()

st.caption(
    f"A szűrt adathalmaz mérete: {len(filtered):,} hallgató"
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Pénzügyi & szociális",
        "Tanulmányi teljesítmény",
        "Szakok",
        "Korrelációk",
    ]
)

with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.plotly_chart(
            charts.dropout_rate_bar(
                filtered,
                "Tuition fees up to date",
                config.YES_NO,
                "Dropout arány - tandíj rendezettsége",
            ),
            use_container_width=True,
        )

    with c2:
        st.plotly_chart(
            charts.dropout_rate_bar(
                filtered,
                "Debtor",
                config.YES_NO,
                "Dropout arány - adósság",
            ),
            use_container_width=True,
        )

    c3, c4 = st.columns(2)

    with c3:
        st.plotly_chart(
            charts.dropout_rate_bar(
                filtered,
                "Scholarship holder",
                config.YES_NO,
                "Dropout arány - ösztöndíj",
            ),
            use_container_width=True,
        )

    with c4:
        st.plotly_chart(
            charts.dropout_rate_bar(
                filtered,
                "Gender",
                config.GENDER_LABELS,
                "Dropout arány - nem szerint",
            ),
            use_container_width=True,
        )

    st.info(
        "A tandíjukat nem rendező hallgatók közel 94%-a lemorzsolódik, míg a "
        "rendezettek esetében ez csak ~31%. Az adósság és a férfi nem szintén "
        "megemelt lemorzsolódási kockázattal jár, míg az ösztöndíj védőfaktorként hat."
    )

with tab2:
    c1, c2 = st.columns(2)

    with c1:
        st.plotly_chart(
            charts.boxplot_by_dropout(
                filtered,
                "Curricular units 1st sem (approved)",
                "Teljesített tárgyak - 1. félév",
            ),
            use_container_width=True,
        )

    with c2:
        st.plotly_chart(
            charts.boxplot_by_dropout(
                filtered,
                "Curricular units 1st sem (grade)",
                "Átlagjegy - 1. félév",
            ),
            use_container_width=True,
        )

    c3, c4 = st.columns(2)

    with c3:
        st.plotly_chart(
            charts.boxplot_by_dropout(
                filtered,
                "Age at enrollment",
                "Életkor beiratkozáskor",
            ),
            use_container_width=True,
        )

    with c4:
        st.plotly_chart(
            charts.boxplot_by_dropout(
                filtered,
                "grade_diff",
                "Jegyváltozás 1. -> 2. félév",
            ),
            use_container_width=True,
        )

    st.info(
        "A végzett hallgatók átlagosan több mint kétszer annyi tárgyat teljesítenek "
        "az 1. félévben, és magasabb átlagjeggyel rendelkeznek, mint a lemorzsolódók. "
        "A 2. félévre romló jegyátlag szintén erős dropout-jelzés."
    )

with tab3:
    st.plotly_chart(
        charts.course_dropout_ranking(
            filtered,
            top_n=10,
        ),
        use_container_width=True,
    )

    st.info(
        "A szakok közötti eltérés arra utal, hogy nem csak egyéni háttér, hanem "
        "intézményi/tantervi tényezők is szerepet játszanak a lemorzsolódásban."
    )

with tab4:
    st.plotly_chart(
        charts.correlation_heatmap(
            filtered,
            config.NUMERIC_COLS,
            "Numerikus változók korrelációja",
        ),
        use_container_width=True,
    )

    st.info(
        "A lemorzsolódás legszorosabb (negatív) összefüggésben a félévente "
        "teljesített tárgyak számával áll - minél kevesebb tárgyat teljesít "
        "valaki, annál nagyobb eséllyel morzsolódik le."
    )
