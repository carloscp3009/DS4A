import dash_bootstrap_components as dbc

from components.choropleth_plot import choropleth_plot
from components.tabs import tabs
from dash import html

# ------------------------------------------------------------------------------

my_choropleth_map = choropleth_plot()
left_col = dbc.Col(
        [
            html.Div(
                "Acidez",
                id="choropleth-title",
            ),
            dbc.Container(
                my_choropleth_map.display(),
                id="id-choropleth-map",
            ),
        ],
        id="left-col",
        className="col-12 col-md-8 px-2 mt-2",
    )

# ------------------------------------------------------------------------------

right_col = dbc.Col(
        [
            tabs.tabs,
        ],
        id="right-col",
        className="col-md-4 offset-md-8 ps-2 h-100 mt-2",
)

# ------------------------------------------------------------------------------

central_container = dbc.Container(
        [
            left_col,
            right_col,
        ],
        id="central-container",
        className="g-0 ms-auto flex-nowrap row pb-2",
    )
