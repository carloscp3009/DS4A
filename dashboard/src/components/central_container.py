import dash_bootstrap_components as dbc
import pandas as pd

from dash import dcc
from utils.map import map
from components.univariate_plot import univariate_plot

# ------------------------------------------------------------------------------

df = pd.read_csv('data/suelos_preprocesado.csv')

# ------------------------------------------------------------------------------

left_col = dbc.Col(
        [
            dbc.Container(
                dcc.Graph(
                    id='map',
                    figure=map,
                    className="mt-2 h-100 mb-2",
                ),
                className="mt-2 h-100 mb-2",
            ),
        ],
        id="left-col",
        className="col-12 col-md-9 h-100",
    )

# ------------------------------------------------------------------------------
grafico_1 = univariate_plot(df, 'cundinamarca', 'azufre')
grafico_2 = univariate_plot(df, 'cundinamarca', 'materia_organica')
grafico_3 = univariate_plot(df, 'cundinamarca', 'aluminio')

right_col = dbc.Col(
        [
            dbc.Row(grafico_1.display()),
            dbc.Row(grafico_2.display()),
            dbc.Row(grafico_3.display()),
        ],
        id="right-col",
        className="col-md-3 .d-sm-none .d-md-block ps-2 h-100",
    )

# ------------------------------------------------------------------------------

central_container = dbc.Container(
        [
            left_col,
            right_col,
        ],
        id="central-container",
        className="g-0 ms-auto flex-nowrap row pb-2",
    )
