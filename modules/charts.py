"""
Újrafelhasználható Plotly ábrák a leíró statisztikai oldalhoz.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Dropout kategóriák színei
DROPOUT_COLORS = {
    0: "#4C9AFF",
    1: "#FF6B6B",
}


def dropout_rate_bar(
        df: pd.DataFrame,
        group_col: str,
        label_map: dict = None,
        title: str = ""
):
    """Csoportonkénti dropout arány oszlopdiagram."""

    rate = df.groupby(group_col)["dropout"].mean().reset_index()
    rate["dropout_pct"] = (rate["dropout"] * 100).round(1)

    if label_map:
        rate[group_col] = rate[group_col].map(label_map).fillna(rate[group_col])

    fig = px.bar(
        rate,
        x=group_col,
        y="dropout_pct",
        text="dropout_pct",
        title=title,
        labels={
            "dropout_pct": "Dropout arány (%)",
            group_col: group_col,
        },
        color="dropout_pct",
        color_continuous_scale="Reds",
    )

    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside",
    )

    fig.update_layout(
        coloraxis_showscale=False
    )

    return fig


def boxplot_by_dropout(
        df: pd.DataFrame,
        y_col: str,
        title: str = ""
):
    """Numerikus változó eloszlása dropout csoportok szerint."""

    fig = px.box(
        df,
        x="dropout",
        y=y_col,
        color="dropout",
        color_discrete_map=DROPOUT_COLORS,
        title=title,
        labels={
            "dropout": "Kimenetel (0=Végzett, 1=Dropout)",
            y_col: y_col,
        },
    )

    fig.update_layout(
        showlegend=False
    )

    return fig


def course_dropout_ranking(
        df: pd.DataFrame,
        top_n: int = 10
):
    """Legmagasabb dropout arányú szakok rangsora."""

    rate = (
        df.groupby("Course_name")["dropout"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
    )

    fig = px.bar(
        x=(rate.values * 100).round(1),
        y=rate.index,
        orientation="h",
        labels={
            "x": "Dropout arány (%)",
            "y": "Szak",
        },
        title=f"Top {top_n} legmagasabb lemorzsolódási arányú szak",
        color=rate.values,
        color_continuous_scale="Reds",
    )

    fig.update_layout(
        coloraxis_showscale=False,
        yaxis={
            "categoryorder": "total ascending"
        },
    )

    return fig


def correlation_heatmap(
        df: pd.DataFrame,
        cols: list,
        title: str = "Korrelációs mátrix"
):
    """Korrelációs hőtérkép készítése."""

    corr = df[cols + ["dropout"]].corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title=title,
        aspect="auto",
    )

    return fig


def feature_importance_bar(
        importances: dict,
        title: str = "Jellemzők fontossága"
):
    """Modell feature fontosságok megjelenítése."""

    items = sorted(
        importances.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    names = [i[0] for i in items]
    values = [i[1] for i in items]

    fig = px.bar(
        x=values,
        y=names,
        orientation="h",
        title=title,
        labels={
            "x": "Fontosság",
            "y": "",
        },
        color=values,
        color_continuous_scale="Viridis",
    )

    fig.update_layout(
        coloraxis_showscale=False,
        yaxis={
            "categoryorder": "total ascending"
        },
    )

    return fig


def confusion_matrix_heatmap(
        cm: list,
        title: str = "Konfúziós mátrix"
):
    """Konfúziós mátrix hőtérkép."""

    labels = [
        "Végzett (0)",
        "Dropout (1)",
    ]

    return ff_confusion(
        cm,
        labels,
        title,
    )


def ff_confusion(
        cm,
        labels,
        title
):
    """Hőtérkép létrehozása konfúziós mátrixból."""

    fig = go.Figure(
        data=go.Heatmap(
            z=cm,
            x=labels,
            y=labels,
            colorscale="Blues",
            text=cm,
            texttemplate="%{text}",
            showscale=False,
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Becsült",
        yaxis_title="Valós",
        yaxis_autorange="reversed",
    )

    return fig


def probability_gauge(
        proba: float,
        title: str = "Dropout valószínűség"
):
    """Dropout valószínűség mérőóra megjelenítése."""

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=proba * 100,
            number={
                "suffix": "%"
            },
            title={
                "text": title
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                },
                "bar": {
                    "color": "#333333"
                },
                "steps": [
                    {
                        "range": [0, 33],
                        "color": "#4CAF50",
                    },
                    {
                        "range": [33, 66],
                        "color": "#FFC107",
                    },
                    {
                        "range": [66, 100],
                        "color": "#FF5252",
                    },
                ],
                "threshold": {
                    "line": {
                        "color": "black",
                        "width": 3,
                    },
                    "thickness": 0.8,
                    "value": 50,
                },
            },
        )
    )

    fig.update_layout(
        height=320,
        margin=dict(
            t=60,
            b=10,
            l=30,
            r=30,
        ),
    )

    return fig
