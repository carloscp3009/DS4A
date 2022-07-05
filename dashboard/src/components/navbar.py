import dash_bootstrap_components as dbc

from dash import html, Input, Output, State, callback

from components.tabs.outliers import variable_plot, multivariable_plot
from components.central_container import my_choropleth_map
from components.tabs.statistics import crops_by_region, crops_types_by_region
from utils.load_data import (
    lstVariables, lstDepartamentos, lstZonas, Connection)

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
                dbc.Button(
                    id='btnClearHidden',
                    style=dict(display='none'))
            ],
            className="col-auto"
        )
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0 pe-4",
    align="center")

ruta_logo = 'assets/logos/logo-agrosavia-transparent.png'
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src=ruta_logo,
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
    try:
        if zona:
            query = f'''
                SELECT
                    cod_departamento, departamento
                FROM
                    departamentos
                WHERE `{zona}` = 1
                ORDER BY departamento'''
        else:
            query = '''
                SELECT cod_departamento, departamento
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
        Output('btnClearHidden', 'n_clicks'),
    ],
    [Input('btnReset', 'n_clicks')],
    prevent_initial_call=True)
def reset_filters(n_clicks):
    return ["", "", "1"]

# ------------------------------------------------------------------------------


@callback(
    [
        Output('select-municipality', 'value'),
        Output('select-municipality', 'options')
    ],
    [Input('select-deparment', 'value')],
    prevent_initial_call=True)
def update_municipalities(departamento):
    lstMunicipios = []
    try:
        if departamento:
            query = '''
                SELECT cod_municipio, municipio
                FROM municipios
                WHERE cod_departamento = '%s'
                ORDER BY municipio''' % departamento
            data = Connection.get_data(query)
            lstMunicipios = [
                {"label": row[1], "value": row[0]} for row in data]
    except Exception as e:
        print("update_municipalities:", e)
    return ["", lstMunicipios]

# ------------------------------------------------------------------------------


@callback(
    [
        Output("id-univariate-plot", "children"),
        Output("id-multivariate-plot", "children"),
        Output("id-choropleth-map", "children"),
        Output("choropleth-title", "children"),
        Output("id-crops-by-region-barplot", "children"),
        Output("id-crops-types-by-region-barplot", "children"),
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
def update_plots(zona, departamento, municipio, feature, n_clicks):
    if feature:
        variable = feature
        for item in lstVariables:
            if item['value'] == feature:
                feature_label = item['label']
                break
    else:
        variable = "acidez"
        feature_label = "Acidez"

    try:
        # General
        agregado = tipo_agregado = ""
        if municipio:
            agregado = municipio
            tipo_agregado = "cod_municipio"
        elif departamento:
            agregado = departamento
            tipo_agregado = "cod_departamento"
        elif zona:
            agregado = zona
            tipo_agregado = 'zona'
        else:
            tipo_agregado = "cod_municipio"
            # return [dash.no_update, dash.no_update]

        # Grafico de univariado de outliers
        variable_plot.agregado = agregado
        variable_plot.tipo_agregado = tipo_agregado

        variable_plot.variable = variable
        variable_plot.label = feature_label
        nuevo_grafico = variable_plot.display()

        # Gráfico multivarido de outliers
        if agregado:
            multivariable_plot.agregado = agregado
        if tipo_agregado:
            multivariable_plot.tipo_agregado = tipo_agregado

        nuevo_grafico_multivariate = multivariable_plot.display()

        # Choropleth
        my_choropleth_map.variable = variable
        my_choropleth_map.label = feature_label

        nuevo_choropleth = my_choropleth_map.display()

        # Gráfico de cultivo por región
        crops_by_region.tipo_agregado = tipo_agregado
        crops_by_region.agregado = agregado
        new_crops_by_region = crops_by_region.display()

        # Gráfico de tipo cultivo por región
        crops_types_by_region.tipo_agregado = tipo_agregado
        crops_types_by_region.agregado = agregado
        new_crops_types_by_region = crops_types_by_region.display()

    except Exception as e:
        print("update_outliers_plot:", e)
    return [
        nuevo_grafico, nuevo_grafico_multivariate, nuevo_choropleth,
        feature_label, new_crops_by_region, new_crops_types_by_region]

# ------------------------------------------------------------------------------


@callback(
    [Output('btnFiltrar', 'n_clicks')],
    [Input('btnClearHidden', 'n_clicks')],
    prevent_initial_call=True)
def reset_plots(feature):
    return ["1"]

# ------------------------------------------------------------------------------
