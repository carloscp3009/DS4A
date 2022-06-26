import os
import json
import plotly.express as px
import pandas as pd
import plotly.io as pio
from pathlib import Path
from dash import Input, Output, State

# create our custom_dark theme from the plotly_dark template
pio.templates["custom_dark"] = pio.templates["plotly_dark"]

# set the paper_bgcolor and the plot_bgcolor to a new color
pio.templates["custom_dark"]['layout']['paper_bgcolor'] = '#303030'
pio.templates["custom_dark"]['layout']['plot_bgcolor'] = '#303030'


ruta = Path(__file__).parent.absolute()
ruta = ruta.parent

ruta_archivo = os.path.join(ruta, "data", "AGROSAVIA.csv")
AGROSAVIA_df = pd.read_csv(ruta_archivo, dtype=str)

ruta_archivo = os.path.join(ruta, "data", "Municipios_Colombia.geojson")
with open(ruta_archivo) as file:
    geo_municipios = json.load(file, encoding="utf-8")

ruta_archivo = os.path.join(ruta, "data", "municipios_clean.csv")
DANE_df = pd.read_csv(ruta_archivo, sep="\t", dtype=str)
DANE_df.set_index("MUN_ID", inplace=True)

AGROSAVIA_df['Materia orgánica (MO) %'] = AGROSAVIA_df['Materia orgánica (MO) %'].astype(
    float)
col = 'Materia orgánica (MO) %'
organic = AGROSAVIA_df.groupby("MUN_ID")[col].mean().to_frame()
organic["Nombre"] = DANE_df.Municipio
organic.reset_index(inplace=True)

fig = px.choropleth_mapbox(
    organic,
    geojson=geo_municipios,
    locations="MUN_ID",
    color=col,
    color_continuous_scale="Viridis",
    hover_data={  # select the columns that will appear in the tooltip
        "MUN_ID": False,
        col: True,
        "Nombre": True
    },
    center={"lat": 4, "lon": -15*5},  # Colombia is GMT-5, each hour is 15°
    zoom=4.5,
    mapbox_style="carto-positron",
    height=550,
    opacity=0.9,
    range_color=organic[col].quantile([0, 0.98]).tolist(),
    template='custom_dark'
)
fig.update_layout(autosize=True, margin=dict(l=0, r=0, t=0, b=0))
fig.update_traces(marker_line_width=0)  # clear contours


# def register_callback(app):
#     @app.callback(
#         [Output(component_id='map', component_property='figure')],
#         [Input(component_id='select-feature', component_property='value')]
#     )
#     def update_graph(feature='Potasio (K) intercambiable cmol(+)/kg'):
#         AGROSAVIA_df[feature] = AGROSAVIA_df[feature].astype(float)
#         col = feature
#         data_req = AGROSAVIA_df.groupby("MUN_ID")[col].mean().to_frame()
#         data_req["Nombre"] = DANE_df.Municipio
#         data_req.reset_index(inplace=True)

#         fig.update_layout(data_frame=data_req)
map = fig
