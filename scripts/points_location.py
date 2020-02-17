#!/usr/bin/env python
# coding: utf-8

from shapely.geometry import Polygon, Point
from keplergl import KeplerGl
import pandas as pd


def load_polygons_in_map(df):
    bogota_map = KeplerGl(height=500)
    for location_name in df.Location.unique():
        bogota_map.add_data(data=df[df.Location == location_name], name=location_name)
    return bogota_map


def remove_outlier(df_in):
    for col_name in ['Latitude', 'Longitude']:
        q1 = df_in[col_name].quantile(0.05)
        q3 = df_in[col_name].quantile(0.95)
        iqr = q3 - q1
        fence_low  = q1 - 1.5*iqr
        fence_high = q3 + 1.5*iqr
        df_out = df_in.loc[
            (df_in[col_name] > fence_low) & 
            (df_in[col_name] < fence_high)
        ]
    return df_out


def cleaned_load_locations():
    return pd.read_csv(
        '../csv_results/location_coordinates.csv', header=0, 
        names=['Location', 'Latitude', 'Longitude']
    )


def cleaned_load_points():
    points = pd.read_csv('../datasets/points.csv', error_bad_lines=False, index_col='id')
    initial_points_shape = points.shape

    points.columns = ['Latitude', 'Longitude']
    points['Latitude'] = pd.to_numeric(points['Latitude'], errors='coerce').round(6)
    points['Longitude'] = pd.to_numeric(points['Longitude'], errors='coerce').round(6)
    points.dropna(inplace=True)
    points = remove_outlier(points)
    final_points_shape = points.shape

    print('initial shape:', initial_points_shape, 'final shape', final_points_shape)

    return points


def get_polygons_shape_objects(df):
    location_shapes = {}
    for location_name in df.Location.unique():
        data=df[df.Location == location_name]
        lat = data.Latitude.tolist()
        lon = data.Longitude.tolist()
        location_shapes[location_name] = Polygon(list(zip(lat, lon)))
    return location_shapes


def point_location(point, shapes):
    for location_name, polygon in shapes.items():
        if polygon.contains(point):
            return location_name
    return '-'


def main():

    points_df = cleaned_load_points()
    points_map = KeplerGl(height=500)
    points_map.add_data(data=points_df, name="points")

    bogota_df = cleaned_load_locations()
    bogota_map = load_polygons_in_map(bogota_df)
    bogota_map.add_data(data=points_df, name="points")

    bogota_map.save_to_html(file_name='bogota_map.html')
    points_map.save_to_html(file_name='points_map.html')

    shapes = get_polygons_shape_objects(bogota_df)
    points_df['Location'] = points_df.apply(
        lambda row: point_location(
                Point(row.Latitude, row.Longitude), shapes
            ), 
        axis = 1
    )

    points_df = points_df[points_df.Location != '-']

    points_df.to_csv('points_location.csv')

if __name__ == "__main__":
    main()