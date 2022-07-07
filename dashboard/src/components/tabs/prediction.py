import dash_bootstrap_components as dbc
from dash import html, State, callback, Input, Output
import sqlite3
from utils.load_data import (lstVariables, lstDepartamentos, lstZonas, Connection)
import os
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
import xgboost
import operator


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
ruta = Path(__file__).parent.parent.absolute()
ruta = os.path.join(ruta.parent, "assets", "modelo_entrenado.pkl")
xgboost = joblib.load(ruta) 

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

            dbc.Label("hierro_olsen:"),
            dbc.Input(id='hierro_olsen-input', placeholder='hierro_olsen value', type="number", min=0),

            dbc.Label("manganeso:"),
            dbc.Input(id='manganeso-input', placeholder='manganeso value', type="number", min=0),

            dbc.Label("boro:"),
            dbc.Input(id='boro-input', placeholder='boro value', type="number", min=0),

            dbc.Label("Tiempo establecimiento:"),
            dbc.Select(id="tiempo-select",
            options=[
                {"label": "Tiempo Establecimiento", "value": "0", "disabled": True},
                {"label": "0 a 1 año", "value": "0 a 1 año"},
                {"label": "1 a 5 años", "value": "1 a 5 años"},
                {"label": "5 a 10 años", "value": "5 a 10 años"},
                {"label": "más de 10 años", "value": "más de 10 años"},
                {"label": "No aplica", "value": "No aplica"},
                {"label": "No indica", "value": "No indica"},
            ],
            value='0'
            ),

            dbc.Label("Drenaje:"),
            dbc.Select(id="drenaje-select",
            options=[
                {"label": "Drenaje", "value": "0", "disabled": True},
                {"label": "Bueno", "value": "Bueno"},
                {"label": "Malo", "value": "Malo"},
                {"label": "Muy bueno", "value": "Muy bueno"},
                {"label": "No indica", "value": "No indica"},
                {"label": "Regular", "value": "Regular"},
            ],
            value='0'
            ),

            dbc.Label("Riego:"),
            dbc.Select(id="riego-select",
            options=[
                {"label": "Riego", "value": "0", "disabled": True},
                {"label": "Aspersión", "value": "Aspersión"},
                {"label": "Cañon", "value": "Cañon"},
                {"label": "Goteo", "value": "Goteo"},
                {"label": "Gravedad", "value": "Gravedad"},
                {"label": "Manguera", "value": "Manguera"},
                {"label": "Microaspersión", "value": "Microaspersión"},
                {"label": "No cuenta", "value": "No cuenta"},
                {"label": "No indica", "value": "No indica"},
                {"label": "Por inundación", "value": "Por inundación"},
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

            dbc.Label("zinc_olsen:"),
            dbc.Input(id='zinc_olsen-input', placeholder='zinc_olsen value', type="number", min=0),

            dbc.Label("Departamento:"),
            dbc.Select(
                id="dpto-select",
                options=lstDepartamentos,
                placeholder='Departamento'
            ),
            
            dbc.Label("Municipio:"),
            dbc.Select(
                id="mun-select",
                options=[],
                placeholder='Municipio'
            ),

            dbc.Label("Estado:"),
            dbc.Select(id="estado_select",
            options=[
                {"label": "Estado", "value": "0", "disabled": True},
                {"label": "Establecido", "value": "Establecido"},
                {"label": "No indica", "value": "No indica"},
                {"label": "Por Establecer", "value": "Por Establecer"},
            ],
            value='0'
            ),

            dbc.Label("Topografia:"),
            dbc.Select(id="topografia-select",
            options=[
                {"label": "Topografia", "value": "0", "disabled": True},
                {"label": "Ligeramente ondulado", "value": "Ligeramente ondulado"},
                {"label": "Moderadamente ondulado", "value": "Moderadamente ondulado"},
                {"label": "No indica", "value": "No indica"},
                {"label": "Ondulado", "value": "Ondulado"},
                {"label": "Pendiente", "value": "Pendiente"},
                {"label": "Pendiente Fuerte", "value": "Pendiente Fuerte"},
                {"label": "Pendiente leve", "value": "Pendiente leve"},
                {"label": "Pendiente moderada", "value": "Pendiente moderada"},
                {"label": "Plano", "value": "Plano"},
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
                    dbc.Row([
                        dbc.Button(
                            "Predecir",
                            id="prediction-button",
                            color="primary",
                            n_clicks=0
                        ),
                        html.Br(),
                        html.P(id="prediction-result", className="p-1 text-center mt-2"),
                    ],
                        className="w-100",
                    ),
                ],
                id="prediction-container",
            ),
        ],
    ),
    id="prediction-card",

)

estado_ops = {"Establecido":[1, 0, 0], "Por Establecer":[0, 1, 0], "No indica":[0, 0, 1]}
tiempo_ops = {
    "0 a 1 año" : [1,0,0,0,0,0],
    "1 a 5 años" : [0,1,0,0,0,0],
    "5 a 10 años" : [0,0,1,0,0,0],
    "más de 10 años" : [0,0,0,1,0,0],
    "No aplica" : [0,0,0,0,1,0],
    "No indica" : [0,0,0,0,0,1]
}
topografia_ops = {    
    "Ligeramente ondulado" :[1,0,0,0,0,0,0,0,0],
    "Moderadamente ondulado" :[0,1,0,0,0,0,0,0,0],
    "No indica" :[0,0,1,0,0,0,0,0,0],
    "Ondulado" :[0,0,0,1,0,0,0,0,0],
    "Pendiente" :[0,0,0,0,1,0,0,0,0],
    "Pendiente Fuerte" :[0,0,0,0,0,1,0,0,0],
    "Pendiente leve" :[0,0,0,0,0,0,1,0,0],
    "Pendiente moderada" :[0,0,0,0,0,0,0,1,0],
    "Plano" :[0,0,0,0,0,0,0,0,1]
}
drenaje_ops = {
    "Bueno" : [1,0,0,0,0],
    "Malo" : [0,1,0,0,0],
    "Muy bueno" : [0,0,1,0,0],
    "No indica" : [0,0,0,1,0],
    "Regular" : [0,0,0,0,1]
}
riego_ops = {
    "Aspersión" : [1,0,0,0,0,0,0,0,0],
    "Cañon" : [0,1,0,0,0,0,0,0,0],
    "Goteo" : [0,0,1,0,0,0,0,0,0],
    "Gravedad" : [0,0,0,1,0,0,0,0,0],
    "Manguera" : [0,0,0,0,1,0,0,0,0],
    "Microaspersión" : [0,0,0,0,0,1,0,0,0],
    "No cuenta" : [0,0,0,0,0,0,1,0,0],
    "No indica" : [0,0,0,0,0,0,0,1,0],
    "Por inundación" : [0,0,0,0,0,0,0,0,1]
}
crops = ['Aguacate', 'Arroz', 'Cacao', 'Café', 'Caucho', 'Caña de azucar',
       'Citricos', 'Frijol', 'Lulo', 'Maracuyá', 'Maíz', 'Millo', 'Mora',
       'Palma de aceite', 'Papa de año', 'Pastos', 'Pastos-kikuyo',
       'Piña', 'Plátano', 'Uva']

# --- Callbacks --- #
@callback(
    [Output("prediction-result", "children")],
    [
    State('ph-input', "value"),
    State("MO-input", "value"),
    State('fosforo-input', "value"),
    State("azufre-input", "value"),
    State('aluminio-input', "value"),
    State("calcio-input", "value"),
    State('magnesio-input', "value"),
    State("potasio-input", "value"),
    State('sodio-input', "value"),
    State("ce-input", "value"),
    State('hierro_olsen-input', "value"),
    State("cobre-input", "value"),
    State('manganeso-input', "value"),
    State("zinc_olsen-input", "value"),
    State('boro-input', "value"),

    State("estado_select", "value"),
    State("tiempo-select", "value"),
    State("topografia-select", "value"),
    State("drenaje-select", "value"),
    State("riego-select", "value"),

    State("dpto-select", "value"),
    State("mun-select", "value"),
    
    ],
    [Input("prediction-button", "n_clicks")],
    prevent_initial_call=True
)
def predict(ph, MO, fosforo, azufre, aluminio, calcio, magnesio, potasio, sodio, ce, hierro_olsen, cobre, manganeso, zinc_olsen, boro, estado_select, tiempo, topografia, drenaje, riego, dpto, mun, clicks):
    # print(ph, MO, fosforo, azufre, aluminio, calcio, magnesio, potasio, sodio, ce, hierro_olsen, cobre, manganeso, zinc_olsen, boro, estado_select, tiempo, topografia, drenaje, riego, geo)
    try:
        if mun:
            query = '''
                SELECT latitud, longitud, altitud
                FROM municipios
                WHERE cod_municipio = '%s'
                ''' % mun
            data = Connection.get_data(query)
            geo = list(data[0])
            # print(f'Geo Data: {list(data[0])} - {type(list(data[0]))}')
    except Exception as e:
        print("No Geo Data Found:", e)
        geo = [6.25, -75, 2070]
    
    new_sample = pd.DataFrame(np.array([[ph, MO, fosforo, azufre, aluminio, calcio, magnesio, potasio, sodio, ce, hierro_olsen, cobre, manganeso, zinc_olsen, boro, 
                                    *estado_ops[estado_select], *tiempo_ops[tiempo], *topografia_ops[topografia], *drenaje_ops[drenaje], *riego_ops[riego], *geo]])).astype(float)
    

    predicted_crop = xgboost.predict(new_sample)
    probabilidades = xgboost.predict_proba(new_sample)
    cont=0
    val={}
    for prob in probabilidades[0]:
        val[crops[cont]]=prob
        cont=cont+1
    sortedDict = sorted(val.items(), key=operator.itemgetter(1))
    cultivos=[]
    cultivos.append(sortedDict[15:20][4][0])
    cultivos.append(sortedDict[15:20][3][0])
    cultivos.append(sortedDict[15:20][2][0])
    cultivos.append(sortedDict[15:20][1][0])
    cultivos.append(sortedDict[15:20][0][0])
    # print(probabilidades)
    # print(cultivos)
    cadena = [html.H5("Top Cultivo Sugeridos :"), 
            "1. ", cultivos[0],html.Br(), 
            "2. ", cultivos[1],html.Br(), 
            "3. ", cultivos[2],html.Br(), 
            "4. ", cultivos[3],html.Br(), 
            "5. ", cultivos[4]
            ] 
    print(cadena)
    return [cadena]

    # return [f"Cultivo Sugerido : {crops[predicted_crop[0]]}"]
# (ph, MO, fosforo, azufre, aluminio, calcio, magnesio, potasio, sodio, ce, hierro_olsen, cobre, manganeso, zinc_olsen, boro, estado_select, tiempo, topografia, drenaje, riego, geo)

# ------------------------------------------------------------------------------

@callback(
    [
        Output('mun-select', 'value'),
        Output('mun-select', 'options')
    ],
    [Input('dpto-select', 'value')],
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