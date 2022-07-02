from dash import dcc
import numpy as np
import pandas as pd

from utils.load_data import Connection

# ------------------------------------------------------------------------------


class univariate_plot:
    def __init__(
                self, variable='acidez',
                titulo='Análisis univariado de outliers',
                tipo_agregado='cod_municipio', agregado=None):
        """Constructs all the attributes for kpiplot class"""
        self.tipo_agregado = tipo_agregado
        self.agregado = agregado
        self.variable = variable if variable else 'acidez'
        self.label = 'Análisis univariado de outliers'

    # --------------------------------------------------------------------------

    def get_layout(self, num_samples=0):
        """Returns the layout of the card"""
        layout = dict(
            autosize=True,
            font={'color': '#ffffff'},
            margin=dict(l=35, r=0, t=40, b=30),
            height=180,
            plot_bgcolor='rgba(48, 48, 48, 1)',
            paper_bgcolor='rgba(48, 48, 48, 1)',
            bgcolor='rgba(0, 0, 0, 0.5)',
            legend=dict(
                orientation="h",
                xanchor="right",
                yanchor="bottom",
                y=0.95,
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
                'text': f'{self.label} ({num_samples})',
                'x': 0.5,
                'y': 0.95,
                'font': {'size': 12},
            },
        )
        return layout

    # --------------------------------------------------------------------------

    @staticmethod
    def figura(self):
        try:
            query = '''
                SELECT id, %s as variable
                FROM analisis
                WHERE %s = '%s'
            ''' % (self.variable, self.tipo_agregado, self.agregado)
            conn, cur = Connection.get_connection()
            self.datos = pd.read_sql_query(query, conn)

            self.datos['outlier'] = False

            Q3 = self.datos['variable'].quantile(0.75)
            Q1 = self.datos['variable'].quantile(0.25)
            IQR = Q3 - Q1

            limite_superior = Q3 + (1.5 * IQR)
            limite_inferior = Q1 - (1.5 * IQR)

            filtro_1 = self.datos['variable'] > limite_superior
            filtro_2 = self.datos['variable'] < limite_inferior
            self.datos.loc[filtro_1, 'outlier'] = True
            self.datos.loc[filtro_2, 'outlier'] = True

            filtro_1 = self.datos['outlier'] == False
            filtro_2 = self.datos['outlier'] == True

            num_samples = self.datos.shape[0]
            num_no_outliers = self.datos[filtro_1].shape[0]
            num_outliers = self.datos[filtro_2].shape[0]

            datadict = [
                {
                    'x': self.datos[filtro_1]['variable'],
                    'y': self.datos[filtro_1].index,
                    'type': 'scatter',
                    'mode': 'markers',
                    'name': f'Normal ({num_no_outliers})',
                    'hovertemplate':'Muestra: %{y:.0f}<br>Valor %{x}',
                    'hoverinfo': 'skip',
                    'marker': {"size": "3", "color": "#2196f3"},
                },
                {
                    'x': self.datos[filtro_2]['variable'],
                    'y': self.datos[filtro_2].index,
                    'type': 'scatter',
                    'mode': 'markers',
                    'name': f'Outlier ({num_outliers})',
                    'hovertemplate':'Muestra: %{y:.0f}<br>Valor %{x}',
                    'hoverinfo': 'skip',
                    'marker': {"size": "3", "color": "#ffeb3b"},
                },
            ]

            layout = self.get_layout()
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
