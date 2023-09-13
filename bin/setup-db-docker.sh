#!/bin/bash
DIRNAME=$(dirname "$0")
. $DIRNAME/lib.sh

check_environment_variables_defined PGBASE DB_SERVER_CONTAINER_NAME PSQL_ADMIN

DOCKER_EXEC="docker exec -it $DB_SERVER_CONTAINER_NAME"
$DOCKER_EXEC createdb -E utf-8 -U postgres $PGBASE 
$DOCKER_EXEC $PSQL_ADMIN -c "CREATE USER $USER; ALTER USER $USER WITH SUPERUSER;"
$DOCKER_EXEC pip install pgxnclient
$DOCKER_EXEC pgxn install vector
$DOCKER_EXEC $PSQL_ADMIN -c "SET search_path TO public; CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"; CREATE EXTENSION IF NOT EXISTS vector;"