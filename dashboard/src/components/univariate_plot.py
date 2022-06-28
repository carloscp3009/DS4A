from turtle import bgcolor
from dash import html, dcc
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc

from utils.load_data import df

# ------------------------------------------------------------------------------


class univariate_plot:
    def __init__(self, variable, titulo, tipo_agregado=None, agregado=None):
        """Constructs all the attributes for kpiplot class"""
        self.label = titulo
        self.tipo_agregado = tipo_agregado
        self.agregado = agregado
        self.variable = variable

        self.datos = df[['departamento', 'municipio', variable]].copy()
        self.datos.dropna(subset=[variable], inplace=True)

    @staticmethod
    def figura(self):
        try:
            self.datos['outlier'] = False
            if self.agregado and self.tipo_agregado:
                filtro = self.datos[self.tipo_agregado] == self.agregado
                df_filtrado = self.datos.loc[filtro]
            else:
                df_filtrado = self.datos

            Q3 = df_filtrado[self.variable].quantile(0.75)
            Q1 = df_filtrado[self.variable].quantile(0.25)
            IQR = Q3 - Q1

            limite_superior = Q3 + (1.5 * IQR)
            limite_inferior = Q1 - (1.5 * IQR)

            filtro_1 = df_filtrado[self.variable] > limite_superior
            filtro_2 = df_filtrado[self.variable] < limite_inferior
            df_filtrado.loc[filtro_1, 'outlier'] = True
            df_filtrado.loc[filtro_2, 'outlier'] = True

            filtro_1 = df_filtrado['outlier'] == False
            filtro_2 = df_filtrado['outlier'] == True
            datadict = [
                {
                    'x': df_filtrado[filtro_1][self.variable],
                    'y': df_filtrado[filtro_1].index,
                    'type': 'scatter',
                    'mode': 'markers',
                    'name': 'Normal',
                    'hovertemplate':'Muestra: %{y:.0f}<br>Valor %{x}',
                    'marker': {"size": "3", "color": "#2196f3"},
                },
                {
                    'x': df_filtrado[filtro_2][self.variable],
                    'y': df_filtrado[filtro_2].index,
                    'type': 'scatter',
                    'mode': 'markers',
                    'name': 'Outlier',
                    'hovertemplate':'Muestra: %{y:.0f}<br>Valor %{x}',
                    'marker': {"size": "3", "color": "#ffeb3b"},
                },
            ]

            layout = dict(
                autosize=True,
                font={'color': '#ffffff'},
                margin=dict(l=35, r=0, t=20, b=30),
                height=120,
                plot_bgcolor='rgba(48, 48, 48, 1)',
                paper_bgcolor='rgba(48, 48, 48, 1)',
                bgcolor='rgba(0, 0, 0, 0.5)',
                legend=dict(
                    orientation="h",
                    xanchor="right",
                    yanchor="top",
                    y=0,
                    x=1,
                    bgcolor="rgba(0, 0, 0, 0)",
                    font=dict(
                        size=8,
                    ),
                ),
                xaxis=dict(
                    title='',
                    type='log',
                    gridcolor='gray',
                    zerolinecolor='white',
                ),
                yaxis=dict(
                    gridcolor='gray',
                    zerolinecolor='white',
                ),
                title={
                    'text': self.label,
                    'x': 0.5,
                    'y': 0.95,
                    'font': {'size': 12},
                },
            )

            fig = dict(data=datadict, layout=layout)
        except Exception as e:
            print("figure:", e)
        return fig

    # --------------------------------------------------------------------------

    def display(self):
        """Displays the card with label, kpi and a mini-plot from the data"""
        layout = dcc.Graph(
            className="mb-1",
            figure=univariate_plot.figura(self),
            id=f"{self.variable}-plot",
        )
        return layout
