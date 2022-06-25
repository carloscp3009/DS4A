import pandas as pd
import sqlite3

# ------------------------------------------------------------------------------

conn = sqlite3.connect('data/database.db')
cur = conn.cursor()

# ------------------------------------------------------------------------------

# crear un diccionario a partir del resultado de una consulta a la base de datos
lstVariables = []
query = 'SELECT codigo, variable FROM variables'
for row in cur.execute(query):
    lstVariables.append({"label": row[1], "value": row[0]})

# ------------------------------------------------------------------------------

lstDepartamentos = {}
query = 'SELECT clean, departamento FROM departamentos'
for row in cur.execute(query):
    lstDepartamentos[row[0]] = {"departamento": row[1]}

# ------------------------------------------------------------------------------

lstZonas = {}
query = 'SELECT codigo, zona, departamentos FROM zonas'
for row in cur.execute(query):
    lstZonas[row[0]] = {"zona": row[1], "departamentos": eval(row[2])}

# ------------------------------------------------------------------------------

df = pd.read_csv('data/suelos_preprocesado.csv')
