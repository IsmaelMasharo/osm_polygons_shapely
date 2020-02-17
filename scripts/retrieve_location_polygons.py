#!/usr/bin/env python
# coding: utf-8

# Imports

from shapely.geometry import Polygon, Point, shape
import requests
import json
import csv
import numpy as np
import pandas as pd

# osm base url
base_url = "http://nominatim.openstreetmap.org/search.php"


# Bogota Locations list
bogota_locations = [
    'Usaquén',
    'Santa Fe',
    'San Cristobal',
    'Usme',
    'Tunjuelito',
    'Bosa',
    'Kennedy',
    'Fontibón',
    'Engativá',
    'Suba',
    'Chapinero',
    'Barrios Unidos',
    'Teusaquillo',
    'Los Mártires',
    'Antonio Nariño',
    'Puente Aranda',
    'La Candelaria',
    'Rafael Uribe Uribe',
    'Ciudad Bolívar',
    'Sumapaz'
]


# Function definition for geojson request
def get_location_polygon(location, base_url):
    params = {
        'q':f'{location} bogota colombia',
        'polygon_geojson':1,
        'format':'json',
    }

    json_response = requests.get(
        url=base_url, params=params
    ).json()

    polygon = None
    for osm_json in json_response:
        geo_field = osm_json.get('geojson')
        if (
            geo_field and geo_field['type'] == 'Polygon'
        ):
            return shape(geo_field)

    if not polygon:
        raise Exception(f'polygon location {location} was not found.')


def get_bogota_polygons():
    bogota_polygons = {}
    for location in bogota_locations:
        polygon = get_location_polygon(location, base_url)
        bogota_polygons[location] = polygon
    return bogota_polygons


def main():
    bogota_polygons = get_bogota_polygons()

    rafael_uribe_url = 'https://global.mapit.mysociety.org/area/1047873.geojson'
    rafael_uribe_json = requests.get(url=rafael_uribe_url).json()
    rafael_uribe_polygon = shape(rafael_uribe_json)

    bogota_polygons['Rafael Uribe Uribe'] = rafael_uribe_polygon

    with open("location_coordinates.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["location", "latitud", "longitud"])
        for location, polygon in bogota_polygons.items():
            x, y = polygon.exterior.coords.xy
            latitude = y.tolist()
            longitude = x.tolist()
            location = [location]*len(latitude)
            coordinates = list(zip(location, latitude, longitude))
            writer.writerows(coordinates)

if __name__ == "__main__":
    main()