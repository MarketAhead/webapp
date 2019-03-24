import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import random
import os

from app import app,cache
import airtable

TIMEOUT = 604800
LOGO = 'https://res.cloudinary.com/marketahead/image/upload/c_scale,h_200,q_80/v1553416457/LOGOS/'

@cache.memoize(timeout=TIMEOUT)
def get_records():
    base_key = 'appJrhutVamnl10Bi'
    table_name = 'US Stocks'
    air_table = airtable.Airtable(base_key, table_name, api_key=os.environ['AIRTABLE_KEY'])
    records = air_table.get_all()

    return records

def get_card(ticker, logo_url):
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardLink(dbc.CardImg(
                                            src=(logo_url),
                                            style={"width": "100%", "height": "100%"}
                     ), href="c/"+ticker) 
                ], style={"padding": "0"}
            ),
        ],
        className='',
        style={"border":"0", "margin":"0"}
    )

def get_home():

    deck = []
    cards = []

    records = get_records()

    #Shuffle records
    random.shuffle(records)
    
    for index, record in enumerate(records):

        if record['fields']['Ticker']:
            ticker = record['fields']['Ticker']
            card = get_card(ticker, LOGO+ticker+'.png')
            cards.append(card)

        if index % 12 == 0:
            if len(cards) == 12:
                this = html.Div(cards, className='grid-row')
                deck.append(this)
            cards = []


    return dbc.Jumbotron(
        [
            html.H1("Market Ahead", className="display-4"),

            html.Div([
                html.Div("Analyze price trends, correlations, and more. Explore a company below or search for one."),
            ], className="lead"),
            html.Div(
                "Supports most stocks and top cryptos.",
                className="support",
            ),
            html.Div([html.A("Read the FAQ", href='https://medium.com/@marketahead.com/app-faq-9422d296d370', target="_blank"),
                    html.A("Twitter", href='https://twitter.com/marketahead/', target="_blank", className="ml-3"),
                    html.A("Medium", href='https://medium.com/@marketahead.com/', target="_blank", className="ml-3")
                     ], className="lead bold-link")

        ], className="text-center"), dbc.Container(deck)
