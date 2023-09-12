#!/bin/bash

DIRNAME=$(dirname `realpath $0`)
. $DIRNAME/lib.sh

PGDATA=$HOME/pgdata

if [ ! -d $PGDATA ]; then
    mkdir -p $PGDATA
fi

STATUS=`docker inspect louis-db-server -f '{{.State.Status}}'`

if [ "$STATUS" = "exited" ]; then
    # Check if $DB_SERVER_CONTAINER_NAME is empty
    source ./lib.sh
    is_parameter_empty $DB_SERVER_CONTAINER_NAME
    is_parameter_empty_DB_SERVER_CONTAINER_NAME=$?

    if [ $is_parameter_empty_DB_SERVER_CONTAINER_NAME -eq 0 ];
    then
        echo "DB_SERVER_CONTAINER_NAME is not defined or empty."
    else
        echo "container exist $DB_SERVER_CONTAINER_NAME but has exited, restarting"
        docker start louis-db-server
    fi

elif [ "$STATUS" != "running" ]; then
    # Check if $PGPASSWORD is empty
    source ./lib.sh
    is_parameter_empty $PGPASSWORD
    is_parameter_empty_PGPASSWORD=$?

    if [ $is_parameter_empty_PGPASSWORD -eq 0 ];
    then
        echo "PGPASSWORD is not defined or empty."
    else
        echo container does not exist, creating
        docker run --name louis-db-server \
            -e POSTGRES_PASSWORD=$PGPASSWORD \
            --network louis_network \
            --mount type=bind,src=$PGDATA,target=/var/lib/postgresql/data \
            --publish 5432:5432 \
            --user "$(id -u):$(id -g)" -v /etc/passwd:/etc/passwd:ro \
            -d louis-postgres
    fi
else
    echo "Postgres is already running"
fi
