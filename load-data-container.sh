#!/bin/bash

if [ -z "$LOUIS_DSN" ]; then
    echo "please set LOUIS_DSN to psql connection string before running"
    echo "export LOUIS_DSN=..."
    exit 1
fi

if [ -z "$1" ]; then
    echo "usage: $0 LOUIS_SCHEMA"
    exit 2
fi

LOUIS_SCHEMA=$1
VOLUME_NAME=louis-data-$LOUIS_SCHEMA

PODMAN_CONTAINER=localhost/louis-dataloader:latest
echo "loading $LOUIS_SCHEMA with $PODMAN_CONTAINER"
podman run -it --rm \
    -e LOUIS_DSN="$LOUIS_DSN" \
    -e LOUIS_SCHEMA=$LOUIS_SCHEMA \
    -e LOAD_DATA_ONLY=$LOAD_DATA_ONLY \
    -e DISABLE_TRIGGER_ALL=$DISABLE_TRIGGER_ALL \
    -v $VOLUME_NAME:/data \
    $PODMAN_CONTAINER