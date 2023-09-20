#!/bin/bash
DIRNAME=$(dirname $(realpath $0))
PARENT_DIR=$DIRNAME/..
PROJECT_DIR=$(realpath $PARENT_DIR)
ENV_FILE=$PROJECT_DIR/.env

if [ -f "$ENV_FILE" ]; then
  # shellcheck source=lib.sh
  . "$ENV_FILE"
else
echo "WARNING: File $ENV_FILE does not exist, relying on environment variables"
fi

check_environment_variables_defined () {
    variable_not_set=0
    for VARIABLE in "$@"; do
        if [ -z "${!VARIABLE}" ]; then
            echo "Environment variable $VARIABLE is not set"
            variable_not_set=1
        fi
    done

    if [ $variable_not_set -eq 1 ]; then
        echo "One or more variables are not defined, the program cannot continue"
        exit 1
    fi
}

export PGOPTIONS="--search_path=$LOUIS_SCHEMA"
export PGBASE
export PGDATABASE
export PGHOST
export PGUSER
export PGPORT
export PGHOST
export PGPASSFILE
export PGPASSWORD

VERSION15=$(psql --version | grep 15.)

if [ -z "$VERSION15" ]; then
    echo "postgresql-client-15 required"
    exit 1
fi

TODAY=$(date +%Y-%m-%d)

if [ -z "$PGDUMP_FILENAME" ]; then
    PGDUMP_FILENAME=$PROJECT_DIR/dumps/$TODAY.$PGBASE.pg_dump
fi

export PSQL_ADMIN="psql -v ON_ERROR_STOP=1 --single-transaction -d $PGBASE"
