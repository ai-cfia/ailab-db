#!/bin/bash
DIRNAME=$(dirname "$0")
. $DIRNAME/lib.sh

## To debug
# set -x -e  

if [ -z "$1" ]; then
    echo "usage: $0 target_schema"
    exit 1
fi
TARGET_SCHEMA=$1
SOURCE_DIR=$PROJECT_DIR/dumps/$TARGET_SCHEMA
CSV_TO_SCHEMA=$PROJECT_DIR/sql/csv_to_schema.sql

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Directory does not exist: $SOURCE_DIR"
    exit 1
fi

if [ ! -f "$CSV_TO_SCHEMA" ]; then
    echo "Source file does not exist: $CSV_TO_SCHEMA"
    exit 1
fi

# $PSQL_ADMIN -d $PGBASE < $CSV_TO_SCHEMA
# if [ $? -ne 0 ]; then
#     echo "Failed to load csv_to_schema.sql"
#     exit 1
# fi
# $PSQL_ADMIN -d $PGBASE -c "select * from csv_to_schema('$TARGET_SCHEMA', '$SOURCE_DIR', array['crawl', 'chunk', 'token', 'ada_002', 'link', 'score', 'query'])"

TABLE_LIST=$SOURCE_DIR/tables.txt
echo $TABLE_LIST
if [ ! -f "$TABLE_LIST" ]; then
    echo "File defining list of table and their load order does not exist: $TABLE_LIST"
    exit 1
fi
TABLES=$(cat "$TABLE_LIST")

# we check that there's a csv file for each table
for table in $TABLES; do
    FILENAME=$SOURCE_DIR/$table.csv
    if [ ! -f "$FILENAME" ]; then
        echo "File does not exist: $FILENAME"
        exit 1
    fi
done

# we check that there's a table for each csv file
for file in $SOURCE_DIR/*.csv; do
    echo "Checking $file is expected in table list"
    TABLE=`basename $file .csv`
    if ! grep -q $TABLE $TABLE_LIST; then
        echo "File $file is not expected in table list"
        exit 1
    fi
done

CSV_TO_SCHEMA_PSQL=$(mktemp)
echo "" > $CSV_TO_SCHEMA_PSQL
# echo "set session_replica_role = 'replica';" >> $CSV_TO_SCHEMA_PSQL
for table in $TABLES; do
    echo "Loading $table"
    FILENAME=$SOURCE_DIR/$table.csv
    echo "\COPY $TARGET_SCHEMA.$table FROM $FILENAME WITH DELIMITER as ';' CSV HEADER" >> $CSV_TO_SCHEMA_PSQL
done
$PSQL_ADMIN -f $CSV_TO_SCHEMA_PSQL
if [ $? -ne 0 ]; then
    echo "Failed to load $table"
    exit 1
fi