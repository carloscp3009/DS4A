import dash_bootstrap_components as dbc

from dash import dcc
from utils.map import map

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

right_col = dbc.Col(
        [
            dbc.Container(
                dbc.Card(
                    dbc.CardBody("aquí es donde vanlos gráficos"),
                    className="mt-2 h-100",
                ),
                className="h-100",
            ),
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
