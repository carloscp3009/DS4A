from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc
from zmq import OUT_BATCH_SIZE
from utils.load_data import lstVariables, lstDepartamentos, lstZonas

# ------------------------------------------------------------------------------

filters_bar = dbc.Row(
    [
        dbc.Col(
            dbc.Select(
                id="select-zone",
                options=[
                    {"label": v.get("zona"), "value": k}
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
                    {"label": v.get("departamento"), "value": k}
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
                html.I(className="fas fa-check"),
                id="btnFiltrar",
                className="ms-1"
            ),
            dbc.Button(
                html.I(className="fas fa-arrow-rotate-left"),
                id="btnReset",
                color="danger",
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
    lst = []
    try:
        if zona:
            departamentos = lstZonas.get(zona).get("departamentos")
            for departamento in departamentos:
                obj = lstDepartamentos[departamento]
                lst.append(
                    {
                        "label": obj["departamento"],
                        "value": departamento})
        else:
            lst = [
                {"label": v.get("departamento"), "value": k}
                    for k, v in lstDepartamentos.items()
            ]
    except Exception as e:
        print("update_deparments:", e)
    return ["", lst]

# agregar callback para el botrón btnReset que borre el contenido de value en select-deparment, select-municipality y select-feature y select-zone
@callback(
    [
        Output('select-zone', 'value')
    ],
    [Input('btnReset', 'n_clicks')],
    prevent_initial_call=True
)
def reset_filters(n_clicks):
    return [""]
