DIRNAME=`dirname $0`
. $DIRNAME/.env
export PGDATABASE
export PGHOST
export PGUSER
export PGPORT
export PGHOST
export PGPASSFILE
export PGPASSWORD

PSQL_ADMIN="psql -v ON_ERROR_STOP=1 -U postgres --single-transaction"
LOUIS_SCHEMA=louis_v003
TODAY=`date +%Y-%m-%d`
