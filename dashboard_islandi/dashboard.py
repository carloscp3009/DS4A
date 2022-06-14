# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from tkinter.tix import Select
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Input, Output, State

# app = Dash(__name__)
app = Dash(external_stylesheets=["assets/bootstrap.min.css"])

filters_bar = dbc.Row(
    [
        dbc.Col(
            dbc.Select(
                id="select-zone",
                options=[
                    {"label": "Option 1", "value": "1"},
                    {"label": "Option 2", "value": "2"},
                    {"label": "Disabled option", "value": "3", "disabled": True},
                ],
                placeholder='Zona'
            )
        ),
        dbc.Col(
            dbc.Select(
                id="select-deparment",
                options=[
                    {"label": "Option 1", "value": "1"},
                    {"label": "Option 2", "value": "2"},
                    {"label": " option", "value": "3", "disabled": True},
                ],
                placeholder='Departamento'
            )
        ),
        dbc.Col(
            dbc.Select(
                id="select-municipality",
                options=[
                    {"label": "Option 1", "value": "1"},
                    {"label": "Option 2", "value": "2"},
                    {"label": " option", "value": "3", "disabled": True},
                ],
                placeholder='Municipio'
            )
        ),
        dbc.Col(
            dbc.Select(
                id="select-feature",
                options=[
                    {"label": "Option 1", "value": "1"},
                    {"label": "Option 2", "value": "2"},
                    {"label": " option", "value": "3", "disabled": True},
                ],
                placeholder='Variable de interés'
            )
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0 pe-4",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src='assets/logo-agrosavia-transparent.png',
                                height="30px")),
                        # dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
                    ], align="center", className="g-0",
                ),
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                filters_bar, id="navbar-collapse", is_open=False, navbar=True,
            ),
        ]
    ), color="dark", dark=True,
)


left_container = dbc.Col(
        [
            dbc.Container(
                dbc.Card(
                    dbc.CardBody("aquí es donde va el mapa"),
                    className="mt-2",
                    style={"height": "600px"},
                ),
            ),
        ],
        className="col-12 col-md-9",
    )

right_container = dbc.Col(
        [
            dbc.Container(
                dbc.Card(
                    dbc.CardBody("aquí es donde vanlos gráficos"),
                    className="mt-2",
                    style={"height": "600px"},
                ),
            ),
        ],
        className="col-md-3 .d-sm-none .d-md-block ps-2",
    )

app.layout = dbc.Container(
    children=[
        navbar,
        dbc.Container(
            [
                left_container,
                right_container,
            ],
            className="g-0 ms-auto flex-nowrap row",
        ),
    ]
)


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)