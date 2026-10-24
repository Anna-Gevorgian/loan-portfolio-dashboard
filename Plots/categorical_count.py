import plotly.graph_objects as go
import pandas as pd

def plot_categorical_count(df, start_date, end_date, variable="purpose"):
    df = df.copy()
    df["issue_date"] = pd.to_datetime(df["issue_date"])

    df_range = df[(df["issue_date"] >= start_date) & (df["issue_date"] <= end_date)]

    if df_range.empty:
        raise ValueError("No data found for the selected period.")

    agg = df_range.groupby(variable).size().reset_index(name="count")

    mask_other = agg[variable].str.lower() == "other"
    others = agg[mask_other]
    main = agg[~mask_other]

    main = main.sort_values("count", ascending=True)

    if len(main) > 15:
        main = main.tail(15)

    if not others.empty:
        agg = pd.concat([others, main], ignore_index=True)
    else:
        agg = main

    var_display = variable.replace("_", " ").title()

    hover_text = [
        f"<b>{cat}</b><br>Count: {count:,}<extra></extra>"
        for cat, count in zip(agg[variable], agg["count"])
    ]

    def custom_scale(x):
        if x <= 1000:
            return x
        else:
            return 1000 + (x - 1000) / 10

    agg["x_scaled"] = agg["count"].apply(custom_scale)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=agg["x_scaled"],
        y=agg[variable],
        orientation="h",
        marker=dict(color="#4ade80", line=dict(color="#22c55e", width=1)),
        text=[f"{val:,}" for val in agg["count"]],
        textposition="inside",
        textfont=dict(color="white", size=11),
        hovertemplate=hover_text,
        hoverlabel=dict(bgcolor="#1f2937", font=dict(color="white"))
    ))

    tick_vals = [custom_scale(x) for x in [100, 500, 1000, 5000, 10000]]
    tick_text = ["100", "500", "1k", "5k", "10k"]

    fig.update_layout(
        title={
            "text": f"Count by {var_display}",
            "x": 0.5,
            "xanchor": "center",
            "y": 0.98,
            "yanchor": "top",
            "font": dict(color="white", size=18)
        },
        xaxis=dict(
            title="",
            tickmode="array",
            tickvals=tick_vals,
            ticktext=tick_text,
            color="white",
            gridcolor="rgba(255,255,255,0.2)",
            zeroline=False,
            showgrid=True,
            range=[0, custom_scale(agg["count"].max()) * 1.05]
        ),
        yaxis=dict(
            title="",
            color="white",
            showgrid=False,
            tickfont=dict(size=11),
            automargin=True
        ),
        plot_bgcolor="#3C3F41",
        paper_bgcolor="#3C3F41",
        template="plotly_dark",
        height=500,
        showlegend=False,
        margin=dict(l=150, r=50, t=80, b=50)
    )

    return fig
