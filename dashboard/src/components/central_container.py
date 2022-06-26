import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from dash import dcc, callback, Input, Output, State
from utils.map import map
from components.univariate_plot import univariate_plot
from utils.load_data import lstVariables

# ------------------------------------------------------------------------------

left_col = dbc.Col(
        [
            dbc.Container(
                # dcc.Graph(
                #     id='map',
                #     figure=map,
                #     className="mt-2 h-100 mb-2",
                # ),
                # className="mt-2 h-100 mb-2",
            ),
        ],
        id="left-col",
        className="col-12 col-md-9 px-2",
    )

# ------------------------------------------------------------------------------

acidez_plot = univariate_plot("acidez", "Acidez")
aluminio_plot = univariate_plot("aluminio", "Aluminio")
azufre_plot = univariate_plot("azufre", "Azufre")
boro_plot = univariate_plot("boro", "Boro")
calcio_plot = univariate_plot("calcio", "Calcio")
ce_plot = univariate_plot("ce", "Conductividad eléctrica")
cice_plot = univariate_plot("cice", "Coef. intercambio catiónico")
cobre_plot = univariate_plot("cobre", "Cobre")
cobre_doble_acido_plot = univariate_plot(
    "cobre_doble_acido", "Cobre doble ácido")
fosforo_plot = univariate_plot("fosforo", "Fósforo")
hierro_doble_acido_plot = univariate_plot(
    "hierro_doble_acido", "Hierro doble ácido")
hierro_olsen_plot = univariate_plot("hierro_olsen", "Hierro Olsen")
magnesio_plot = univariate_plot("magnesio", "Magnesio")
manganeso_plot = univariate_plot("manganeso", "Manganeso")
manganeso_doble_acido_plot = univariate_plot(
    "manganeso_doble_acido", "Manganeso doble ácido")
materia_organica_plot = univariate_plot(
    "materia_organica", "Materia orgánica")
ph_plot = univariate_plot("ph", "pH")
potasio_plot = univariate_plot("potasio", "Potasio")
sodio_plot = univariate_plot("sodio", "Sodio")
zinc_olsen_plot = univariate_plot("zinc_olsen", "Zinc Olsen")

lstPlots = [
    "acidez", "aluminio", "azufre", "boro", "calcio", "ce", "cice", "cobre",
    "cobre_doble_acido", "fosforo", "hierro_doble_acido", "hierro_olsen",
    "magnesio", "manganeso", "manganeso_doble_acido", "materia_organica", "ph",
    "potasio", "sodio", "zinc_olsen"]

right_col = dbc.Col(
        [
            dbc.Row([
                eval(f"{variable}_plot").display()],
                id=f"id_{variable}_plot")
                    for variable in lstPlots
        ],
        id="right-col",
        className="col-md-3 offset-md-9 ps-2 h-100 mt-2",
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

# ------------------------------------------------------------------------------

lstOutputs = [Output(f"id_{plot}_plot", "children") for plot in lstPlots]

@callback(
    lstOutputs,
    [State('select-deparment', 'value')],
    [Input('btnFiltrar', 'n_clicks')],
    prevent_initial_call=True
)
def update_plots(departamento, n_clicks):
    try:
        lst = []
        for item in lstVariables:
            variable = item["value"]
            # filtro_1 = df['departamento'] == departamento
            eval(f"{variable}_plot").agregado = departamento
            nuevo_grafico = eval(f"{variable}_plot").display()
            lst.append([nuevo_grafico])
    except Exception as e:
        print("update_plot:", e)
    return tuple(lst)
