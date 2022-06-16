import json
from dash import Dash, dcc, html, Input, Output, State
# from numpy import deprecate_with_doc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


AGROSAVIA_df = pd.read_csv("../data/AGROSAVIA.csv",dtype=str)

with open("../data/Municipios_Colombia.geojson") as file:
    geo_municipios = json.load(file)
    
DANE_df = pd.read_csv("../data/municipios_clean.csv",sep="\t",dtype=str)
DANE_df.set_index("MUN_ID",inplace=True)
# print(AGROSAVIA_df.columns)
# print(AGROSAVIA_df.info())



AGROSAVIA_df['Materia orgánica (MO) %'] = AGROSAVIA_df['Materia orgánica (MO) %'].astype(float)
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
    hover_data = { # select the columns that will appear in the tooltip
        "MUN_ID":False,
        col:True,
        "Nombre":True
    },
    center = {"lat":4,"lon":-15*5}, # Colombia is GMT-5, each hour is 15°
    zoom=4,
    mapbox_style="carto-positron",
    height=550,
    opacity=1,
    range_color = organic[col].quantile([0,0.98]).tolist()
)
# fig.update_layout(margin=dict(l=100, r=100, t=100, b=100))
fig.update_traces(marker_line_width=0) # clear contours

map = fig