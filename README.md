# osm-mapnik-svg-builder

This is a simple script that builds SVG file or PDF file from OpenStreetMap data using the Mapnik library.

This repository is based on [OpenStreetMap Carto](https://github.com/gravitystorm/openstreetmap-carto) master branch.

## Requirements

- Docker and Docker Compose

## Setup

Download the OSM data into data directory and build the docker images:

```bash
cd data
# Download the OSM data
aria2c https://download.geofabrik.de/asia/japan/kanto-241206.osm.pbf
cd ..
docker compose pull
docker compose build
```

## Preparing the database

Open a shell for the postgresql container:

```bash
docker compose up postgres
```

Open a shell for the import container:

```bash
docker compose run --rm import kanto-241206.osm.pbf
```

## Usage

```bash
docker compose run --rm -u $(id -u):$(id -g) app /data/output.svg 17/35.635966/140.161573 1000 1000
```

The arguments are:

- The output file, which can be a SVG or PDF file
- The zoom/latitude/longitude (Hash)
- Width
- Height
- (Optional) Custom attribution

This example, data/output.svg, will render a 1000x1000 SVG file centered at 35.635966, 140.161573 with a zoom level of 17.

## Help

See the help message:

```
❯ docker compose run --rm -u $(id -u):$(id -g) app --help
usage: app.py [-h] [--attribution ATTRIBUTION] output_file hash width height

Mapnik rendering svg file

positional arguments:
  output_file           output svg/pdf file
  hash                  hash (ex. 18/35.636056/140.160160)
  width                 width
  height                height

options:
  -h, --help            show this help message and exit
  --attribution ATTRIBUTION
                        custom attribution, if you don't want to embed attribution, set empty value
```
