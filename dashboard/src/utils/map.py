import os
import json
from matplotlib.pyplot import colorbar
import plotly.express as px
import pandas as pd
import plotly.io as pio
from pathlib import Path
from dash import Input, Output, State

from utils.load_data import Connection

variable = "materia_organica"
query = f"""
    SELECT a.cod_municipio, m.municipio, AVG(a.{variable}) as variable
    FROM
        analisis a INNER JOIN
        municipios m ON a.cod_municipio = m.cod_municipio
    WHERE a.{variable} IS NOT NULL
    GROUP BY a.cod_municipio, m.municipio
    """
df = pd.DataFrame(
        Connection.get_data(query),
        columns=["cod_municipio", "municipio", "variable"]
    )#.reset_index(inplace=True)
# df_group = df.groupby("cod_municipio")['acidez'].mean()#.to_frame()

# create our custom_dark theme from the plotly_dark template
# pio.templates["custom_dark"] = pio.templates["plotly_dark"]
pio.templates["custom_dark"] = pio.templates["plotly_dark"]

# set the paper_bgcolor and the plot_bgcolor to a new color
pio.templates["custom_dark"]['layout']['paper_bgcolor'] = '#303030'
pio.templates["custom_dark"]['layout']['plot_bgcolor'] = '#303030'
pio.templates["custom_dark"]['layout']['geo']['bgcolor'] = '#303030'
pio.templates["custom_dark"]['layout']['geo']['lakecolor'] = '#303030'
# pio.templates["custom_dark"]['layout']['geo']['showlakes'] = False
# print(pio.templates["plotly_dark"])

ruta = Path(__file__).parent.absolute()
ruta = ruta.parent

ruta_archivo = os.path.join(ruta, "data", "AGROSAVIA.csv")
AGROSAVIA_df = pd.read_csv(ruta_archivo, dtype=str)

ruta_archivo = os.path.join(ruta, "data", "Municipios_Colombia.geojson")
with open(ruta_archivo) as file:
    geo_municipios = json.load(file, encoding="utf-8")

# ruta_archivo = os.path.join(ruta, "data", "municipios_clean.csv")
# DANE_df = pd.read_csv(ruta_archivo, sep="\t", dtype=str)
# DANE_df.set_index("MUN_ID", inplace=True)

# AGROSAVIA_df['Materia orgánica (MO) %'] = AGROSAVIA_df['Materia orgánica (MO) %'].astype(
#     float)
# col = 'Materia orgánica (MO) %'
# organic = AGROSAVIA_df.groupby("MUN_ID")[col].mean().to_frame()
# organic["Nombre"] = DANE_df.Municipio
# organic.reset_index(inplace=True)
# print(organic.head())
print("==================|")
fig = px.choropleth_mapbox(
    df,
    geojson=geo_municipios,
    locations="cod_municipio",
    color='variable',
    color_continuous_scale="Portland",
    # hover_data={  # select the columns that will appear in the tooltip
    #     "cod_municipio": False,
    #     "municipio": True
    #     'variable': True,
    # },
    center={"lat": 4, "lon": -15 * 5},  # Colombia is GMT-5, each hour is 15°
    zoom=4.5,
    # mapbox_style="carto-darkmatter",
    mapbox_style="carto-darkmatter",
    height=550,
    opacity=0.3,
    range_color=df['variable'].quantile([0, 0.98]).tolist(),
    template='custom_dark',

)
# fig.update_geos(showocean=False)
fig.update_layout(autosize=True, margin=dict(l=0, r=0, t=0, b=0))
fig.update_traces(marker_line_width=0)  # clear contours
fig.layout.coloraxis.colorbar.title = ''
fig.update_geos(oceancolor='rgba(0, 0, 0, 0)')
fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))

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
