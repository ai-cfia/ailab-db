DIRNAME=`dirname $0`
PARENT_DIR=$DIRNAME/..
PROJECT_DIR=`realpath $PARENT_DIR`
ENV_FILE=$PROJECT_DIR/.env

if [ -f "$ENV_FILE" ]; then
  . $ENV_FILE
else
  echo "WARNING: File $ENV_FILE does not exist, relying on environment variables"
fi

REQUIRED_ENVIRONMENT_VARIABLES="LOUIS_DSN PGBASE PGUSER PGPASSWORD PGHOST OPENAI_API_KEY AZURE_OPENAI_SERVICE LOUIS_SCHEMA"
for VARIABLE in $REQUIRED_ENVIRONMENT_VARIABLES; do
    if [ -z "${!VARIABLE}" ]; then
        echo "Environment variable $VARIABLE is not set"
        exit 1
    fi
done

export PGBASE
export PGDATABASE
export PGHOST
export PGUSER
export PGPORT
export PGHOST
export PGPASSFILE
export PGPASSWORD

PSQL_ADMIN="psql -v ON_ERROR_STOP=1 -U postgres --single-transaction -d $PGBASE"
TODAY=`date +%Y-%m-%d`

if [ -z "$PGDUMP_FILENAME" ]; then
    PGDUMP_FILENAME=$PROJECT_DIR/dumps/$TODAY.$PGBASE.pg_dump
fi
