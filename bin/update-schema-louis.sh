DIRNAME=`dirname $0`
. $DIRNAME/lib.sh
DBNAME=inspection.canada.ca

SCHEMA_SOURCE=$1
SCHEMA_TARGET=$2

SQL_FILE=sql/$SCHEMA_TARGET.sql
if [ ! -f "$SQL_FILE" ]; then
    echo "$SQL_FILE does not exist"
    exit 1
fi

$PSQL_ADMIN "dbname=$DBNAME" -c "select clone_schema('$SCHEMA_SOURCE', '$SCHEMA_TARGET', false);"
if [ "$?" -ne 0 ]; then
    echo "Schema cloning from $SCHEMA_SOURCE to $SCHEMA_TARGET failed"
    exit 2
fi
$PSQL_ADMIN  "dbname=$DBNAME options=--search-path=$SCHEMA_TARGET,public" -f $SQL_FILE