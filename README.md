# Loan Portfolio Dashboard

An interactive dashboard for exploring a loan portfolio, built with Dash and Plotly.

## Features
- **Monthly loan volume** over a selectable date range, filterable by credit grade
- **Geographic view** of loan amounts by region
- **Grade and sub-grade breakdown** of the portfolio
- **Sunburst chart** of the portfolio's composition
- **Categorical distributions** of loan attributes
- All views update together from a shared date-range filter

## Run locally
```bash
pip install -r requirements.txt
python dashboard.py
```
Then open http://127.0.0.1:8050.

## Structure
```
dashboard.py        # app layout and callbacks
Plots/              # one module per chart
assets/style.css    # styling
Data/portfolio.xlsx # portfolio data
```

## Stack
Python · Dash · Plotly · pandas
