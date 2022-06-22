# Geographical data 

### Notebooks

`geo_adjacency_and_reduction.ipynb` generates all the `*.json` and `*.geojson` on this folder.

### Data

* `adjacent_municipalities.json`: dictionary mapping a **municipality** ID to all of its adjacent regions (including itself)

* `limit_and_self_municipalities.json`: dictionary mapping a **department** ID to its own (internal) and  surrouding (external) municipalities.

* `Municipios_Colombia.geojson`: reduced polygon and name data for the municipalities. Has the columns:
	* `ID_DEP`, `NOMBRE_DEP`, `ID_MUN`, `NOMBRE_MUN`: (str) names and IDs for the municipalities and departments
	* `LATITUD`, `LONGITUD`: (float) pressumably, the centroid of the polygon
	* `AREA`: (float) pressumably, the area of the polygon
	* `adjacent`: (list) municipality codes for the adjacent municipalities
	* `geometry`: the polygon itself, simplified using [Douglas-Peucker](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.simplify.html) with 0.01 tolerance.

### Internal

`.gitignore` is set up to not include the heavy unprocessed data. 
