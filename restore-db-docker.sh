DIRNAME=`dirname $0`
. $DIRNAME/lib.sh

if [ -z "$PGBASE" ]; then
    echo "PGBASE is not set"
    exit 1
fi

if [ -z "$1" ]; then
    echo "usage: $0 dump_path"
    exit 1
fi
DUMP=$1
DOCKER_EXEC="docker exec -it louis-db-server"
$DOCKER_EXEC $PSQL_ADMIN -f "$DUMP"