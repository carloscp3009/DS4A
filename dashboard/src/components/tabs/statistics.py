import dash_bootstrap_components as dbc
from dash import html
from components.crops_by_region_barplot import Crops_by_region_barplot
from components.crops_types_by_region_barplot import (
    Crops_types_by_region_barplot)

crops_by_region = Crops_by_region_barplot()
crops_types_by_region = Crops_types_by_region_barplot()

statistics_tab_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                dbc.Col(
                    [
                        crops_by_region.display(),
                    ],
                    id="id-crops-by-region-barplot",
                    className="mt-2",
                ),
            ),
            dbc.Row(
                [],
                className="plot-separator",
            ),
            dbc.Row(
                dbc.Col(
                    [
                        crops_types_by_region.display(),
                    ],
                    id="id-crops-types-by-region-barplot",
                    className="mt-2",
                ),
            ),
        ],
        className="p-0",
    ),
    className="mt-3",
)
