#!/bin/bash
DIRNAME=`dirname $0`
. $DIRNAME/lib.sh

if [ ! -f "$NAME" ]; then
    echo "preparing to dump $PGBASE.$LOUIS_SCHEMA to $PGDUMP_FILENAME"
    # apparently pg_dump doesn't use the environment variables PG*
    pg_dump -d $PGBASE --schema=$LOUIS_SCHEMA --no-owner --no-privileges --file $PGDUMP_FILENAME
else
    echo "File $PGDUMP_FILENAME already exists"
fi

if [ -f "$PGDUMP_FILENAME" ]; then
    if [ ! -f "$PGDUMP_FILENAME.zip" ]; then
        zip $PGDUMP_FILENAME.zip $PGDUMP_FILENAME
    else
        echo "File $PGDUMP_FILENAME.zip already exists"
    fi
fi