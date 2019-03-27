import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import requests

from apps.prices.crypto import crypto_tickers
from apps.home.home_items import home

CRYPTO_LOGO = 'https://res.cloudinary.com/marketahead/image/upload/c_scale,h_100,q_80/CRYPTO%20LOGOS/'
LOGO = 'https://res.cloudinary.com/marketahead/image/upload/c_scale,h_100,q_80/LOGOS/'
def get_sub_navbar(ticker):

    logo = '' 
    url = ticker
    ticker = ticker.replace('%5E', '')
    ticker = ticker.replace('^', '')

    #CRYPTO
    if ticker in crypto_tickers.keys():
        if ticker != crypto_tickers[ticker]:
            title = crypto_tickers[ticker] + ' - ' + ticker

        logo = CRYPTO_LOGO+ticker+'.png'

    #STOCKS
    else:
        if ticker in home.keys():
            title = home[ticker] + ' - ' + ticker
        else:
            title = ticker 

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

                dbc.Container(
                        [
                        dcc.Link(dbc.Button("Economic Data", color="secondary", outline=True, className="mr-2 full-width", id="correlation"), href="/c/"+url),
                        dcc.Link(dbc.Button("Performance", color="secondary", outline=True, className="mr-2 full-width", id="performance"), href="/p/"+url),
                        dcc.Link(dbc.Button("Fractals", color="secondary", outline=True, className="mr-2 full-width", id="flashback"), href="/f/"+url),
                        dcc.Link(dbc.Button("Trends", color="secondary", outline=True, className="mr-2 full-width", id="correlation"), href="/g/"+url),
                        ], className="mb-3 text-center")
                ])

