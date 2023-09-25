#!/bin/bash
DIRNAME=$(dirname "$(realpath "$0")")
. "$DIRNAME"/lib.sh

if [ -z "$PGDATA" ]; then  
    echo "PGDATA is not set. Setting to default directory..."  
    PGDATA=$HOME/pgdata  
fi  
  
if [ ! -d "$PGDATA" ]; then  
    echo "PGDATA directory $PGDATA does not exist, creating it..."  
    mkdir -p "$PGDATA"  
fi  

check_environment_variables_defined DB_SERVER_CONTAINER_NAME POSTGRES_PASSWORD 

STATUS=$(docker inspect "$DB_SERVER_CONTAINER_NAME" -f '{{.State.Status}}')

if [ "$STATUS" = "exited" ]; then
    echo "container $DB_SERVER_CONTAINER_NAME exist but has exited, restarting"
    docker start "$DB_SERVER_CONTAINER_NAME"

elif [ "$STATUS" != "running" ]; then

    echo "container $DB_SERVER_CONTAINER_NAME does not exist, creating"

    docker run --name "$DB_SERVER_CONTAINER_NAME" \
        -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
        --network louis_network \
        --mount type=bind,src="$PGDATA",target=/var/lib/postgresql/data \
        --publish 5432:5432 \
        --user "$(id -u):$(id -g)" -v /etc/passwd:/etc/passwd:ro \
        -d "louis-postgres"
else
    echo "Postgres is already running"
fi
