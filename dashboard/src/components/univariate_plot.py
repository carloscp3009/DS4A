import pandas as pd

from dash import dcc

from utils.load_data import Connection

# ------------------------------------------------------------------------------


class univariate_plot:
    def __init__(
                self,
                variable='acidez',
                tipo_agregado='cod_municipio',
                agregado=None):
        """Initializes the class

        Inputs:
            variable: str
                Variable to plot
            tipo_agregado: str
                Type of aggregation to use
            agregado: str
                Value of the aggregation

        Outputs:
            None

        Version: 1.0 - Initial version """
        self.tipo_agregado = tipo_agregado
        self.agregado = agregado
        self.variable = variable
        self.label = 'Acidez'

    # --------------------------------------------------------------------------

    def get_layout(self, num_samples=0):
        """Returns the layout of the plot.

        Inputs:
            num_samples: int
                Number of samples in the data

        Outputs:
            layout: dict
                Layout of the plot

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

    def figura(self):
        """Returns the figure of the component.

        Inputs:
            None

        Outputs:
            fig: dict
                Figure of the component

        Version: 1.0 - Initial version """
        try:
            query = f"""
                SELECT
                    id, {self.variable} as variable
                FROM
                    analisis a INNER JOIN
                    municipios m ON a.cod_municipio = m.cod_municipio INNER JOIN
                    departamentos d ON m.cod_departamento = d.cod_departamento
                """
            if self.tipo_agregado == 'zona':
                query += f"WHERE `{self.agregado}` = 1"
            else:
                query += f"WHERE m.{self.tipo_agregado} = '{self.agregado}'"
            conn, cur = Connection.get_connection()
            self.datos = pd.read_sql_query(query, conn)

            if self.datos.empty:
                layout = self.get_layout()
                fig = dict(data=[], layout=layout)
                return fig

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
                    'marker': {"size": "5", "color": "#2196f3"},
                },
                {
                    'x': self.datos[filtro_2]['variable'],
                    'y': self.datos[filtro_2].index,
                    'type': 'scatter',
                    'mode': 'markers',
                    'name': f'Outlier ({num_outliers})',
                    'hovertemplate':'Muestra: %{y:.0f}<br>Valor %{x}',
                    'hoverinfo': 'skip',
                    'marker': {"size": "5", "color": "#ffeb3b"},
                },
            ]

            layout = self.get_layout(num_samples)
            fig = dict(data=datadict, layout=layout)
        except Exception as e:
            print("univariate_plot.figure:", e)
        return fig

    # --------------------------------------------------------------------------

    def display(self):
        """Returns the display of the component.

        Inputs:
            None

        Outputs:
            layout: dict
                Layout of the component

        Version: 1.0 - Initial version """
        layout = dcc.Graph(
            className="mb-1",
            figure=univariate_plot.figura(self),
        )
        return layout
