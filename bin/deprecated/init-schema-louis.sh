SCHEMA_NAME="louis-v001.sql"

SQL_FILE=sql/$SCHEMA_NAME.sql
DBNAME=inspection.canada.ca
if [ ! -f "$SQL_FILE" ]; then
    echo "$SQL_FILE does not exist"
    exit 1
fi

psql "dbname=$DBNAME" -c "CREATE SCHEMA IF NOT EXISTS \"$SCHEMA_NAME\""
if [ "$?" -ne 0 ]; then
    echo "Schema creation $SCHEMA_NAME failed"
    exit 2
fi
psql "dbname=$DBNAME options=--search-path=$SCHEMA_NAME,public" -f $SQL_FILE