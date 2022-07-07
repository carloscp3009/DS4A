import pandas as pd

from dash import dcc
from sklearn.decomposition import KernelPCA
from sklearn.ensemble import IsolationForest
from sklearn import preprocessing

from utils.load_data import Connection

# ------------------------------------------------------------------------------


class multivariate_plot:
    def __init__(
            self, tipo_agregado='cod_municipio', agregado=None):
        """Constructor of the class

        Inputs:
            tipo_agregado: str, type of aggregation
            agregado: str, aggregation

        Outputs:
            None

        Version: 1.0 - Initial version """
        self.tipo_agregado = tipo_agregado
        self.agregado = agregado
        self.label = "Análisis multivariado de outliers"
        self.datos = None

    # --------------------------------------------------------------------------

    def outliers_iforest(self):
        """Returns the outliers using Isolation Forest

        Inputs:
            None

            Outputs:
                outliers: list
                    List of outliers

        Version: 1.0 - Initial version """
        try:
            df_region = self.datos

            # Normalización de los datos
            df_region = df_region[[
                'ph', 'materia_organica', 'fosforo', 'calcio', 'magnesio',
                'potasio', 'sodio', 'cice', 'ce', 'boro'
            ]]

            # Data is normalized with MinMax()
            min_max_scaler = preprocessing.MinMaxScaler()
            df_region = min_max_scaler.fit_transform(df_region)
            df_region = pd.DataFrame(df_region)
            df_region = df_region.rename(
                columns={
                    0: 'ph',
                    1: 'materia_organica',
                    2: 'fosforo',
                    3: 'azufre',
                    4: 'acidez',
                    5: 'aluminio',
                    6: 'calcio',
                    7: 'magnesio',
                    8: 'potasio',
                    9: 'sodio',
                    10: 'cice',
                    11: 'ce',
                    12: 'hierro_olsen',
                    13: 'cobre',
                    14: 'manganeso',
                    15: 'zinc_olsen',
                    16: 'boro'
                }
            )

            kpca = KernelPCA(n_components=2, kernel='poly')
            kpca.fit(df_region)
            dt_train = kpca.transform(df_region)

            # ISOLATION FOREST MODEL
            iso_forest = IsolationForest(n_estimators=50, contamination=0.07)
            iso_forest.fit(dt_train)
            isof_outliers = iso_forest.predict(dt_train)
            isof_outliers_df = pd.DataFrame(
                isof_outliers, columns=['Prediction'])

            data = pd.concat(
                [
                    (pd.DataFrame(dt_train)),
                    isof_outliers_df
                ], axis=1)

            data = data.rename(
                columns={
                    0: 'Artificial variable X',
                    1: 'Artificial variable Y'})

            data['Prediction'].replace(
                {-1: 'Outlier', 1: 'No outlier'},
                inplace=True)
        except Exception as e:
            print('outliers_iforest:', e)
            data = None
        return data

    # --------------------------------------------------------------------------

    def get_layout(self, num_samples=0):
        """Returns the layout of the component

        Inputs:
            num_samples: int, number of samples

        Outputs:
            layout: dict, layout of the component

            Version: 1.0 - Initial version """
        layout = dict(
            autosize=True,
            font={'color': '#ffffff'},
            margin=dict(l=35, r=0, t=40, b=30),
            plot_bgcolor='rgba(48, 48, 48, 0)',
            paper_bgcolor='rgba(48, 48, 48, 0)',
            bgcolor='rgba(0, 0, 0, 0.5)',
            legend=dict(
                orientation="h",
                xanchor="right",
                yanchor="bottom",
                y=0.95,
                x=1,
                bgcolor="rgba(0, 0, 0, 0)",
                font=dict(
                    size=10,
                ),
            ),
            xaxis=dict(
                title='',
                gridcolor='gray',
                zerolinecolor='white',
            ),
            yaxis=dict(
                gridcolor='gray',
                zerolinecolor='white',
            ),
            title={
                'text': f"Total samples {num_samples} (Max. 5000)",
                'x': 0.5,
                'y': 0.95,
                'font': {'size': 12},
            },
        )
        return layout

    # --------------------------------------------------------------------------

    def figura(self):
        """Returns the figure of the component

        Inputs:
            None

        Outputs:
            figura: dict, figure of the component

        Version: 1.0 - Initial version """
        try:
            query = """
                SELECT
                    id, ph, materia_organica, fosforo, calcio, magnesio,
                    potasio, sodio, cice, ce, boro
                 FROM
                    analisis a INNER JOIN
                    municipios m ON a.cod_municipio = m.cod_municipio
                                                                    INNER JOIN
                    departamentos d ON m.cod_departamento = d.cod_departamento
                """
            if self.tipo_agregado == 'zona':
                query += f"WHERE `{self.agregado}` = 1"
            else:
                query += f"WHERE m.{self.tipo_agregado} = '{self.agregado}'"

            conn, cur = Connection.get_connection()
            self.datos = pd.read_sql_query(query, conn)

            if self.datos.shape[0] > 5000:
                self.datos = self.datos.sample(5000)

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

            if 'Artificial variable Y' not in df_outliers.columns:
                df_outliers['Artificial variable Y'] = 0

            datadict = [
                {
                    'x':
                        df_outliers[no_outliers_mask]['Artificial variable X'],
                    'y':
                        df_outliers[no_outliers_mask]['Artificial variable Y'],
                    'type': 'scatter',
                    'mode': 'markers',
                    'name': f'Normal ({num_no_outliers})',
                    'hovertemplate':'Muestra: %{y:.0f}<br>Valor %{x}',
                    'marker': {"size": "5", "color": "#2196f3"},
                },
                {
                    'x': df_outliers[outliers_mask]['Artificial variable X'],
                    'y': df_outliers[outliers_mask]['Artificial variable Y'],
                    'type': 'scatter',
                    'mode': 'markers',
                    'name': f'Outliers ({num_outliers})',
                    'hovertemplate':'Muestra: %{y:.0f}<br>Valor %{x}',
                    'marker': {"size": "5", "color": "#ffeb3b"},
                },
            ]

            layout = self.get_layout(num_samples)
            fig = dict(data=datadict, layout=layout)
        except Exception as e:
            print("figure:", e)
        return fig

    # --------------------------------------------------------------------------

    def display(self):
        """Returns the display of the component

        Inputs:
            None

        Outputs:
            layout: dict, layout of the component

        Version: 1.0 - Initial version """
        layout = dcc.Graph(
            className="mb-1",
            figure=multivariate_plot.figura(self),
        )
        return layout
