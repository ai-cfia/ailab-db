#!/bin/bash
DIRNAME=`dirname $0`
. $DIRNAME/lib.sh
TODAY=`date +%Y-%m-%d`

if [ -z "$PGBASE" -o -z "$LOUIS_SCHEMA" ]; then
    echo "Environment variables PGBASE and LOUIS_SCHEMA must be specified"
    exit 1
fi

NAME=dumps/$LOUIS_SCHEMA.$TODAY.pg_dump
PGDUMP="docker exec -it louis-db-server pg_dump -U postgres -d $PGBASE"

if [ ! -f "$NAME" ]; then
    echo "Backing up $LOUIS_SCHEMA to $NAME"
    $PGDUMP --schema=$LOUIS_SCHEMA --no-owner --no-privileges > $NAME
    if [ "$?" -eq 0 ]; then
        echo "Dumped to $NAME"
    else
        echo "Error dumping to $NAME"
        cat $NAME
        rm $NAME
        exit 1
    fi
else
    echo "File $NAME already exists"
fi

ARCHIVE_FILENAME="$NAME.zip"
if [ ! -f "$ARCHIVE_FILENAME" ]; then
    zip $ARCHIVE_FILENAME $NAME
else
    echo "File $ARCHIVE_FILENAME.zip already exists"
fi

