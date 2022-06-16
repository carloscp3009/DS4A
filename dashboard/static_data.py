import json
# variable = ['pH agua:suelo 2,5:1,0 ',
# 'Materia orgánica (MO) %',
# 'Fósforo (P) Bray II mg/kg',
# 'Azufre (S) Fosfato monocalcico mg/kg',
# 'Acidez (Al+H) KCL cmol(+)/kg',
# 'Aluminio (Al) intercambiable cmol(+)/kg',
# 'Calcio (Ca) intercambiable cmol(+)/kg',
# 'Magnesio (Mg) intercambiable cmol(+)/kg',
# 'Potasio (K) intercambiable cmol(+)/kg',
# 'Sodio (Na) intercambiable cmol(+)/kg',
# 'capacidad de intercambio cationico (CICE) suma de bases cmol(+)/kg',
# 'Conductividad electrica (CE) relacion 2,5:1,0 dS/m',
# 'Hierro (Fe) disponible olsen mg/kg',
# 'Cobre (Cu) disponible mg/kg',
# 'Manganeso (Mn) disponible Olsen mg/kg',
# 'Zinc (Zn) disponible Olsen mg/kg',
# 'Boro (B) disponible mg/kg',
# 'Hierro (Fe) disponible doble acido mg/kg',
# 'Cobre (Cu) disponible doble acido mg/kg',
# 'Manganeso (Mn) disponible doble acido mg/kg',
# 'Zinc (Zn) disponible doble acido mg/kg']

variables = ["ph","materia_organica","fosforo","azufre","acidez","aluminio","calcio","magnesio","potasio","sodio","cice","ce","hierro_olsen","cobre","manganeso","zinc_olsen","boro","hierro_doble_acido", "cobre_doble_acido","manganeso_doble_acido"]
features = []
for i in range(len(variables)):
    features.append({"label": variables[i], "value": i+1})

