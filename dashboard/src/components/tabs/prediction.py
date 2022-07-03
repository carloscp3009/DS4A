import dash_bootstrap_components as dbc
from dash import html

# prediction_tab_content = dbc.Card(
#     dbc.CardBody(
#         [
#             dbc.Label("pH:"),
#             dbc.Input(id='ph-input', placeholder='pH value', type="number", min=0, max=10),

#             dbc.Label("Materia Organica:"),
#             dbc.Input(id='MO-input', placeholder='MO', type="number", min=0),

#             dbc.Button("Don't click here", color="danger"),
#         ]
#     ),
#     className="mt-3",
# )

left_col = dbc.Col(
        [
            dbc.Label("pH:"),
            dbc.Input(id='ph-input', placeholder='pH value', type="number", min=0, max=10),

            dbc.Label("Fosforo:"),
            dbc.Input(id='fosforo-input', placeholder='fosforo value', type="number", min=0),

            dbc.Label("aluminio:"),
            dbc.Input(id='aluminio-input', placeholder='aluminio value', type="number", min=0),

            dbc.Label("magnesio:"),
            dbc.Input(id='magnesio-input', placeholder='magnesio value', type="number", min=0),

            dbc.Label("sodio:"),
            dbc.Input(id='sodio-input', placeholder='sodio value', type="number", min=0),

            dbc.Label("hierro olsen:"),
            dbc.Input(id='hierro olsen-input', placeholder='hierro olsen value', type="number", min=0),

            dbc.Label("manganeso:"),
            dbc.Input(id='manganeso-input', placeholder='manganeso value', type="number", min=0),

            dbc.Label("boro:"),
            dbc.Input(id='boro-input', placeholder='boro value', type="number", min=0),

            dbc.Label("Tiempo establecimiento:"),
            dbc.Select(id="tiempo-select",
            options=[
                {"label": "Tiempo Establecimiento", "value": "0", "disabled": True},
                {"label": "0 a 1 año", "value": "1"},
                {"label": "1 a 5 años", "value": "2"},
                {"label": "5 a 10 años", "value": "3"},
                {"label": "más de 10 años", "value": "4"},
            ],
            value='0'
            ),

            dbc.Label("Drenaje:"),
            dbc.Select(id="drenaje-select",
            options=[
                {"label": "Drenaje", "value": "0", "disabled": True},
                {"label": "Bueno", "value": "1"},
                {"label": "Malo", "value": "2"},
                {"label": "Muy bueno", "value": "3"},
                {"label": "No indica", "value": "4"},
                {"label": "Regular", "value": "5"},
            ],
            value='0'
            ),

            dbc.Label("Riego:"),
            dbc.Select(id="riego-select",
            options=[
                {"label": "Riego", "value": "0", "disabled": True},
                {"label": "Aspersión", "value": "1"},
                {"label": "Cañon", "value": "2"},
                {"label": "Goteo", "value": "3"},
                {"label": "Gravedad", "value": "4"},
                {"label": "Manguera", "value": "5"},
                {"label": "Microaspersión", "value": "6"},
                {"label": "No cuenta", "value": "7"},
                {"label": "No indica", "value": "8"},
                {"label": "Por inundación", "value": "9"},
            ],
            value='0'
            ),
        ],
        id="left-col-pred",
        className="p-3",
)
right_col = dbc.Col(
        [
            dbc.Label("Materia Organica:"),
            dbc.Input(id='MO-input', placeholder='MO', type="number", min=0),

            dbc.Label("azufre:"),
            dbc.Input(id='azufre-input', placeholder='azufre value', type="number", min=0),

            dbc.Label("calcio:"),
            dbc.Input(id='calcio-input', placeholder='calcio value', type="number", min=0),

            dbc.Label("potasio:"),
            dbc.Input(id='potasio-input', placeholder='potasio value', type="number", min=0),

            dbc.Label("Conductividad electrica:"),
            dbc.Input(id='ce-input', placeholder='ce value', type="number", min=0),

            dbc.Label("cobre:"),
            dbc.Input(id='cobre-input', placeholder='cobre value', type="number", min=0),

            dbc.Label("zinc-olsen:"),
            dbc.Input(id='zinc-olsen-input', placeholder='zinc-olsen value', type="number", min=0),

            dbc.Label("Municipio id:"),
            dbc.Input(id='geo-input', placeholder='Municipio id from map', type="number", min=0, max=10000),

            dbc.Label("Estado:"),
            dbc.Select(id="estado-select",
            options=[
                {"label": "Estado", "value": "0", "disabled": True},
                {"label": "Establecido", "value": "1"},
                {"label": "Por Establecer", "value": "2"},
                {"label": "No indica", "value": "3"},
            ],
            value='0'
            ),

            dbc.Label("Topografia:"),
            dbc.Select(id="topografia-select",
            options=[
                {"label": "Topografia", "value": "0", "disabled": True},
                {"label": "Ligeramente ondulado", "value": "1"},
                {"label": "Moderadamente ondulado", "value": "2"},
                {"label": "No indica", "value": "3"},
                {"label": "Ondulado", "value": "4"},
                {"label": "Pendiente", "value": "5"},
                {"label": "Pendiente Fuerte", "value": "6"},
                {"label": "Pendiente leve", "value": "7"},
                {"label": "Pendiente moderada", "value": "8"},
                {"label": "Plano", "value": "9"},
            ],
            value='0'
            ),
        ],
        id="right-col-pred",
        className="p-3",
)

prediction_tab_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Row(
                        [
                            left_col,
                            right_col,
                        ],
                        className="w-100",
                    ),
                    dbc.Row(
                        dbc.Button(
                            "Predecir",
                            color="primary"
                        ),

                        className="w-100",
                    ),
                ],
                id="prediction-container",
            ),
        ],
    ),
    id="prediction-card",

)
