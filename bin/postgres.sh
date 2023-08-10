#!/bin/bash

DIRNAME=$(dirname `realpath $0`)
. $DIRNAME/lib.sh

PGDATA=$HOME/pgdata

if [ ! -d $PGDATA ]; then
    mkdir -p $PGDATA
fi

STATUS=`docker inspect louis-db-server -f '{{.State.Status}}'`

if [ "$STATUS" = "exited" ]; then
    docker start louis-db-server
elif [ "$STATUS" != "running" ]; then
    docker run --name louis-db-server \
        -e POSTGRES_PASSWORD=$PGPASSWORD \
        --network louis_network \
        --mount type=bind,src=$PGDATA,target=/var/lib/postgresql/data \
        --publish 5432:5432 \
        --user "$(id -u):$(id -g)" -v /etc/passwd:/etc/passwd:ro \
        -d louis-postgres
else
    echo "Postgres is already running"
fi
