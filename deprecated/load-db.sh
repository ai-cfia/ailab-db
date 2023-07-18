#!/bin/bash

if [ -z "$1" ]; then
    echo "specify path to db dump or SQL schema"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Not a valid filename: $1"
    exit 1
fi
psql -v ON_ERROR_STOP=1 --single-transaction -d inspection.canada.ca < $1
