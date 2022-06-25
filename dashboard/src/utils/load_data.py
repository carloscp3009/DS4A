import pandas as pd

# ------------------------------------------------------------------------------

lstVariables = [
    {"label": "Acidez", "value": "acidez"},
    {"label": "Aluminio", "value": "aluminio"},
    {"label": "Azufre", "value": "azufre"},
    {"label": "Boro", "value": "boro"},
    {"label": "Calcio", "value": "calcio"},
    {"label": "Coductividad eléctrica", "value": "ce"},
    {"label": "Coef. Intercambio Catiónico", "value": "cice"},
    {"label": "Cobre", "value": "cobre"},
    {"label": "Cobre doble ácido", "value": "cobre_doble_acido"},
    {"label": "Fósforo", "value": "fosforo"},
    {"label": "Hierro doble ácido", "value": "hierro_doble_acido"},
    {"label": "Hierro Olsen", "value": "hierro_olsen"},
    {"label": "Magnesio", "value": "magnesio"},
    {"label": "Manganeso", "value": "manganeso"},
    {"label": "Manganeso doble ácido", "value": "manganeso_doble_acido"},
    {"label": "Materia orgánica", "value": "materia_organica"},
    {"label": "Ph", "value": "ph"},
    {"label": "Potasio", "value": "potasio"},
    {"label": "Sodio", "value": "sodio"},
    {"label": "Zinc Olsen", "value": "zinc_olsen"}
]

lstDepartamentos = {
    "amazonas": {"descripcion": "Amazonas"},
    "antioquia": {"descripcion": "Antioquia"},
    "arauca": {"descripcion": "Arauca"},
    "atlantico": {"descripcion": "Atlántico"},
    "bolivar": {"descripcion": "Bolívar"},
    "boyaca": {"descripcion": "Boyacá"},
    "caldas": {"descripcion": "Caldas"},
    "caqueta": {"descripcion": "Caquetá"},
    "casanare": {"descripcion": "Casanare"},
    "cauca": {"descripcion": "Cauca"},
    "cesar": {"descripcion": "Cesar"},
    "choco": {"descripcion": "Chocó"},
    "cordoba": {"descripcion": "Córdoba"},
    "cundinamarca": {"descripcion": "Cundinamarca"},
    "guainia": {"descripcion": "Guainía"},
    "guaviare": {"descripcion": "Guaviare"},
    "huila": {"descripcion": "Huila"},
    "guajira": {"descripcion": "La Guajira"},
    "magdalena": {"descripcion": "Magdalena"},
    "meta": {"descripcion": "Meta"},
    "narino": {"descripcion": "Nariño"},
    "norte_santander": {"descripcion": "Norte de Santander"},
    "putumayo": {"descripcion": "Putumayo"},
    "quindio": {"descripcion": "Quindío"},
    "risaralda": {"descripcion": "Risaralda"},
    "santander": {"descripcion": "Santander"},
    "sucre": {"descripcion": "Sucre"},
    "tolima": {"descripcion": "Tolima"},
    "valle_cauca": {"descripcion": "Valle del Cauca"},
    "vaupes": {"descripcion": "Vaupés"},
    "vichada": {"descripcion": "Vichada"}
}

lstZonas = {
    "amazonia": {
        "descripcion": "Amazonía",
        "departamentos": [
            "amazonas", "caqueta", "guainia", "guaviare", "meta",
            "putumayo", "vaupes", "vichada"
        ]
    },
    "andina": {
        "descripcion": "Andina",
        "departamentos": [
            "antioquia", "boyaca", "caldas", "caqueta", "cauca", "cesar",
            "choco", "cundinamarca", "huila", "narino", "norte_santander",
            "putumayo", "quindio", "risaralda", "santander", "tolima",
            "valle_cauca"
        ]
    },
    "orinoquia": {
        "descripcion": "Orinoquía",
        "departamentos": [
            "arauca", "casanare", "meta", "vichada"
        ]
    },
    "pacifica": {
        "descripcion": "Pacífica",
        "departamentos": [
            "choco", "valle_cauca", "cauca", "narino"
        ]
    },
    "caribe": {
        "descripcion": "Caribe",
        "departamentos": [
            "atlantico", "bolivar", "cordoba", "magdalena", "cesar",
            "guajira", "sucre"
        ]
    }
}

df = pd.read_csv('data/suelos_preprocesado.csv')
