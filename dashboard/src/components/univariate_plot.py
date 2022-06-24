from dash import html, dcc
import pandas as pd
import dash_bootstrap_components as dbc

# ------------------------------------------------------------------------------

class univariate_plot:
    def __init__(self, df, departamento, variable):
        """Constructs all the attributes for kpiplot class"""
        self.label = variable.capitalize()
        self.departamento = departamento
        self.variable = variable

        filtro = df['departamento'] == departamento
        self.datos = df[filtro].copy().dropna(subset=[variable])
        self.datos['outlier'] = False

    @staticmethod
    def figura(self):
        Q3 = self.datos[self.variable].quantile(0.75)
        Q1 = self.datos[self.variable].quantile(0.25)
        IQR = Q3 - Q1

        limite_superior = Q3 + (1.5 * IQR)
        limite_inferior = Q1 - (1.5 * IQR)

        filtro_1 = self.datos[self.variable] > limite_superior
        filtro_2 = self.datos[self.variable] < limite_inferior
        self.datos['outlier'] = filtro_1 | filtro_2

        filtro_1 = self.datos['outlier'] == False
        filtro_2 = self.datos['outlier'] == True
        datadict = [
            {
                'x': self.datos[filtro_1][self.variable],
                'y': self.datos[filtro_1].index,
                'type': 'scatter',
                'mode': 'markers',
                'name': 'Normal',
                'hovertemplate':'%{x}',
            },
            {
                'x': self.datos[filtro_2][self.variable],
                'y': self.datos.index,
                'type': 'scatter',
                'mode': 'markers',
                'name': 'Outlier',
                'hovertemplate':'%{x}',
            },
        ]

        layout = dict(
            autosize=True,
            margin=dict(l=35, r=0, t=35, b=30),
            height=180,
            plot_bgcolor='rgba(0, 0, 0, 0)',
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

        return fig


    def display(self):
        """Displays the card with label, kpi and a mini-plot from the data"""
        layout = html.Div([
            dcc.Graph(figure=univariate_plot.figura(self)),
        ])
        return layout
