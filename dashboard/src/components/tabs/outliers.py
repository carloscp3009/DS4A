import dash_bootstrap_components as dbc
from components.univariate_plot import univariate_plot
from components.multivariate_plot import multivariate_plot

variable_plot = univariate_plot("acidez", "Acidez")
multivariable_plot = multivariate_plot("cod_municipio", "None")

outliers_tab_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    variable_plot.display(),
                ],
                id="id-univariate-plot",
            ),
            dbc.Row(
                [],
                className="plot-separator",
            ),
            dbc.Row(
                [
                    multivariable_plot.display(),
                ],
                id="id-mutlivariate-plot",
                className="mt-2",
            ),
        ]
    ),
    className="mt-3",
)
