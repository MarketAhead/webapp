import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import random
import os

from app import app,cache
import airtable

TIMEOUT = 604800

@cache.memoize(timeout=TIMEOUT)
def get_records():
    base_key = 'appJrhutVamnl10Bi'
    table_name = 'US Stocks'
    air_table = airtable.Airtable(base_key, table_name, api_key=os.environ['AIRTABLE_KEY'])
    records = air_table.get_all()

    random.shuffle(records)

    return records

def get_card(ticker, logo_url):
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardLink(dbc.CardImg(
                                            src=(logo_url)
                     ), href="c/"+ticker) 
                ], style={"padding": "0"}
            ),
        ],
        style={"border":"0", "margin":"0"}
    )

def get_home():

    deck = []
    cards = []

    records = get_records()

    for index, record in enumerate(records):

        if record['fields']['Ticker'] and record['fields']['Logo'][0]['url']:
            card = get_card(record['fields']['Ticker'], record['fields']['Logo'][0]['url'])
            cards.append(card)

        if index % 12 == 0:
            if len(cards) == 12:
                this = dbc.CardDeck(cards)
                deck.append(this)
            cards = []


    return dbc.Jumbotron(
        [
            html.H1("Market Ahead", className="display-4"),

            html.Div([
                html.Div("Analyze price trends, correlations, and more."),
            ], className="lead"),
            html.Div(
                "Supports most stocks and top cryptos.",
                className="lead",
            ),
            html.Div([html.A("Read the FAQ", href='https://medium.com/@marketahead.com/app-faq-9422d296d370', target="_blank"),
                    html.A("Twitter", href='https://twitter.com/marketahead/', target="_blank", className="ml-3"),
                    html.A("Medium", href='https://medium.com/@marketahead.com/', target="_blank", className="ml-3")

                     ])

        ], className="lead text-center"), dbc.Container(deck)
