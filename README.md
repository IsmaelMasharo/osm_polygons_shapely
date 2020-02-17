# osm_polygons_shapely
City polygons fetched and displayed with shapely, keplergl and pandas.

- datasets:
  1. points.csv format: id, latitud, longitud. List of coordinates. Needs validation. Find location containing the points.

- notebooks file:
  1. retrieve_location_polygons.ipynb: notebook for exploratory analysis and prototyping
  2. points_location.ipynb: notebook for exploratory analysis and prototyping

- html_results file:
  1. retrieve_location_polygons.html: html version of notebook for exploratory analysis and prototyping
  2. points_location.html: html version of notebook for exploratory analysis and prototyping
  3. bogota_map.html: keplergl image of bogota locations
  4. points_map.html: keplergl image of valid points given in datasets/points.csv

- scripts file:
  1. retrieve_location_polygons.py: finale script for polygon location retrieval.
  2. points_location.py: finale script for finding location containing points.

- csv_results file:
  1. location_coordinates.csv format: location, latitud, longitud for bogota locations
  2. points_location.csv format: id, latitud, longitud, location. Location found for valid points in datasets/points.csv

Execute:
  - virtualenv env -p `which python3.7`
  - source env/bin/activate
  - pip install -r requirements.txt
  - python scripts/retrieve_location_polygons.py
  - python scripts/points_location.py
