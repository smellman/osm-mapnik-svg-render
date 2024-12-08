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
docker compose run --rm -u $(id -u):$(id -g) app /data/output.svg 
```
