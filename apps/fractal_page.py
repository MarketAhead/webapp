import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from app import app

from apps.prices.prices import get_price
from apps.fractal.flashback import generate_flashback
from apps.sub_navbar import get_sub_navbar

from datetime import date
today = str(date.today())

colorway = ["#424ff9","#ec3a1c","#00cc96","#cfa5fc","#9aebfa","#f6c6fd","#fecb52","#ffa15a","#ff6692","#b6e880"]

filterf = {'close':'Close Price', 'OCP':'Open-Close %','CP':'Close %','LHP':'Low-High %', 'open':'Open Price', 'high':'High Price', 'low':'Low Price'}
filtert_text = {'D':'Daily', 'W':'Weekly', 'M':'Monthly'}
filterw = {'5':'5','15':'15','20':'20','30':'30 Periods','45':'45','60':'60'}

fractal =  dbc.FormGroup(
            [
                dcc.Dropdown(
                    id="fractal",
                    options=[
                        {"label": i, "value": col} for col, i in filterf.items()
                    ],
                    value="close",
                ),
            ]
            )

timeres =  dbc.FormGroup(
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

dateselector = dbc.DatePickerSingle(
                                    id='date-picker-single',
                                    date = today
                                )

windowselector = dcc.Slider(
                            min=5,
                            max=60,
                            marks={col: label for col, label in filterw.items()},
                            value=20,
                            id='window-slider'
                        )

options = dbc.Container([                   
                        dbc.Row([

                            dbc.Col([timeres], width=5),
                            dbc.Col([fractal], width=5),
                            dbc.Col([dateselector], width=2)

                            ]),
                        dbc.Row([
                            dbc.Col([windowselector], width=12)
                            ]),

                            #         dbc.Col[(fractal)], dcc.Col(timeres),dcc.Col(dateselector)]),
                        html.Br(),
                            # html.P(windowselector),

                            # html.P(timeres),
                            # html.P(dateselector)

                        ], id="filter-options", className="center-text")

def get_page(ticker):

    sub_navbar = get_sub_navbar(ticker)

    layout = html.Div([
                    sub_navbar,
                    dbc.Row([dbc.Col(options)]),
                    html.Div(id='fractals'),
                    dcc.Input(id='hidden-input', type='text', value=ticker, style={'display': 'none'}),
                    ])

    return layout


@app.callback(Output(component_id='fractals', component_property='children'),
                    [
                    Input('hidden-input', 'value'),
                    Input('time-res', 'value'), 
                    Input('fractal', 'value'), 
                    Input('window-slider', 'value'), 
                    Input('date-picker-single', 'date')
                    ]
                    )
def update_figure(ticker, timeRes, fractal, window, set_date):

    print(ticker, timeRes, fractal, window, set_date)

    return generate_flashback(ticker, window, timeRes, fractal, set_date)



