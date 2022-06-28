from dash import html, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
from utils.load_data import (
    lstVariables,
    lstDepartamentos,
    lstZonas,
    lstPlots,
    Connection)
from components.central_container import (
    acidez_plot, aluminio_plot, azufre_plot, boro_plot, calcio_plot, ce_plot, cice_plot, cobre_plot, cobre_doble_acido_plot, fosforo_plot, hierro_doble_acido_plot, hierro_olsen_plot, magnesio_plot, manganeso_plot, manganeso_doble_acido_plot, materia_organica_plot, ph_plot, potasio_plot, sodio_plot, zinc_olsen_plot)

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
                options=[],
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
        dbc.Col(
            [
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
            ],
            className="col-auto"
        )
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0 pe-4",
    align="center")

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

# ------------------------------------------------------------------------------


@callback(
    [
        Output('select-deparment', 'value'),
        Output('select-deparment', 'options')
    ],
    [Input('select-zone', 'value')],
    prevent_initial_call=True)
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

# ------------------------------------------------------------------------------


@callback(
    [
        Output('select-zone', 'value'),
        Output('select-feature', 'value')
    ],
    [Input('btnReset', 'n_clicks')],
    prevent_initial_call=True)
def reset_filters(n_clicks):
    return ["", ""]

# ------------------------------------------------------------------------------


@callback(
    [
        Output('select-municipality', 'value'),
        Output('select-municipality', 'options')
    ],
    [Input('select-deparment', 'value')],
    prevent_initial_call=True)
def update_municipalities(departamento):
    lst = []
    try:
        if departamento:
            codigo = lstDepartamentos[departamento]["codigo"]
            query = (
                'SELECT codigo, municipio '
                'FROM municipios '
                'WHERE departamento = %s' % codigo)
            data = Connection.get_data(query)
            for row in data:
                lst.append({"label": row[1], "value": row[0]})
    except Exception as e:
        print("update_municipalities:", e)
    return ["", lst]

# ------------------------------------------------------------------------------


lstOutputs = [Output(f"id_{plot}_plot", "children") for plot in lstPlots]


@callback(
    lstOutputs,
    [
        State('select-zone', 'value'),
        State('select-deparment', 'value'),
        State('select-municipality', 'value'),
        State('select-feature', 'value'),
    ],
    [Input('btnFiltrar', 'n_clicks')],
    prevent_initial_call=True
)
def update_plots(zona, departamento, municipio, feature, n_clicks):
    try:
        agregado = tipo_agregado = ""
        if municipio:
            agregado = municipio
            tipo_agregado = "municipio"
        elif departamento:
            agregado = departamento
            tipo_agregado = "departamento"
        elif zona:
            agregado = zona
            tipo_agregado = "zona"
        else:
            return [no_update for i in range(len(lstOutputs))]
        lst = []
        for item in lstVariables:
            variable = item["value"]
            eval(f"{variable}_plot").agregado = agregado
            eval(f"{variable}_plot").tipo_agregado = tipo_agregado
            nuevo_grafico = eval(f"{variable}_plot").display()
            lst.append([nuevo_grafico])
    except Exception as e:
        print("update_plots:", e)
    return tuple(lst)
