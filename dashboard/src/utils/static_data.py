import sqlite3
# from sqlalchemy import create_engine

# con = sqlite3.connect(":memory:")
# engine = create_engine('sqlite://', echo=False)
# con = sqlite3.connect(":memory:")

variables = ['pH agua:suelo 2,5:1,0 ',
'Materia orgánica (MO) %',
'Fósforo (P) Bray II mg/kg',
'Azufre (S) Fosfato monocalcico mg/kg',
'Acidez (Al+H) KCL cmol(+)/kg',
'Aluminio (Al) intercambiable cmol(+)/kg',
'Calcio (Ca) intercambiable cmol(+)/kg',
'Magnesio (Mg) intercambiable cmol(+)/kg',
'Potasio (K) intercambiable cmol(+)/kg',
'Sodio (Na) intercambiable cmol(+)/kg',
'capacidad de intercambio cationico (CICE) suma de bases cmol(+)/kg',
'Conductividad electrica (CE) relacion 2,5:1,0 dS/m',
'Hierro (Fe) disponible olsen mg/kg',
'Cobre (Cu) disponible mg/kg',
'Manganeso (Mn) disponible Olsen mg/kg',
'Zinc (Zn) disponible Olsen mg/kg',
'Boro (B) disponible mg/kg',
'Hierro (Fe) disponible doble acido mg/kg',
'Cobre (Cu) disponible doble acido mg/kg',
'Manganeso (Mn) disponible doble acido mg/kg']

# lstVariables = [
#     {"label": "Acidez", "value": "acidez"},
#     {"label": "Aluminio", "value": "aluminio"},
#     {"label": "Azufre", "value": "azufre"},
#     {"label": "Boro", "value": "boro"},
#     {"label": "Calcio", "value": "calcio"},
#     {"label": "Coductividad eléctrica", "value": "ce"},
#     {"label": "Coef. Intercambio Catiónico", "value": "cice"},
#     {"label": "Cobre", "value": "cobre"},
#     {"label": "Cobre doble ácido", "value": "cobre_doble_acido"},
#     {"label": "Fósforo", "value": "fosforo"},
#     {"label": "Hierro doble ácido", "value": "hierro_doble_acido"},
#     {"label": "Hierro Olsen", "value": "hierro_olsen"},
#     {"label": "Magnesio", "value": "magnesio"},
#     {"label": "Manganeso", "value": "manganeso"},
#     {"label": "Manganeso doble ácido", "value": "manganeso_doble_acido"},
#     {"label": "Materia orgánica", "value": "materia_organica"},
#     {"label": "Ph", "value": "ph"},
#     {"label": "Potasio", "value": "potasio"},
#     {"label": "Sodio", "value": "sodio"},
#     {"label": "Zinc Olsen", "value": "zinc_olsen"}
# ]

# lstDepartamentos = [
#     {"label": "Amazonas", "value": "amazonas"},
#     {"label": "Antioquia", "value": "antioquia"},
#     {"label": "Arauca", "value": "arauca"},
#     {"label": "Atlántico", "value": "atlantico"},
#     {"label": "Bolívar", "value": "bolivar"},
#     {"label": "Boyacá", "value": "boyaca"},
#     {"label": "Caldas", "value": "caldas"},
#     {"label": "Caquetá", "value": "caqueta"},
#     {"label": "Casanare", "value": "casanare"},
#     {"label": "Cauca", "value": "cauca"},
#     {"label": "Cesar", "value": "cesar"},
#     {"label": "Chocó", "value": "choco"},
#     {"label": "Córdoba", "value": "cordoba"},
#     {"label": "Cundinamarca", "value": "cundinamarca"},
#     {"label": "Guainía", "value": "guainia"},
#     {"label": "Guaviare", "value": "guaviare"},
#     {"label": "Huila", "value": "huila"},
#     {"label": "La Guajira", "value": "guajira"},
#     {"label": "Magdalena", "value": "magdalena"},
#     {"label": "Meta", "value": "meta"},
#     {"label": "Nariño", "value": "narino"},
#     {"label": "Norte de Santander", "value": "norte_santander"},
#     {"label": "Putumayo", "value": "putumayo"},
#     {"label": "Quindío", "value": "quindio"},
#     {"label": "Risaralda", "value": "risaralda"},
#     {"label": "Santander", "value": "santander"},
#     {"label": "Sucre", "value": "sucre"},
#     {"label": "Tolima", "value": "tolima"},
#     {"label": "Valle del Cauca", "value": "valle_cauca"},
#     {"label": "Vaupés", "value": "vaupes"},
#     {"label": "Vichada", "value": "vichada"}
# ]