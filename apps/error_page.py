import dash_bootstrap_components as dbc
import dash_html_components as html

error = dbc.Jumbotron(
    [
        html.H1("🤭 Oops", className="display-3 text-center"),
        html.P(
            "Couldn't find that ticker",
            className="lead text-center",
        ),
    ]
)

errorfof = dbc.Jumbotron(
    [
        html.H1("🤭 404", className="display-3 text-center"),
        html.P(
            "Couldn't find that page",
            className="lead text-center",
        ),
    ]
)