import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_table


import pandas as pd

from app import app
from apps.prices.prices import get_price
from apps.performance.streak import Streak
from apps.error_page import error
from apps.sub_navbar import get_sub_navbar


filtert_text = {'D':'Daily', 'W':'Weekly', 'M':'Monthly'}

streak_text = {
                'TG':'Top Gain',
                'TL':'Top Loss',
                'TGAH':'Top Gain After-Hours',
                'TLAH':'Top Loss After-Hours',
                'TWS':'Top Winning Streak',
                'TLS':'Top Losing Streak',
                'TWSP':'Top Winning Streak by %',
                'TLSP':'Top Losing Streak by %',   
                }


timeres_dd =  dbc.FormGroup(
            [
                dcc.Dropdown(
                    id="time-res",
                    options=[
                        {"label": i, "value": col} for col, i in filtert_text.items()
                    ],
                    value="D",
                ),
            ]
            )

streak_dd =  dbc.FormGroup(
            [
                dcc.Dropdown(
                    id="streak",
                    options=[
                        {"label": i, "value": col} for col, i in streak_text.items()
                    ],
                    value="TG",
                ),
            ]
            )


def get_page(ticker):
    
    sub_navbar = get_sub_navbar(ticker)

    layout = html.Div([
        sub_navbar,
        dbc.Container([
                        dbc.Row([
                            dbc.Col([timeres_dd], width=6),
                            dbc.Col([streak_dd], width=6),
                        ])   
                      ]),

        dbc.Container(id='performance-table'),
        dcc.Input(id='hidden-input', type='text', value=ticker, style={'display': 'none'}),
    ])

    return layout


@app.callback(
    Output('performance-table', 'children'),
    [Input('hidden-input', 'value'), Input('time-res', 'value'), Input('streak', 'value')])
def get_streak(ticker, timeres, streak):

    pdata = get_price(ticker, timeres)

    if pdata is None:
        return error

    s = Streak(ticker, pdata, timeres)

    if streak == 'TG':
        s.get_win_all()
        figdata = [s.data_main]
    elif streak == 'TL':
        s.get_loss_all()
        figdata = [s.data_main]
    elif streak == 'TGAH':
        s.get_win_all_ah()
        figdata = [s.data_main]
    elif streak == 'TLAH':
        s.get_loss_all_ah()
        figdata = [s.data_main]
    elif streak == 'TWS':
        s.get_win_streak()
        figdata = s.data_main
    elif streak == 'TLS':
        s.get_loss_streak()
        figdata = s.data_main
    elif streak == 'TWSP':
        s.get_win_perc_streak()
        figdata = s.data_main
    elif streak == 'TLSP':
        s.get_loss_perc_streak()
        figdata = s.data_main

    layout = s.layout
    table = s.table

    fig = go.Figure(data=figdata, layout=layout)

    return html.Div([ 
                        dcc.Graph(id='Performance', figure=fig),
                        table
                    ])


