import pandas as pd
import plotly.express as px

from dash import dcc

from utils.load_data import Connection

# ------------------------------------------------------------------------------


class Crops_by_region_barplot:
    def __init__(self, tipo_agregado=None, agregado=None):
        """ Initializes the class

        Inputs:
            tipo_agregado: string
                'zona' or 'cod_departamento' or 'cod_municipio'
            agregado: string
                'zona' or 'cod_departamento' or 'cod_municipio'

        Outputs:
            None

        Version: 1.0 - Initial version
        """
        self.agregado = agregado
        self.tipo_agregado = tipo_agregado
        self.title = ' '

    # --------------------------------------------------------------------------

    def figura(self):
        """Create a crops bar plot of the given region.

        Inputs:
            None

        Outputs:
            figura: dict
                Layout of the crops bar plot.

        Version: 1.0 - Initial version """
        try:
            if self.tipo_agregado == 'zona':
                query = f"""
                    SELECT region
                    FROM zonas
                    WHERE cod_region = '{self.agregado}'
                """
                _zona = Connection.get_data(query)[0][0]
                self.title = 'Crops in ' + _zona + ' zone'
                field = 'd.departamento'
                fieldname = 'Deparments'
                extra = f'WHERE d.`{self.agregado}` = 1'

            elif self.tipo_agregado == 'cod_departamento':
                query = f"""
                    SELECT departamento
                    FROM departamentos
                    WHERE cod_departamento = '{self.agregado}'
                """
                _departamento = Connection.get_data(query)[0][0]
                self.title = f"Crops in {_departamento} per municipality"
                field = 'm.municipio'
                fieldname = 'Municipalities'
                extra = f"WHERE d.cod_departamento = '{self.agregado}'"

            elif self.tipo_agregado == 'cod_municipio':
                query = f"""
                    SELECT d.cod_departamento, d.departamento
                    FROM
                        municipios m INNER JOIN
                        departamentos d
                                    ON m.cod_departamento = d.cod_departamento
                    WHERE m.cod_municipio = '{self.agregado}'
                """
                _cod_departamento = Connection.get_data(query)[0][0]
                _departamento = Connection.get_data(query)[0][1]
                self.title = f"Crops in {_departamento} per municipality"
                field = 'm.municipio'
                fieldname = 'Municipalities'
                extra = f"WHERE d.cod_departamento = '{_cod_departamento}'"

            else:
                self.title = 'Crops by deparment'
                field = 'd.departamento'
                fieldname = 'Deparments'
                extra = ''
            query = f"""
                SELECT
                    {field} as {fieldname}, count(*) as Quantity
                FROM
                    analisis a INNER JOIN
                    municipios m ON a.cod_municipio = m.cod_municipio
                                                                    INNER JOIN
                    departamentos d ON m.cod_departamento = d.cod_departamento
                {extra}
                GROUP BY {fieldname}
                ORDER BY Quantity DESC
                LIMIT 10
                """
            conn, cur = Connection.get_connection()
            self.datos = pd.read_sql_query(query, conn)

            fig = px.bar(
                self.datos, x='Quantity', y=fieldname,
                hover_data=[fieldname, 'Quantity'],
                color='Quantity',
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
        except Exception as e:
            print("crops_by_region_barplot.figure:", e)
        return fig

    # --------------------------------------------------------------------------

    def display(self):
        """Return the crops bar plot.

        Inputs:
            None

        Outputs:
            layout: dict
                Layout of the crops bar plot.

        Version: 1.0 - Initial version """
        layout = dcc.Graph(
            className="mb-1",
            figure=Crops_by_region_barplot.figura(self),

        )
        return layout
