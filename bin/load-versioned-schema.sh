#!/bin/bash
DIRNAME=$(dirname "$0")
. $DIRNAME/lib.sh

## To debug
# set -x -e  

## Explain usage if missing argument
if [ -z "$1" ]; then
    echo "usage: $0 source_schema"
    exit 1
fi

SOURCE_SCHEMA=$1  
  
## Create a path using the project directory and the schema name  
SOURCE_DIR=$PROJECT_DIR/dumps/$1  
  
## If the directory at the path doesn't exist, print an error and exit  
if [ ! -d "$SOURCE_DIR" ]; then  
    echo "Directory does not exist: $SOURCE_DIR"  
    exit 1  
fi  

## Create a path to a file named schema.sql
SCHEMA_FILE=$SOURCE_DIR/schema.sql  
  
## If the file does not exist, print an error message and exit with status code 2
if [ ! -f "$SCHEMA_FILE" ]; then    
    echo "File does not exist: $SCHEMA_FILE"  
    exit 2  
fi  
## If the file does exist, pass it as input to a PostgreSQL admin command  
$PSQL_ADMIN < $SCHEMA_FILE  
