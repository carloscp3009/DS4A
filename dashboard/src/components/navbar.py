from dash import html, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
from utils.load_data import (
    lstVariables,
    lstDepartamentos,
    lstZonas,
    lstPlots,

    Connection)
from components.central_container import variable_plot, multivariable_plot
# (
    # acidez_plot,
    # aluminio_plot, azufre_plot, boro_plot, calcio_plot, ce_plot, cice_plot, cobre_plot, cobre_doble_acido_plot, fosforo_plot, hierro_doble_acido_plot, hierro_olsen_plot, magnesio_plot, manganeso_plot, manganeso_doble_acido_plot, materia_organica_plot, ph_plot, potasio_plot, sodio_plot, zinc_olsen_plot
    # )

# ------------------------------------------------------------------------------

filters_bar = dbc.Row(
    [
        dbc.Col(
            dbc.Select(
                id="select-zone",
                options=lstZonas,
                placeholder='Zona'
            ),
            className="ps-2"
        ),
        dbc.Col(
            dbc.Select(
                id="select-deparment",
                options=lstDepartamentos,
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
            query = '''
                SELECT
	                departamentos.codigo, departamentos.departamento
                FROM
	                departamentos INNER JOIN
	                zonas_departamentos ON departamentos.codigo = zonas_departamentos.cod_departamento
                WHERE zonas_departamentos.cod_zona='%s'
                ORDER BY departamentos.departamento''' % zona
        else:
            query = '''
                SELECT codigo, departamento
                FROM departamentos
                ORDER BY departamento'''
        data = Connection.get_data(query)
        lstDepartamentos = [{"label": row[1], "value": row[0]} for row in data]
    except Exception as e:
        print("update_deparments:", e)
    return ["", lstDepartamentos]

# ------------------------------------------------------------------------------


@callback(
    [
        Output('select-zone', 'value'),
        Output('select-feature', 'value'),
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
            query = '''
                SELECT codigo, municipio
                FROM municipios
                WHERE cod_departamento = '%s'
                ORDER BY municipio''' % departamento
        else:
            query = '''
                SELECT codigo, municipio
                FROM municipios
                ORDER BY municipio'''
        data = Connection.get_data(query)
        lstMunicipios = [{"label": row[1], "value": row[0]} for row in data]
    except Exception as e:
        print("update_municipalities:", e)
    return ["", lstMunicipios]

# ------------------------------------------------------------------------------




@callback(
    [
        Output("id-univariate-plot", "children"),
        Output("id-mutlivariate-plot", "children")
    ],
    [
        State('select-zone', 'value'),
        State('select-deparment', 'value'),
        State('select-municipality', 'value'),
        State('select-feature', 'value'),
    ],
    [Input('btnFiltrar', 'n_clicks')],
    prevent_initial_call=True
)
def update_variable_plot(
                    zona, departamento, municipio, feature, n_clicks):
    try:
        agregado = tipo_agregado = ""
        if municipio:
            agregado = municipio
            tipo_agregado = "cod_municipio"
        elif departamento:
            agregado = departamento
            tipo_agregado = "cod_departamento"
        elif zona:
            agregado = zona
            tipo_agregado = "cod_zona"
        else:
            agregado = None
            tipo_agregado = "departamento"

        variable_plot.agregado = agregado
        variable_plot.tipo_agregado = tipo_agregado
        variable_plot.variable = feature if feature else 'acidez'
        for item in lstVariables:
            if item['value'] == feature:
                variable_plot.label = item['label']
                break
        nuevo_grafico = variable_plot.display()

        # ----------------------------------------------------------------------

        multivariable_plot.agregado = agregado
        multivariable_plot.tipo_agregado = tipo_agregado
        # multivariable_plot.variable = feature if feature else 'acidez'
        # for item in lstVariables:
            # if item['value'] == feature:
                # multivariable_plot.label = item['label']
                # break
        nuevo_grafico_multivariate = multivariable_plot.display()

    except Exception as e:
        print("update_variable_plot:", e)
    return [nuevo_grafico, nuevo_grafico_multivariate]


# ------------------------------------------------------------------------------


# @callback(
#     [Output('btnFiltrar', 'n_clicks')],
#     [Input('select-feature', 'value')],
#     prevent_initial_call=True)
# def reset_plots(feature):
#     if feature == "":
#         return ["1"]
#     return [0]

# ------------------------------------------------------------------------------
