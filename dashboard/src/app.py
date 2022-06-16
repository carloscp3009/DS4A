# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
# from tkinter.tix import Select
# from dash import Dash, dcc, html, Input, Output, State
# from numpy import deprecate_with_doc
# import plotly.express as px

from components.navbar import navbar
from components.central_container import central_container
from components.footer import footer
from utils.map import map
from utils.static_data import features


# df = pd.read_csv('/data/suelos_preprocesado.csv')

app = Dash(__name__)

# ------------------------------------------------------------------------------
# App layout
# ------------------------------------------------------------------------------
app.layout = dbc.Container(
    children=[
        navbar,
        central_container,
        footer,
    ],
    id="main-container",
)

# ------------------------------------------------------------------------------
# Callbacks
# ------------------------------------------------------------------------------
# Add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# ------------------------------------------------------------------------------
# Run the Dash app
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
