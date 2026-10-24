import plotly.graph_objects as go
import pandas as pd

def plot_map_by_range(df, start_date, end_date):
    df = df.copy()
    df["issue_date"] = pd.to_datetime(df["issue_date"])

    df_range = df[(df["issue_date"] >= start_date) & (df["issue_date"] <= end_date)]

    if df_range.empty:
        raise ValueError("No data found for the selected period.")

    agg = df_range.groupby("address_state").agg(
        loan_count=("id", "count"),
        loan_amount=("loan_amount", "sum"),
        bad_count=("Good Or Bad Loan", lambda x: (x == "Bad Loan").sum()),
        bad_amount=("loan_amount", lambda x: x[df_range.loc[x.index, "Good Or Bad Loan"] == "Bad Loan"].sum()),
        avg_income=("annual_income", "mean")
    ).reset_index()

    agg["bad_percent"] = (agg["bad_amount"] / agg["loan_amount"] * 100).round(2)

    agg["loan_amount_f"] = agg["loan_amount"].apply(lambda x: f"{x:,.0f}")
    agg["bad_amount_f"] = agg["bad_amount"].apply(lambda x: f"{x:,.0f}")
    agg["avg_income_f"] = agg["avg_income"].apply(lambda x: f"{x:,.0f}")

    agg["hover"] = (
        "State: " + agg["address_state"] + "<br>" +
        "Loans: " + agg["loan_count"].astype(str) + "<br>" +
        "Loan Amount: $" + agg["loan_amount_f"] + "<br>" +
        "Bad Loans: " + agg["bad_count"].astype(str) + "<br>" +
        "Bad Amount: $" + agg["bad_amount_f"] + "<br>" +
        "Bad Loan %: " + agg["bad_percent"].astype(str) + "%<br>" +
        "Avg Income: $" + agg["avg_income_f"]
    )

    fig = go.Figure(
        go.Choropleth(
            locations=agg["address_state"],
            z=agg["loan_amount"],
            locationmode="USA-states",
            colorscale="Greens",
            marker_line_color="white",
            marker_line_width=1,
            colorbar_title="Loan Amount",
            text=agg["hover"],
            hoverinfo="text"
        )
    )

    fig.update_layout(
        title={
            "text": f"Loan Portfolio Map",
            "x": 0.5,
            "xanchor": "center",
            "y": 0.95,
            "yanchor": "top",
            "font": dict(color="white")
        },
        geo=dict(
            scope="usa",
            projection=go.layout.geo.Projection(type="albers usa"),
            bgcolor="#3C3F41",
            lakecolor="#3C3F41",
            landcolor="#3C3F41",
            subunitcolor="rgba(255,255,255,0.2)",
            showlakes=True,
            showland=True
        ),
        plot_bgcolor="#3C3F41",
        paper_bgcolor="#3C3F41",
        template="plotly_dark",
        height=500,
        font=dict(color="white")
    )

    return fig
