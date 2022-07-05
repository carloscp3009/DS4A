import os
import json
import plotly.express as px
import pandas as pd
from pathlib import Path
from dash import dcc

from utils.load_data import Connection

# ------------------------------------------------------------------------------


class choropleth_plot:
    def __init__(self, variable='acidez'):
        self.label = "Análisis multivariado de outliers"
        self.datos = None
        self.variable = variable
        self.label = variable.capitalize()

    # --------------------------------------------------------------------------

    def figura(self):
        try:
            query = f"""
                SELECT
                    a.cod_municipio, m.municipio,
                    AVG(a.{self.variable}) AS `{self.label}`
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
                color=self.label,
                color_continuous_scale="Portland",
                hover_name="municipio",
                hover_data={
                    "cod_municipio": False,
                    "municipio": False,
                    f"{self.label}": True,
                },
                # Colombia is GMT-5, each hour is 15°
                center={"lat": 4, "lon": -15 * 5},
                zoom=4.5,
                mapbox_style="carto-positron",
                opacity=0.4,
                range_color=self.datos[self.label].quantile(
                    [0, 0.98]).tolist(),
            )

            fig.update_layout(paper_bgcolor='#303030', plot_bgcolor='#303030')

            fig.update_layout(autosize=True, margin=dict(l=0, r=0, t=0, b=0))
            fig.update_traces(
                marker=dict(
                    line=dict(
                        width=1,
                        color='rgba(0, 0, 0, 0.1)'
                    )
                ),
            )
            fig.layout.coloraxis.colorbar.title = ''

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
