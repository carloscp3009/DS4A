from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc
from zmq import OUT_BATCH_SIZE
from utils.load_data import lstVariables, lstDepartamentos, lstZonas

# lst = []
# for k, v in lstDepartamentos.items():
#     lst.append({"label": v.get("descripcion"), "value": k})


filters_bar = dbc.Row(
    [
        dbc.Col(
            dbc.Select(
                id="select-zone",
                options=[
                    {"label": v.get("descripcion"), "value": k}
                    for k, v in lstZonas.items()
                ],
                placeholder='Zona'
            ),
            className="ps-2"
        ),
        dbc.Col(
            dbc.Select(
                id="select-deparment",
                options=[
                    {"label": v.get("descripcion"), "value": k}
                    for k, v in lstDepartamentos.items()
                ],
                placeholder='Departamento'
            ),
            className="ps-2"
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
            ),
            className="ps-2"
        ),
        dbc.Col(
            dbc.Select(
                id="select-feature",
                options=lstVariables,
                placeholder='Variable'
            ),
            className="ps-2"
        ),
        dbc.Col([
            dbc.Button(
                ["Filtrar"],
                id="btnFiltrar",
                className="ms-1"
            ),
            dbc.Button(
                ["Reset"],
                id="reset",
                className="ms-1",
            ),
        ])
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
                                src='assets/logos/logo-agrosavia-transparent.png',
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
    ),
    className="fixed-top",
    color="dark",
    dark=True,
)


@callback(
    [
        Output('select-deparment', 'value'),
        Output('select-deparment', 'options')
    ],
    [Input('select-zone', 'value')],
    prevent_initial_call=True
)
def update_deparments(zona):
    try:
        departamentos = lstZonas.get(zona).get("departamentos")
        lst = []
        for departamento in departamentos:
            obj = lstDepartamentos[departamento]
            lst.append({"label": obj["descripcion"], "value": departamento})
    except Exception as e:
        print("update_deparments:", e)
    return ["", lst]
