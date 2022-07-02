# from operator import index
# from re import A
# from turtle import bgcolor
from cgi import print_directory
import re
from dash import dcc
from matplotlib.ft2font import LOAD_VERTICAL_LAYOUT
import pandas as pd
# import dash_bootstrap_components as dbc
# import matplotlib.pyplot as plt
# import datetime
from sklearn.decomposition import KernelPCA
from sklearn.ensemble import IsolationForest
from sklearn import preprocessing

from utils.load_data import Connection

# ------------------------------------------------------------------------------


class multivariate_plot:
    def __init__(
            self, tipo_agregado='cod_municipio', agregado=None):
        self.tipo_agregado = tipo_agregado
        self.agregado = agregado
        self.label = "Análisis multivariado de outliers"
        self.datos = None

    # --------------------------------------------------------------------------

    def outliers_iforest(self):
        try:
            df_region = self.datos.copy()
            # Normalización de los datos
            df_region = df_region[
                [
                    'ph', 'materia_organica', 'fosforo', 'calcio', 'magnesio', 'potasio', 'sodio', 'cice', 'ce', 'boro'
                ]
            ]

            #Data is normalized with MinMax()
            min_max_scaler = preprocessing.MinMaxScaler()
            df_region = min_max_scaler.fit_transform(df_region)
            df_region = pd.DataFrame(df_region)
            df_region = df_region.rename(
                columns = {
                    0: 'ph',
                    1: 'materia_organica', 2: 'fosforo',
                    3: 'azufre', 4: 'acidez', 5: 'aluminio',
                    6: 'calcio',
                    7: 'magnesio', 8: 'potasio', 9: 'sodio', 10: 'cice',
                    11: 'ce', 12: 'hierro_olsen', 13: 'cobre', 14: 'manganeso',
                    15: 'zinc_olsen', 16: 'boro'
                }
            )
            print(df_region.head())


            kpca = KernelPCA(n_components=2, kernel='poly')
            model = kpca.fit(df_region)
            dt_train = kpca.transform(df_region)

            # ISOLATION FOREST MODEL
            iso_forest = IsolationForest(n_estimators=50, contamination=0.07)
            modelo_iforest = iso_forest.fit(dt_train)
            isof_outliers = iso_forest.predict(dt_train)
            isof_outliers_df = pd.DataFrame(
                isof_outliers, columns=['Prediction'])

            # isoF_outliers_values = dt_train[isof_outliers == -1]
            # outlier_size = isoF_outliers_values.shape

            data = pd.concat(
                [
                    (pd.DataFrame(dt_train)),
                    isof_outliers_df
                ],
                axis=1)
            data = data.rename(
                columns={0: 'Artificial variable X', 1: 'Artificial variable Y'})
            data['Prediction'].replace(
                {-1: 'Outlier', 1: 'No outlier'}, inplace=True)
        except Exception as e:
            print('outliers_iforest:', e)
            data = None
        return data

    # --------------------------------------------------------------------------

    def get_layout(self, num_samples=0):
        layout = dict(
            autosize=True,
            font={'color': '#ffffff'},
            margin=dict(l=35, r=0, t=40, b=30),
            height=200,
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
                gridcolor='gray',
                zerolinecolor='white',
            ),
            yaxis=dict(
                # type='log',
                gridcolor='gray',
                zerolinecolor='white',
            ),
            title={
                'text': f"{self.label} ({num_samples})",
                'x': 0.5,
                'y': 0.95,
                'font': {'size': 12},
            },
        )
        return layout

    # --------------------------------------------------------------------------

    # @staticmethod
    def figura(self):
        try:
            query = f"""
                SELECT
                    id, ph, materia_organica, fosforo, calcio, magnesio,
                    potasio, sodio, cice, ce, boro
                FROM analisis
                WHERE {self.tipo_agregado} = '{self.agregado}' """
            conn, cur = Connection.get_connection()
            self.datos = pd.read_sql_query(query, conn)

            null_values = self.datos[self.datos.isnull().any(1)]
            self.datos = \
                self.datos.drop(null_values.index).reset_index(drop=True)

            layout = self.get_layout()
            if self.datos.empty:
                fig = dict(data=[], layout=layout)
                return fig

            df_outliers = self.outliers_iforest()

            outliers_mask = df_outliers['Prediction'] == 'Outlier'
            no_outliers_mask = df_outliers['Prediction'] == 'No outlier'

            num_samples = self.datos.shape[0]
            num_outliers = df_outliers[outliers_mask].shape[0]
            num_no_outliers = df_outliers[no_outliers_mask].shape[0]

            datadict = [
                {
                    'x': df_outliers[no_outliers_mask]['Artificial variable X'],
                    'y': df_outliers[no_outliers_mask]['Artificial variable Y'],
                    'type': 'scatter',
                    'mode': 'markers',
                    'name': f'Normal ({num_no_outliers})',
                    'hovertemplate':'Muestra: %{y:.0f}<br>Valor %{x}',
                    'marker': {"size": "3", "color": "#2196f3"},
                },
                {
                    'x': df_outliers[outliers_mask]['Artificial variable X'],
                    'y': df_outliers[outliers_mask]['Artificial variable Y'],
                    'type': 'scatter',
                    'mode': 'markers',
                    'name': f'Outliers ({num_outliers})',
                    'hovertemplate':'Muestra: %{y:.0f}<br>Valor %{x}',
                    'marker': {"size": "3", "color": "#ffeb3b"},
                },
            ]

            fig = dict(data=datadict, layout=layout)
        except Exception as e:
            print("figure:", e)
        return fig

    # --------------------------------------------------------------------------

    def display(self):
        layout = dcc.Graph(
            className="mb-1",
            figure=multivariate_plot.figura(self),
            # id="id-multivariate-plot",
        )
        return layout
