import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import random
import os

from app import app,cache
from apps.home.home_items import home

LOGO = 'https://res.cloudinary.com/marketahead/image/upload/c_scale,h_200,q_80/v1553507334/LOGOS/'

def get_card(ticker, name, logo_url):
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardLink(dbc.CardImg(
                                            src=(logo_url),
                                            title= name,
                                            style={"width": "100%"}
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

    #Shuffle records
    keylist = []
    keylist.extend(iter(home.keys())) 
    random.shuffle(keylist)

    for index, key in enumerate(keylist):
        ticker = key
        card = get_card(ticker, home[key], LOGO+ticker+'.png')
        cards.append(card)

        if index % 10 == 0:
            if len(cards) == 10:
                this = html.Div(cards, className='grid-row')
                deck.append(this)
            cards = []

        if len(deck) == 10:
            break


    return dbc.Jumbotron(
        [
            html.H1("Market Ahead", className="display-4"),

            html.Div([
                html.Div("Analyze price trends, correlations, and more. Explore below or search."),
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
