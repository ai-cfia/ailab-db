DIRNAME=`dirname $0`
. $DIRNAME/lib.sh

if [ -z "$PGBASE" ]; then
    echo "PGBASE is not set"
    exit 1
fi
DOCKER_EXEC="docker exec -it louis-db-server"
$DOCKER_EXEC createdb -E utf-8 $PGBASE
$DOCKER_EXEC $PSQL_ADMIN -c "CREATE USER $USER; ALTER USER $USER WITH SUPERUSER;"
$DOCKER_EXEC pip install pgxnclient
$DOCKER_EXEC pgxn install vector
$DOCKER_EXEC $PSQL_ADMIN -c "SET search_path TO public; CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"; CREATE EXTENSION IF NOT EXISTS vector;"