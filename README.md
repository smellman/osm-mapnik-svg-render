# osm-mapnik-svg-builder

This is a simple script that builds SVG files from OpenStreetMap data using the Mapnik library.

## Requirements

- Docker and Docker Compose

## Setup

```bash
cd data
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

- The output file
- The zoom/latitude/longitude (Hash)
- Width
- Height

This example, data/output.svg, will render a 1000x1000 SVG file centered at 35.635966, 140.161573 with a zoom level of 17.
