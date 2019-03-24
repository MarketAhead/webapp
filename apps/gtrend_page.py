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


gtrend_input = dbc.Input(type="text", placeholder="Google™ Trend Keyword", id="gtrend", style={"border-radius":".25rem"})

gtrend_geo =  dbc.FormGroup(
            [
                dcc.Dropdown(
                    id="gtrend_geo",
                    options=[
                        {"label": i, "value": col} for col, i in geo.items()
                    ],
                    value="",
                ),
            ]
            )

def get_page(ticker):

    sub_navbar = get_sub_navbar(ticker)

    layout = html.Div([
        sub_navbar,
        dbc.Container([
                      dbc.Row([
                              dbc.Col([gtrend_input], width=6),
                              dbc.Col([gtrend_geo], width=6)
                            ])
                      ]),
        dbc.Container(id='gtrend-table'),
        dcc.Input(id='hidden-input', type='text', value=ticker, style={'display': 'none'}),
    ])

    return layout


@app.callback(
    Output('gtrend-table', 'children'),
    [Input('hidden-input', 'value'), Input('gtrend_geo', 'value'), Input('gtrend', 'n_submit')], 
    [State('gtrend', 'value')])
def get_google_trend(ticker, geo, ns, gtrend):

    pdata = get_price(ticker, 'D')

    if pdata is None:
        return error

    print(ticker, gtrend, geo)

    c = Correlation(ticker, pdata)

    if gtrend is not None and gtrend:
        fig = c.get_gtrend(gtrend, geo)
        
    else:
        fig = c.get_main()

    return dbc.Container(dcc.Graph(id='GTrend', figure=fig))





