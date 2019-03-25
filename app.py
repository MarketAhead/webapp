from dash import Dash
from flask_caching import Cache
import dash_bootstrap_components as dbc
import os
from flask import request, redirect

from urllib.parse import urlparse, urlunparse

external_stylesheets = [dbc.themes.COSMO]

app = Dash(__name__, external_stylesheets=external_stylesheets, static_folder='static', 
           meta_tags=[
            {
                'name': 'description',
                'content': 'Analyze price trends, correlations, and more. Supports most stocks and top cryptos.'
            },
            {
            	'name':'viewport',
            	'content':'width=device-width, initial-scale=1.0'
            }
            ]
        )

app.title = 'Market Ahead'

server = app.server
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally= True
app.scripts.config.serve_locally= True

cache = Cache(app.server, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ['REDIS_URL'] 
})


@server.before_request
def enforceHttpsInHeroku():

    urlparts = urlparse(request.url)

    print('header',request.headers.get('X-Forwarded-Proto'))
    if request.headers.get('X-Forwarded-Proto') == 'http':
        url = request.url.replace('http://', 'https://', 1)

        if urlparts.netloc == 'marketahead.com':
            url = url.replace('marketahead.com', 'www.marketahead.com', 1)

        return redirect(url, code=301)

    print('urlparts',urlparts)
    if urlparts.netloc == 'marketahead.com' and urlparts.scheme == 'https':
        url = request.url.replace('marketahead.com', 'www.marketahead.com', 1)
        
        return redirect(url, code=301)