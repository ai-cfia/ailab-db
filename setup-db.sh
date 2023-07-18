DIRNAME=`dirname $0`
. $DIRNAME/lib.sh

$PSQL_ADMIN -f $DIRNAME/sql/fix-utf8-template.sql
$PSQL_ADMIN -c "CREATE USER $USER; ALTER USER $USER WITH SUPERUSER;"
createdb -E utf-8 $PGBASE
pip install pgxnclient
pgxn install vector

$PSQL_ADMIN -c "SET search_path TO public; CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"; CREATE EXTENSION IF NOT EXISTS vector;"