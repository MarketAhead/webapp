import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from apps import performance_page, fred_page, gtrend_page, fractal_page, navbar
from apps import home_page, error_page

import re

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar.navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'),
                Input('search', 'n_submit')],
                [State('search', 'value')]
            )
def display_page(pathname, ns1, search):

    print('pathname',pathname, 'search', search)

    if (pathname is None or pathname == '/') and search is None:
        return home_page.get_home()

    elif search is not None and pathname == '/':
        return fred_page.get_page(search)

    elif pathname is not None:
        path = re.split('/', pathname.strip('/'))

        if search is not None:
            if path[0] == "c":
                return fred_page.get_page(search.upper())
            if path[0] == "f":
                return fractal_page.get_page(search.upper())
            if path[0] == "p":
                return performance_page.get_page(search.upper())
            if path[0] == "g":
                return gtrend_page.get_page(search.upper())
        else:
            if path[0] == "f":
                return fractal_page.get_page(path[1].upper())
            if path[0] == "p":
                return performance_page.get_page(path[1].upper())
            if path[0] == "c":
                return fred_page.get_page(path[1].upper())
            if path[0] == "g":
                return gtrend_page.get_page(path[1].upper())

    return error_page.errorfof

@app.callback(Output('url', 'pathname'), [Input('search', 'n_submit')], [State('search', 'value')])
def update_pathname(ns, search):
    if search is not None:
        return '/c/{}'.format(str(search).upper())


if __name__ == '__main__':
    app.run_server(debug=True)