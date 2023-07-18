#!/bin/bash
DIRNAME=`dirname $0`
. $DIRNAME/lib.sh
TODAY=`date +%Y-%m-%d`

if [ -z $2 ]; then
    echo "usage: $0 source_schema output_schema"
    exit 1
fi

SOURCE_SCHEMA=$1
TARGET_SCHEMA=$2

SCHEMA_OUTPUT_DIR=$DIRNAME/dumps/$TARGET_SCHEMA
mkdir -p $SCHEMA_OUTPUT_DIR
SCHEMA_OUTPUT_FILENAME=$SCHEMA_OUTPUT_DIR/schema.sql
if [ -f "$SCHEMA_OUTPUT_FILENAME" ]; then
    echo "File $SCHEMA_OUTPUT_FILENAME already exists"
    #exit 2
fi
pg_dump -n $SOURCE_SCHEMA -d $PGBASE \
    --no-owner --no-privileges --no-security-labels \
    --no-table-access-method --no-tablespaces --schema-only \
    | grep -v "^SELECT pg_catalog.set_config('search_path', '', false);" \
    | sed s/$SOURCE_SCHEMA/$TARGET_SCHEMA/g > $SCHEMA_OUTPUT_FILENAME