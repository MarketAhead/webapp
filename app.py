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
    
    if urlparts.netloc == 'marketahead.com':
        urlparts_list = list(urlparts)
        urlparts_list[1] = 'www.marketahead.com'
        return redirect(urlunparse(urlparts_list), code=301)
    
    if request.headers.get('X-Forwarded-Proto') == 'http':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)