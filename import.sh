#!/bin/bash

# Check data file
if [ $# -le 0 ]; then
  echo "Usage: $0 <datafile>"
  exit 1
fi
OSM2PGSQL_DATAFILE=$1
if [ ! -f /data/$OSM2PGSQL_DATAFILE ]; then
  echo "Data file not found: $OSM2PGSQL_DATAFILE"
  exit 1
fi

# Enable hstore extension
psql postgresql://gis:gis@postgres:5432/gis -c 'CREATE EXTENSION hstore;'

# Import data
osm2pgsql \
  --slim \
  --drop \
  --cache 8000 \
  --number-processes $(nproc) \
  -O flex \
  --database "host=postgres port=5432 user=gis password=gis dbname=gis" \
  --style /src/openstreetmap-carto/openstreetmap-carto-flex.lua \
  /data/$OSM2PGSQL_DATAFILE

if [ $? -ne 0 ]; then
  echo "Failed to import data"
  exit 1
fi

# Import external data
cd /src/openstreetmap-carto
python3 scripts/get-external-data.py -D /data -d gis -H postgres -U gis -w gis

# Create indexes
psql postgresql://gis:gis@postgres:5432/gis -f indexes.sql

# Create functions
psql postgresql://gis:gis@postgres:5432/gis -f functions.sql