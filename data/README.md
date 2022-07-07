# Data flux: preprocessing phase

## 1. `suelos_preprocesamiento.ipynb`

From `suelos_original.csv` generates `suelos_preprocesado.csv`.

#### 1.1 Column name fixing

#### 1.2 Delete empty columns

#### 1.3 Float columns formatting

#### 1.4 String columns formatting

#### 1.5 Invalid data elimination

#### 1.6 create Dummy variables

## 2. `geo_name_correction.ipynb`

From `suelos_preprocesado.csv` generates `suelos_geolocalizado`.

#### `cannonicalize` package

#### 2.1 Correct department names

#### 2.2 Correct department-municipality name tuples

#### 2.3 Replace the DIVPOLA codification for each municipalities


## 3. `database_creation.ipynb`

On all tablesm names are capitalized, with the exception of the following stopwords: `{"y","la","el","de","del","los"}`.

### Tables

From `suelos_geolocalizado.csv` and the geographical datasets `geo/Municipios_Colombia.geojson` and `geo/altitud.csv`, generates `../dashboard/src/data/database.db`.

#### `municipios`

| column | type | notes |
| - | - | - |
| `cod_municipio` | string | Index, fixed length 5 |
| `cod_departamento` | string | fixed length 2 |
| `departamento` | string | name |
| `municipio` | string | name |
| `latitud` | float | centroid |
| `longitud` | float | centroid |
| `altitud` | float | mean of a 1km grid | 

#### `departamentos`

| column | type | notes |
| :- | :- | :- |
| `cod_departamento` | string | Index, fixed length 2, connection with `municipios` table |
| `departamento` | string | name |
| `AMA` | boolean | Amazonian region pertenence |
| `AND` | boolean | Andes region pertenence |
| `ORI` | boolean | Orinoquia pertenence |
| `PAC` | boolean | Pacific pertenence |
| `CAR` | boolean | Caribbean pertenence |


#### `zonas`

| column | type | notes |
| - | - | - |
| `cod_region` | string | Index, fixed length 3 |
| `region` | string | name |


#### `analisis`

| column | type | notes |
| - | - | - |
| `id` | integer | Index, sequential from 0 to 46449 |
| `cod_municipio` | string | connection with `municipios` table |
| `cultivo` | string | name of the crop |
| `fertilizantes` | string | fertilizer details |
| (chemical variables)* | float | |
| (dummy columns)  ** | boolean | |


##### * Chemical variables 

| column | spec |
| - | - |
| ph | pH agua:suelo 2,5:1,0 |
| materia_organica | Materia orgánica (MO) % |
| fosforo | Fósforo (P) Bray II mg/kg |
| azufre | Azufre (S) Fosfato monocalcico mg/kg |
| acidez | Acidez (Al+H) KCL cmol(+)/kg |
| aluminio | Aluminio (Al) intercambiable cmol(+)/kg |
| calcio | Calcio (Ca) intercambiable cmol(+)/kg |
| magnesio | Magnesio (Mg) intercambiable cmol(+)/kg |
| potasio | Potasio (K) intercambiable cmol(+)/kg |
| sodio | Sodio (Na) intercambiable cmol(+)/kg |
| cice | capacidad de intercambio cationico (CICE) suma de bases cmol(+)/kg |
| ce | Conductividad el‚ctrica (CE) relacion 2,5:1,0 dS/m |
| hierro_olsen | Hierro (Fe) disponible olsen mg/kg |
| cobre | Cobre (Cu) disponible mg/kg |
| manganeso | Manganeso (Mn) disponible Olsen mg/kg |
| zinc_olsen | Zinc (Zn) disponible Olsen mg/kg |
| boro | Boro (B) disponible mg/kg |
| hierro_doble_acido | Hierro (Fe) disponible doble  cido mg/kg |
| cobre_doble_acido | Cobre (Cu) disponible doble acido mg/kg |
| manganeso_doble_acido | Manganeso (Mn) disponible doble acido mg/kg |
| zinc_doble_acido | Zinc (Zn) disponible doble  cido mg/kg |

##### ** Dummy columns

* tiempo_establecimiento
* topografia
* drenaje
* riego
















