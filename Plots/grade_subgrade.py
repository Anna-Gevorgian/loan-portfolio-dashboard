import plotly.graph_objects as go
import pandas as pd


def plot_grade_subgrade(df, start_date, end_date, show_subgrade=False, selected_grade="A"):

    df = df.copy()
    df["issue_date"] = pd.to_datetime(df["issue_date"])

    df_range = df[(df["issue_date"] >= start_date) & (df["issue_date"] <= end_date)]

    if df_range.empty:
        raise ValueError("No data found for the selected period.")

    if not show_subgrade:
        agg = df_range.groupby("grade")["loan_amount"].sum().reset_index()
        agg = agg.sort_values("grade")

        title_text = "Loan Amount by Grade"
        x_data = agg["grade"]
        y_data = agg["loan_amount"]

    else:
        df_grade = df_range[df_range["grade"] == selected_grade]

        if df_grade.empty:
            raise ValueError(f"No data found for grade {selected_grade}.")

        agg = df_grade.groupby("sub_grade")["loan_amount"].sum().reset_index()
        agg = agg.sort_values("sub_grade")

        title_text = f"Loan Amount by Subgrade ({selected_grade})"
        x_data = agg["sub_grade"]
        y_data = agg["loan_amount"]

    hover_text = [
        f"<b>{x}</b><br>Loan Amount: ${y:,.0f}<extra></extra>"
        for x, y in zip(x_data, y_data)
    ]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=x_data,
        y=y_data,
        marker=dict(color="#4ade80", line=dict(color="#22c55e", width=1)),
        text=[f"{val:,.0f}" for val in y_data],
        textposition="inside",
        textfont=dict(color="white", size=11),
        hovertemplate=hover_text,
        hoverlabel=dict(bgcolor="#1f2937", font=dict(color="white"))
    ))

    fig.update_layout(
        title={
            "text": title_text,
            "x": 0.5,
            "xanchor": "center",
            "y": 0.95,
            "yanchor": "top",
            "font": dict(color="white", size=18)
        },
        xaxis=dict(
            title="",
            color="white",
            showgrid=False,
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title="",
            color="white",
            gridcolor="rgba(255,255,255,0.2)",
            zeroline=False,
            tickformat=",.0f"
        ),
        plot_bgcolor="#3C3F41",
        paper_bgcolor="#3C3F41",
        template="plotly_dark",
        height=500,
        showlegend=False
    )

    return fig