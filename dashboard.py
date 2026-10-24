import dash
from dash import dcc, html, Input, Output
import pandas as pd

from Plots.monthly_loan_amount import plot_monthly_loan_amount
from Plots.map_by_range import plot_map_by_range
from Plots.grade_subgrade import plot_grade_subgrade
from Plots.sunburst import plot_sunburst
from Plots.categorical_count import plot_categorical_count

df = pd.read_excel("Data/portfolio.xlsx", engine='openpyxl')

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Styles
CARD_STYLE = {
    'backgroundColor': '#3C3F41',
    'borderRadius': '10px',
    'border': '1px solid #6b7280',
    'padding': '20px',
    'flex': '1 1 300px',
    'minWidth': '0',
    'display': 'flex',
    'flexDirection': 'column'
}

ROW_STYLE = {
    'display': 'flex',
    'gap': '20px',
    'flexWrap': 'wrap',
    'marginBottom': '20px',
    'width': '100%'
}

GRAPH_STYLE = {'height': '450px'}

HEADER_STYLE = {
    'textAlign': 'center',
    'color': 'white',
    'marginBottom': '30px',
    'fontSize': '36px',
    'fontWeight': 'bold'
}

# Layout
app.layout = html.Div(
    style={
        'backgroundColor': '#2B2B2B',
        'padding': '20px',
        'minHeight': '100vh',
        'fontFamily': 'Arial, sans-serif',
        'maxWidth': '100vw',
        'overflowX': 'hidden',
        'boxSizing': 'border-box'
    },
    children=[
        html.H1("Loan Portfolio Dashboard", style=HEADER_STYLE),

        # Row 1: Monthly Loan Amount & Map
        html.Div(style=ROW_STYLE, children=[
            # Chart 1: Monthly Loan Amount
            html.Div(style=CARD_STYLE, children=[
                html.Div(
                    style={
                        'display': 'flex',
                        'justifyContent': 'space-between',
                        'flexWrap': 'wrap',
                        'gap': '10px',
                        'marginBottom': '15px',
                        'alignItems': 'center'
                    },
                    children=[
                        dcc.Dropdown(
                            id='grade-dropdown-chart1',
                            options=[{'label': g, 'value': g} for g in ['A', 'B', 'C', 'D', 'E', 'F', 'G']],
                            value=['A', 'B', 'C', 'D', 'E'],  # default selected
                            multi=True,
                            clearable=False,
                            style={'width': '200px'}
                        ),

                        dcc.DatePickerRange(
                            id='chart1-date-range',
                            start_date='2021-07-01',
                            end_date='2021-12-10',
                            display_format='YYYY-MM-DD'
                        )
                    ]
                ),
                dcc.Store(id='selected-grades', data=['A', 'B', 'C', 'D', 'E']),
                dcc.Graph(id='chart1-monthly', config={'displayModeBar': False}, style=GRAPH_STYLE)
            ]),

            # Chart 2: Map
            html.Div(style=CARD_STYLE, children=[
                html.Div(
                    style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '15px'},
                    children=[
                        dcc.DatePickerRange(
                            id='chart2-date-range',
                            start_date='2021-07-01',
                            end_date='2021-12-31',
                            display_format='YYYY-MM-DD'
                        )
                    ]
                ),
                dcc.Graph(id='chart2-map', config={'displayModeBar': False}, style=GRAPH_STYLE)
            ])
        ]),

        # Row 2: Grade/Subgrade
        html.Div(style=ROW_STYLE, children=[
            html.Div(style={**CARD_STYLE, 'flex': '1 1 100%'}, children=[
                html.Div(
                    style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'flexWrap': 'wrap',
                        'gap': '10px',
                        'marginBottom': '15px',
                        'alignItems': 'center'
                    },
                    children=[
                        dcc.DatePickerRange(
                            id='chart3-date-range',
                            start_date='2021-01-01',
                            end_date='2021-12-31',
                            display_format='YYYY-MM-DD'
                        ),
                        html.Div(
                            style={'display': 'flex', 'gap': '15px', 'alignItems': 'center'},
                            children=[
                                html.Label('Subgrade Mode',
                                           style={'color': 'white', 'fontSize': '14px', 'marginBottom': '0'}),
                                dcc.Checklist(
                                    id='subgrade-toggle',
                                    options=[{'label': '', 'value': 'show'}],
                                    value=[],
                                    style={'transform': 'scale(1.5)', 'marginLeft': '5px'}
                                ),
                                dcc.Dropdown(
                                    id='grade-dropdown',
                                    options=[{'label': g, 'value': g} for g in ['A', 'B', 'C', 'D', 'E', 'F', 'G']],
                                    value='A',
                                    style={'width': '100px'},
                                    disabled=True,
                                    clearable=False
                                )
                            ]
                        )
                    ]
                ),
                dcc.Graph(id='chart3-grade', config={'displayModeBar': False}, style=GRAPH_STYLE)
            ])
        ]),

        # Row 3: Sunburst & Categorical Count
        html.Div(style=ROW_STYLE, children=[
            # Chart 4: Sunburst
            html.Div(style={**CARD_STYLE, 'flex': '3'}, children=[
                html.Div(
                    style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '15px'},
                    children=[
                        dcc.DatePickerRange(
                            id='chart4-date-range',
                            start_date='2021-09-01',
                            end_date='2021-12-31',
                            display_format='YYYY-MM-DD'
                        )
                    ]
                ),
                dcc.Graph(id='chart4-sunburst', config={'displayModeBar': False}, style=GRAPH_STYLE)
            ]),

            # Chart 5: Categorical Count
            html.Div(style={**CARD_STYLE, 'flex': '5'}, children=[
                html.Div(
                    style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'marginBottom': '15px',
                        'alignItems': 'center',
                        'flexWrap': 'wrap',
                        'gap': '10px'
                    },
                    children=[
                        dcc.DatePickerRange(
                            id='chart5-date-range',
                            start_date='2021-01-01',
                            end_date='2021-12-31',
                            display_format='YYYY-MM-DD'
                        ),
                        dcc.Dropdown(
                            id='variable-dropdown',
                            options=[
                                {'label': 'Purpose', 'value': 'purpose'},
                                {'label': 'Home Ownership', 'value': 'home_ownership'},
                                {'label': 'Employment Length', 'value': 'emp_length'}
                            ],
                            value='purpose',
                            style={'width': '200px'},
                            clearable=False
                        )
                    ]
                ),
                dcc.Graph(id='chart5-categorical', config={'displayModeBar': False}, style=GRAPH_STYLE)
            ])
        ])
    ]
)


# Callbacks
@app.callback(
    Output('selected-grades', 'data'),
    Input('grade-dropdown-chart1', 'value')
)
def update_selected_grades(selected):
    if not selected:
        return ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    return selected

@app.callback(
    Output('chart1-monthly', 'figure'),
    [Input('selected-grades', 'data'),
     Input('chart1-date-range', 'start_date'),
     Input('chart1-date-range', 'end_date')]
)
def update_chart1(grades, start, end):
    if not grades:
        grades = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    return plot_monthly_loan_amount(df, grades, pd.to_datetime(start), pd.to_datetime(end))


@app.callback(
    Output('chart2-map', 'figure'),
    [Input('chart2-date-range', 'start_date'),
     Input('chart2-date-range', 'end_date')]
)
def update_chart2(start, end):
    return plot_map_by_range(df, pd.to_datetime(start), pd.to_datetime(end))


@app.callback(
    [Output('chart3-grade', 'figure'),
     Output('grade-dropdown', 'disabled')],
    [Input('chart3-date-range', 'start_date'),
     Input('chart3-date-range', 'end_date'),
     Input('subgrade-toggle', 'value'),
     Input('grade-dropdown', 'value')]
)
def update_chart3(start, end, toggle, selected):
    show_subgrade = 'show' in toggle
    fig = plot_grade_subgrade(df, pd.to_datetime(start), pd.to_datetime(end), show_subgrade, selected)
    return fig, not show_subgrade


@app.callback(
    Output('chart4-sunburst', 'figure'),
    [Input('chart4-date-range', 'start_date'),
     Input('chart4-date-range', 'end_date')]
)
def update_chart4(start, end):
    return plot_sunburst(df, pd.to_datetime(start), pd.to_datetime(end))


@app.callback(
    Output('chart5-categorical', 'figure'),
    [Input('chart5-date-range', 'start_date'),
     Input('chart5-date-range', 'end_date'),
     Input('variable-dropdown', 'value')]
)
def update_chart5(start, end, var):
    return plot_categorical_count(df, pd.to_datetime(start), pd.to_datetime(end), var)


if __name__ == '__main__':
    app.run(debug=True, port=8050, dev_tools_hot_reload=False)