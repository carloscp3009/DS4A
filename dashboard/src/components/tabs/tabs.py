import dash_bootstrap_components as dbc

from components.tabs.outliers import outliers_tab_content
from components.tabs.prediction import prediction_tab_content
from components.tabs.statistics import statistics_tab_content


tabs = dbc.Tabs(
    [
        dbc.Tab(outliers_tab_content, label="Outliers"),
        dbc.Tab(prediction_tab_content, label="Predictions"),
        dbc.Tab(statistics_tab_content, label="Statistics"),
    ]
)
