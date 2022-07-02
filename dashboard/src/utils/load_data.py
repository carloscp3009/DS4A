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


lstVariables = []
query = 'SELECT codigo, variable FROM variables'
data = Connection.get_data(query)
lstVariables = [{"label": row[1], "value": row[0]} for row in data]

# ------------------------------------------------------------------------------

lstDepartamentos = []
query = '''
    SELECT cod_departamento, departamento
    FROM departamentos
    ORDER BY departamento'''
data = Connection.get_data(query)
lstDepartamentos = [{"label": row[1], "value": row[0]} for row in data]

# ------------------------------------------------------------------------------

lstZonas = {}
query = 'SELECT cod_region, region FROM zonas'
data = Connection.get_data(query)
lstZonas = [{"label": row[1], "value": row[0]} for row in data]

# ------------------------------------------------------------------------------

# df = pd.read_csv('data/suelos_preprocesado.csv', nrows=100)

# ------------------------------------------------------------------------------

lstPlots = [
    "acidez",
    # "aluminio", "azufre", "boro", "calcio", "ce", "cice", "cobre",
    # "cobre_doble_acido", "fosforo", "hierro_doble_acido", "hierro_olsen",
    # "magnesio", "manganeso", "manganeso_doble_acido", "materia_organica", "ph",
    # "potasio", "sodio", "zinc_olsen"
]