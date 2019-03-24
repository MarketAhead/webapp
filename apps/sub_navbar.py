import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import requests

from apps.prices.crypto import crypto_tickers

CRYPTO_LOGO = 'https://res.cloudinary.com/marketahead/image/upload/c_scale,h_100,q_80/v1553236208/CRYPTO%20LOGOS/'
LOGO = 'https://res.cloudinary.com/marketahead/image/upload/c_scale,h_100,q_80/v1549395052/LOGOS/'
def get_sub_navbar(ticker):

    logo = '' 
    title = ticker

    if ticker in crypto_tickers.keys():
        if ticker != crypto_tickers[ticker]:
            title = crypto_tickers[ticker] + ' - ' + ticker

        logo = CRYPTO_LOGO+ticker+'.png'

    else:
        logo = LOGO+ticker+'.png'

    #Check if Logo exists
    page = requests.get(logo)
    if (page.status_code != 200):
        logo = ''

    return html.Div([
                
                html.Div(
                        [
                            html.Img(src=logo, style={'width':'44px', 'padding':'0 5px 15px 0'}),
                            html.H1(title, className="text-center ticker-header", style={'display': 'inline-block'}),
                        ], className="text-center", style={'margin':'0 auto'}),

                html.Div(
                        [
                        dcc.Link(dbc.Button("Economic Data", color="secondary", outline=True, className="mr-2", id="correlation"), href="/c/"+ticker),
                        dcc.Link(dbc.Button("Performance", color="secondary", outline=True, className="mr-2", id="performance"), href="/p/"+ticker),
                        dcc.Link(dbc.Button("Fractals", color="secondary", outline=True, className="mr-2", id="flashback"), href="/f/"+ticker),
                        dcc.Link(dbc.Button("Trends", color="secondary", outline=True, className="mr-2", id="correlation"), href="/g/"+ticker),
                        ], className="mb-5 text-center")
                ])

