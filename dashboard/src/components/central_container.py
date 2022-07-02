import dash_bootstrap_components as dbc
# import pandas as pd
# import numpy as np

# from dash import dcc, callback, Input, Output, State
# from utils.map import map
from components.univariate_plot import univariate_plot
from components.multivariate_plot import multivariate_plot
# from utils.load_data import lstPlots

# ------------------------------------------------------------------------------

left_col = dbc.Col(
        [
            dbc.Container(
                # dcc.Graph(
                #     id='map',
                #     figure=map,
                #     className="mt-2 h-100 mb-2",
                # ),
                # className="mt-2 h-100 mb-2",
            ),
        ],
        id="left-col",
        className="col-12 col-md-9 px-2",
    )

# ------------------------------------------------------------------------------

variable_plot = univariate_plot("acidez", "Acidez")
# multivariable_plot = multivariate_plot()
multivariable_plot = multivariate_plot("cod_municipio", "None")

right_col = dbc.Col(
        children=[
            dbc.Row(
                [
                    variable_plot.display(),
                ],
                id="id-univariate-plot",
            ),
            dbc.Row(
                [
                    multivariable_plot.display(),
                ],
                id="id-mutlivariate-plot",
                className="mt-1",
            ),
        ],
        id="right-col",
        className="col-md-3 offset-md-9 ps-2 h-100 mt-2",
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

# ------------------------------------------------------------------------------

# lstOutputs = [Output(f"id_{plot}_plot", "children") for plot in lstPlots]


# @callback(
#     lstOutputs,
#     [State('select-deparment', 'value')],
#     [Input('btnFiltrar', 'n_clicks')],
#     prevent_initial_call=True
# )
# def update_plots(departamento, n_clicks):
#     try:
#         lst = []
#         for item in lstVariables:
#             variable = item["value"]
#             eval(f"{variable}_plot").agregado = departamento
#             nuevo_grafico = eval(f"{variable}_plot").display()
#             lst.append([nuevo_grafico])
#     except Exception as e:
#         print("update_plot:", e)
#     return tuple(lst)
