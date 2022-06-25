from turtle import bgcolor
from dash import html, dcc
import pandas as pd
import dash_bootstrap_components as dbc

from utils.load_data import df

# ------------------------------------------------------------------------------


class univariate_plot:
    def __init__(self, variable, tipo_agregado='departamento', agregado='cauca'):
        """Constructs all the attributes for kpiplot class"""
        self.label = variable.replace("_", " ").capitalize()
        self.tipo_agregado = tipo_agregado
        self.agregado = agregado
        self.variable = variable

        self.datos = df[['departamento', 'municipio', variable]].copy()
        self.datos.dropna(subset=[variable], inplace=True)

    @staticmethod
    def figura(self):
        try:
            self.datos['outlier'] = False
            filtro = self.datos[self.tipo_agregado] == self.agregado
            df_filtrado = self.datos.loc[filtro]

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
                    'hovertemplate':'%{x}',
                },
                {
                    'x': df_filtrado[filtro_2][self.variable],
                    'y': df_filtrado[filtro_2].index,
                    'type': 'scatter',
                    'mode': 'markers',
                    'name': 'Outlier',
                    'hovertemplate':'%{x}',
                },
            ]

            layout = dict(
                autosize=True,
                margin=dict(l=35, r=0, t=35, b=30),
                height=120,
                plot_bgcolor='rgba(0, 0, 0, 0)',
                bgcolor='rgba(0, 0, 0, 0.5)',
                legend=dict(
                    orientation="h",
                    y=0,
                    x=0.5,
                    bgcolor="rgba(255, 255, 255, 0.5)",
                ),
                xaxis=dict(
                    title='',
                    type='log',
                ),
                title=self.variable.capitalize(),
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
