#!/usr/bin/env python3

import argparse
import mapnik
import cairo
import math

WORLD_SIZE = 40075016.686
TILE_SIZE = 256

def zoom_level_to_scale(zoom: int) -> float:
    return WORLD_SIZE / (TILE_SIZE * 2 ** zoom)

def lon_to_mercator(lon: float) -> float:
    return lon * (WORLD_SIZE / 360.0)

def lat_to_mercator(lat: float) -> float:
    rad = math.radians(lat)
    return math.log(math.tan(math.pi / 4 + rad / 2)) * (WORLD_SIZE / (2 * math.pi))

def calculate_bbox(center_lon: float, center_lat: float, zoom: int, width: int, height: int) -> mapnik.Box2d:
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

def render_map(output_file: str, hash: str, width: int, height: int, attribution: str):
    # Check the output file extension
    if not (output_file.endswith('.svg') or output_file.endswith('.pdf')):
        raise ValueError('output_file must be svg or pdf')

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

    # Render the svg file or pdf file
    if (output_file.endswith('.svg')):
        surface = cairo.SVGSurface(output_file, width, height)
        surface.restrict_to_version(cairo.SVG_VERSION_1_2)
    else:
        surface = cairo.PDFSurface(output_file, width, height)
        surface.restrict_to_version(cairo.PDF_VERSION_1_5)
    context = cairo.Context(surface)
    mapnik.render(m, context)
    # attribution
    if len(attribution) > 0:
        context.set_font_size(20)
        context.select_font_face("Noto Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        context.set_source_rgb(0, 0, 0)
        padding_width = 11 * len(attribution)
        x, y = width - padding_width - 10, height - 10
        context.move_to(x, y)
        context.show_text(attribution)
    surface.finish()

def main():
    parser = argparse.ArgumentParser(description='Mapnik rendering svg file')
    parser.add_argument('output_file', type=str, help='output svg/pdf file')
    parser.add_argument('hash', type=str, help='hash (ex. 18/35.636056/140.160160)')
    parser.add_argument('width', type=int, help='width')
    parser.add_argument('height', type=int, help='height')
    parser.add_argument('--attribution', type=str, help="custom attribution, if you don't want to embed attribution, set empty value", default="@ OpenStreetMap contributors")

    args = parser.parse_args()
    render_map(args.output_file, args.hash, args.width, args.height, args.attribution)

if __name__ == '__main__':
    main()