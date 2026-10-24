import plotly.graph_objects as go
import pandas as pd

def plot_monthly_loan_amount(df, grades, start_date, end_date):
    GRADE_COLORS = {
        "A": "#0a821e",
        "B": "#33a345",
        "C": "#d1af17",
        "D": "#e8a41c",
        "E": "#e68d27",
        "F": "#db4409",
        "G": "#e31919"
    }

    df = df.copy()
    df["issue_date"] = pd.to_datetime(df["issue_date"])
    df = df[(df["issue_date"] >= start_date) & (df["issue_date"] <= end_date)]

    monthly = (
        df.groupby([pd.Grouper(key="issue_date", freq="ME"), "grade"])["loan_amount"]
        .sum().reset_index()
    )

    fig = go.Figure()

    for g in grades:
        sub = monthly[monthly["grade"] == g]
        if sub.empty:
            continue

        color = GRADE_COLORS.get(g, "#FFFFFF")

        fig.add_trace(go.Scatter(
            x=sub["issue_date"],
            y=sub["loan_amount"],
            mode="lines+markers",
            name=f"Grade {g}",
            line=dict(color=color, width=3),
            marker=dict(color=color, size=6),
            hovertemplate=(
                "<b>Grade: %{customdata}</b><br>" +
                "Month: %{x|%Y-%m}<br>" +
                "Loan Amount: %{y:,.0f}<extra></extra>"
            ),
            hoverlabel=dict(
                bgcolor=color,
                font=dict(color="white")
            ),
            customdata=sub["grade"]
        ))

    fig.update_layout(
        title={
            "text": "Monthly Loan Amount by Grade",
            "x": 0.5,
            "xanchor": "center",
            "y": 0.95,
            "yanchor": "top",
            "font": dict(color="white")
        },
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.0,
            xanchor="center",
            x=0.5,
            font=dict(color="white")
        ),
        xaxis=dict(
            tickformat="%Y-%m",
            color="white",
            showgrid=False
        ),
        yaxis=dict(
            color="white",
            gridcolor="rgba(255,255,255,0.2)",
            zeroline=False
        ),
        plot_bgcolor="#3C3F41",
        paper_bgcolor="#3C3F41",
        template="plotly_dark",
        height=520
    )
    return fig