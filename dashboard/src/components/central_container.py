import dash_bootstrap_components as dbc
from components.tabs import tabs

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

right_col = dbc.Col(
        [
            tabs.tabs,
        ],
        id="right-col",
        className="col-md-4 offset-md-8 ps-2 h-100 mt-2",
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
