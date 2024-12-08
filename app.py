#!/usr/bin/env python3

import argparse
import mapnik

def render_map(output_file, hash, width, height):
    # Create a map
    m = mapnik.Map(width, height)
    mapnik.load_map(m, '/src/openstreetmap-carto/mapnik.xml')

    # Create a bounding box
    bbox = mapnik.Box2d(*map(float, hash.split('/')))

    # Zoom to the bounding box
    m.zoom_to_box(bbox)

    # Render the map to an image
    im = mapnik.Image(width, height)
    mapnik.render(m, im)

    # Save the image to a file
    im.save(output_file, 'svg')

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