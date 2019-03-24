import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app

LOGO = '/static/marketahead_logo.png'

search = dbc.Input(type="text", placeholder="Ticker", id="search", 
                   style={"border-radius":".25rem"},
                   className= 'full-width'
                   )

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="40px")),
                        dbc.Col(dbc.NavbarBrand("", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/",
            ),

            dbc.Nav(
                    [search], className="ml-auto", navbar=True
            ),
            # dbc.NavbarToggler(id="navbar-toggler2"),
            # dbc.Collapse(
            #     dbc.Nav(
            #         [search], className="ml-auto", navbar=True
            #     ),
            #     id="navbar-collapse2",
            #     navbar=True,
            # ),
        ]
    ),
    color="light",
    dark=False,
    className="border-bottom",
)

# # we use a callback to toggle the collapse on small screens
# def toggle_navbar_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# # the same function (toggle_navbar_collapse) is used in all three callbacks
# for i in [1, 2, 3]:
#     app.callback(
#         Output(f"navbar-collapse{i}", "is_open"),
#         [Input(f"navbar-toggler{i}", "n_clicks")],
#         [State(f"navbar-collapse{i}", "is_open")],
#     )(toggle_navbar_collapse)
