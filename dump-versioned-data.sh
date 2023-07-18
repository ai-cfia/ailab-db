DIRNAME=`dirname $0`
. $DIRNAME/lib.sh
if [ -z "$2" ]; then
    echo "usage: $0 input_schema output_schema"
    exit 1
fi
INPUT_SCHEMA=$1
OUTPUT_SCHEMA=$2

if [ -z "$PGHOST" -o "$PGHOST" == "localhost" ]; then
    RELPATH=dumps/$OUTPUT_SCHEMA
    OUTPUT_DIR=`realpath $RELPATH`
    if [ -d "$OUTPUT_DIR" ]; then
       echo "Warning: Directory exist: $OUTPUT_DIR"
    fi
    mkdir -p "$OUTPUT_DIR" || exit 2
else
    OUTPUT_DIR=/var/lib/postgresql/data
fi

$PSQL_ADMIN < $DIRNAME/sql/schema_to_csv.sql

echo "Outputting all tables from schema $INPUT_SCHEMA as csv to $OUTPUT_DIR on the database server"
$PSQL_ADMIN -c "select * from schema_to_csv('$INPUT_SCHEMA', '$OUTPUT_DIR')"