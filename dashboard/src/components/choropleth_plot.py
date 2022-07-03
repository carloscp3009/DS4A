import os
import json
from matplotlib.pyplot import colorbar
import plotly.express as px
import pandas as pd
import plotly.io as pio
from pathlib import Path
from dash import Input, Output, State
from dash import dcc

from utils.load_data import Connection

# ------------------------------------------------------------------------------


class choropleth_plot:
    def __init__(self, variable='acidez'):
        self.label = "Análisis multivariado de outliers"
        self.datos = None
        self.variable = variable

    # --------------------------------------------------------------------------

    def figura(self):
        try:
            query = f"""
                SELECT
                    a.cod_municipio, m.municipio,
                    AVG(a.{self.variable}) as variable
                FROM
                    analisis a INNER JOIN
                    municipios m ON a.cod_municipio = m.cod_municipio
                WHERE a.{self.variable} IS NOT NULL
                GROUP BY a.cod_municipio, m.municipio
                """
            conn, cur = Connection.get_connection()
            self.datos = pd.read_sql_query(query, conn)

            ruta = Path(__file__).parent.absolute()
            ruta = ruta.parent
            ruta_archivo = os.path.join(
                ruta, "data", "Municipios_Colombia.geojson")
            with open(ruta_archivo) as file:
                geo_municipios = json.load(file, encoding="utf-8")

            fig = px.choropleth_mapbox(
                self.datos,
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
                # height=550,
                opacity=0.3,
                range_color=self.datos['variable'].quantile([0, 0.98]).tolist(),
                template='custom_dark',
            )

            fig.update_layout(autosize=True, margin=dict(l=0, r=0, t=0, b=0))
            fig.update_traces(marker_line_width=0)  # clear contours
            fig.layout.coloraxis.colorbar.title = ''
            # fig.update_geos(oceancolor='rgba(0, 0, 0, 0)')
            # fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))

        except Exception as e:
            print("figure:", e)
        return fig

    # --------------------------------------------------------------------------

    def display(self):
        layout = dcc.Graph(
            # id='id-choropleth-map',
            className="h-100 mb-2",
            figure=choropleth_plot.figura(self),
        )
        return layout
