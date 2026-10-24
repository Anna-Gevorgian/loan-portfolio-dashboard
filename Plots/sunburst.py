import pandas as pd
import plotly.graph_objects as go

def plot_sunburst(df, start_date, end_date):

    GRADE_COLORS = {
        "A": "#22c55e",
        "B": "#84cc16",
        "C": "#eab308",
        "D": "#f59e0b",
        "E": "#f97316",
        "F": "#db4409",
        "G": "#e31919"
    }

    df = df.copy()
    df["issue_date"] = pd.to_datetime(df["issue_date"])

    df_range = df[(df["issue_date"] >= start_date) & (df["issue_date"] <= end_date)]

    if df_range.empty:
        raise ValueError("No data found for the selected period.")

    agg = df_range.groupby(["grade", "sub_grade"], as_index=False)["loan_amount"].sum()

    agg["sub_index"] = agg["sub_grade"].str.extract(r"(\d+)").astype(int)
    agg = agg.sort_values(["grade", "sub_index"])

    labels = []
    parents = []
    values = []
    colors = []

    for grade in ["A", "B", "C", "D", "E", "F", "G"]:
        grade_data = agg[agg["grade"] == grade]

        if grade_data.empty:
            continue

        grade_total = grade_data["loan_amount"].sum()
        labels.append(grade)
        parents.append("")
        values.append(grade_total)
        colors.append(GRADE_COLORS[grade])

        for _, row in grade_data.iterrows():
            labels.append(row["sub_grade"])
            parents.append(grade)
            values.append(row["loan_amount"])
            colors.append(GRADE_COLORS[grade])

    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        marker=dict(
            colors=colors,
            line=dict(color="#374151", width=2)
        ),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Loan Amount: %{value:,.0f}<br>"
            "Percent of parent: %{percentParent:.1%}<br>"
            "Percent of total: %{percentRoot:.1%}<extra></extra>"
        ),
        hoverlabel=dict(
            bgcolor="#1f2937",
            font=dict(color="white")
        )
    ))

    fig.update_layout(
        title=dict(
            text="Loan Amount by Grade and Subgrade",
            x=0.5,
            y=0.95,
            xanchor="center",
            yanchor="top",
            font=dict(color="white", size=18)
        ),
        template="plotly_dark",
        paper_bgcolor="#3C3F41",
        plot_bgcolor="#3C3F41",
        height=530,
        margin=dict(t=80, l=5, r=5, b=5),
        font=dict(color="white")
    )

    return fig
