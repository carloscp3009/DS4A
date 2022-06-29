# Geographical data

### Notebooks

##### `geo_adjacency_and_reduction.ipynb` (python)

generates all the `*.json` and `*.geojson` on this folder.

##### `altitude_query.nb` (wolfram mathematica)

Queries the geoJSON polygons for altitude data. Produces `altitud.csv`.


### Data

* `adjacent_municipalities.json`: dictionary mapping a **municipality** ID to all of its adjacent municipalities (including itself).

* `adjacent_departments.json`: dictionary mapping a **department** ID to all of its adjacent departments (including itself).

* `muns_of_adjacent_deps.json`: dictionary mapping a **department¨** ID to the municipalities of its adjacent departments (including itself).

* `Municipios_Colombia.geojson`: reduced polygon and name data for the municipalities. Has the columns:
	* `ID_DEP`, `NOMBRE_DEP`, `ID_MUN`, `NOMBRE_MUN`: (str) names and IDs for the municipalities and departments.
	* `LATITUD`, `LONGITUD`: (float) pressumably, the centroid of the polygon.
	* `AREA`: (float) pressumably, the area of the polygon.
	* `adjacent`: (string) municipality codes for the adjacent municipalities, joined by spaces.
	* `geometry`: the polygon itself, simplified using [Douglas-Peucker](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.simplify.html) with 0.01 tolerance.
    
* `altitud.csv`: table of municipality ID and mean altitude, using a grid of 1km.

### Internal

`.gitignore` is set up to not include the heavy unprocessed data. 
