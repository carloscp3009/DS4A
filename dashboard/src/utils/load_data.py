import pandas as pd
import sqlite3

# ------------------------------------------------------------------------------


class Connection():
    @staticmethod
    def get_connection():
        conn = sqlite3.connect('data/database.db')
        cur = conn.cursor()
        return conn, cur

    @staticmethod
    def get_data(query):
        conn, cur = Connection.get_connection()
        cur.execute(query)
        data = cur.fetchall()
        conn.close()
        return data

# ------------------------------------------------------------------------------


# crear un diccionario a partir del resultado de una consulta a la base de datos
lstVariables = []
query = 'SELECT codigo, variable FROM variables'
data = Connection.get_data(query)
for row in data:
    lstVariables.append({"label": row[1], "value": row[0]})

# ------------------------------------------------------------------------------

# lstMunicipios = {}
# query = 'SELECT codigo, municipio, clean, departamento FROM municipios'
# data = Connection.get_data(query)
# for row in data:
#     lstMunicipios[row[1]] = {
#         "value": row[0],
#         "clean": row[2],
#         "departamento": row[3]
#     }

# ------------------------------------------------------------------------------

lstDepartamentos = {}
query = 'SELECT clean, departamento, codigo FROM departamentos'
data = Connection.get_data(query)
for row in data:
    lstDepartamentos[row[0]] = {"departamento": row[1], "codigo": row[2]}

# ------------------------------------------------------------------------------

lstZonas = {}
query = 'SELECT codigo, zona, departamentos FROM zonas'
data = Connection.get_data(query)
for row in data:
    lstZonas[row[0]] = {"zona": row[1], "departamentos": eval(row[2])}

# ------------------------------------------------------------------------------

df = pd.read_csv('data/suelos_preprocesado.csv')

# ------------------------------------------------------------------------------

lstPlots = [
    "acidez", "aluminio", "azufre", "boro", "calcio", "ce", "cice", "cobre",
    "cobre_doble_acido", "fosforo", "hierro_doble_acido", "hierro_olsen",
    "magnesio", "manganeso", "manganeso_doble_acido", "materia_organica", "ph",
    "potasio", "sodio", "zinc_olsen"]