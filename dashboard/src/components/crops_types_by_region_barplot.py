import pandas as pd
import plotly.express as px

from dash import dcc

from utils.load_data import Connection

# ------------------------------------------------------------------------------


class Crops_types_by_region_barplot:
    def __init__(self, tipo_agregado=None, agregado=None):
        self.agregado = agregado
        self.tipo_agregado = tipo_agregado
        self.title = 'Principales cultivos a nivel nacional'

    # --------------------------------------------------------------------------

    def figura(self):
        try:
            if self.tipo_agregado == 'zona':
                query = f"""
                    SELECT region
                    FROM zonas
                    WHERE cod_region = '{self.agregado}'
                """
                _zona = Connection.get_data(query)[0][0]
                self.title = 'Cantidad de cultivos en zona ' + _zona
                extra = f'WHERE d.`{self.agregado}` = 1'

            elif self.tipo_agregado == 'cod_departamento':
                query = f"""
                    SELECT departamento
                    FROM departamentos
                    WHERE cod_departamento = '{self.agregado}'
                """
                _departamento = Connection.get_data(query)[0][0]
                self.title = f"Principales cultivos en {_departamento}"
                extra = f"WHERE d.cod_departamento = '{self.agregado}'"

            elif self.tipo_agregado == 'cod_municipio':
                query = f"""
                    SELECT municipio
                    FROM municipios
                    WHERE cod_municipio = '{self.agregado}'
                """
                _municipio = Connection.get_data(query)[0][0]
                self.title = f"Principales cultivos en {_municipio}"
                extra = f"WHERE m.cod_municipio = '{self.agregado}'"

            else:
                self.tipo_agregado = 'departamento'
                extra = ''
            query = f"""
                SELECT
                    a.cultivo as Cultivos, count(*) as Cantidad
                FROM
                    analisis a INNER JOIN
                    municipios m ON a.cod_municipio = m.cod_municipio
                                                                    INNER JOIN
                    departamentos d ON m.cod_departamento = d.cod_departamento
                {extra}
                GROUP BY Cultivos
                ORDER BY Cantidad DESC
                LIMIT 10
                """
            conn, cur = Connection.get_connection()
            self.datos = pd.read_sql_query(query, conn)
            self.datos['Cultivos'] = self.datos['Cultivos'].str.title()

            fig = px.bar(
                self.datos, x='Cantidad', y='Cultivos',
                hover_data=['Cultivos', 'Cantidad'],
                color='Cantidad',
                text_auto=True,
                orientation='h',
                title=self.title,
                color_continuous_scale="Portland",
            )

            fig.update_layout(
                autosize=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(
                    color='white',
                    size=10,
                ),
                margin=dict(
                    l=10,
                    r=10,
                    t=30,
                    b=10,
                ),
                yaxis=dict(autorange='reversed'),
            )
            # fig = Figure()
            # layout = self.get_layout(num_samples)
            # fig = dict(data=datadict, layout=layout)
        except Exception as e:
            print("crops_types_by_region_barplot.figure:", e)
        return fig

    # --------------------------------------------------------------------------

    def display(self):
        """Displays the card with label, kpi and a mini-plot from the data"""
        layout = dcc.Graph(
            className="mb-1",
            figure=Crops_types_by_region_barplot.figura(self),

        )
        return layout