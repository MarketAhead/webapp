import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import json

from app import app
from apps.prices.prices import get_price
from apps.error_page import error
from apps.sub_navbar import get_sub_navbar

from apps.correlation.corr import Correlation
from apps.correlation.geo import geo
from apps.correlation.fred import search_fred
from apps.correlation.fred_default import fred_dd_values

fred_dd =  dbc.FormGroup(
            [
                dcc.Dropdown(
                    id="fred",
                    options=[
                        {"label": i, "value": col} for col, i in fred_dd_values.items()
                    ],
                    value="SP500",
                ),
            ]
            )

fred_search = dbc.Input(type="text", placeholder="FRED© Economic Data Search", id="fsearch", style={"border-radius":".25rem"})


def get_page(ticker):

    sub_navbar = get_sub_navbar(ticker)

    layout = html.Div([
        sub_navbar,

        dbc.Container([
              dbc.Row([
                      dbc.Col([fred_dd], width=6),
                      dbc.Col([fred_search], width=6)
                    ])
              ]),
        dbc.Container(id='fred-results'),
        dbc.Container(id='correlation-table'),
        dcc.Input(id='fred-select', type='text', value='', style={'display': 'none'}),
        dcc.Input(id='hidden-input', type='text', value=ticker, style={'display': 'none'}),
    ])

    return layout



@app.callback(
    Output('fred-results', 'children'),
    [Input('fsearch', 'n_submit')], 
    [State('fsearch', 'value')])
def fred_results(ns, fsearch):

    if fsearch is not None and fsearch:

        result = search_fred(fsearch)

        if result is not None:

            result = json.loads(result)
            return dbc.FormGroup(
                    [
                        dcc.Dropdown(
                            id="fred-select",
                            options=[
                                {"label": item['title'], "value": item['id']} for item in result
                            ],
                            value="",
                        ),
                    ]
                    )
        else:
            return html.P("🤭 Oops! Please Try Again")

    else:
        return None



@app.callback(
    Output('correlation-table', 'children'),
    [Input('hidden-input', 'value'), Input('fred', 'value'), Input('fred-select', 'value')])
def get_correlation(ticker, fred, freds):

    pdata = get_price(ticker, 'D')

    if pdata is None:
        return error

    print(ticker, fred, freds)

    c = Correlation(ticker, pdata)
    
    graphs = []

    if fred is not None and fred:
        fig = c.get_fred(fred)
        graphs.append(dcc.Graph(id='Fred', figure=fig))

    if freds is not None and freds:
        fig2 = c.get_fred(freds)
        graphs.insert(0, dcc.Graph(id='Fred-Search', figure=fig2))
    

    return dbc.Container(graphs)





