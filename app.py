#!/usr/bin/env python3

import argparse
import mapnik
import cairo
import math

WORLD_SIZE = 40075016.686
TILE_SIZE = 256

def zoom_level_to_scale(zoom):
    return WORLD_SIZE / (TILE_SIZE * 2 ** zoom)

def lon_to_mercator(lon):
    return lon * (WORLD_SIZE / 360.0)

def lat_to_mercator(lat):
    rad = math.radians(lat)
    return math.log(math.tan(math.pi / 4 + rad / 2)) * (WORLD_SIZE / (2 * math.pi))

def calculate_bbox(center_lon, center_lat, zoom, width, height):
    scale = zoom_level_to_scale(zoom)
    mercator_lat = lat_to_mercator(center_lat)
    mercator_lon = lon_to_mercator(center_lon)
    half_width = (scale * width) / 2
    half_height = (scale * height) / 2
    return mapnik.Box2d(
        mercator_lon - half_width,
        mercator_lat - half_height,
        mercator_lon + half_width,
        mercator_lat + half_height,
    )

def render_map(output_file, hash, width, height):
    # Create a map
    m = mapnik.Map(width, height)
    mapnik.load_map(m, '/src/openstreetmap-carto/mapnik.xml')

    # Get center and zoom from the hash
    center = map(float, hash.split('/')[1:3])
    center_lat, center_lon = center
    zoom = int(hash.split('/')[0])
    bbox = calculate_bbox(center_lon, center_lat, zoom, width, height)

    # Zoom to the bounding box
    m.zoom_to_box(bbox)

    # Render the svg file
    surface = cairo.SVGSurface(output_file, width, height)
    surface.restrict_to_version(cairo.SVG_VERSION_1_2)
    mapnik.render(m, surface)
    surface.finish()

def main():
    parser = argparse.ArgumentParser(description='Mapnik rendering svg file')
    parser.add_argument('output_file', type=str, help='output svg file')
    parser.add_argument('hash', type=str, help='hash (ex. 18/35.636056/140.160160)')
    parser.add_argument('width', type=int, help='width')
    parser.add_argument('height', type=int, help='height')

    args = parser.parse_args()
    render_map(args.output_file, args.hash, args.width, args.height)

if __name__ == '__main__':
    main()