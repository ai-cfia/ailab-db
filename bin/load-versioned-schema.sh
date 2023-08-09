DIRNAME=`dirname $0`
. $DIRNAME/lib.sh

if [ -z "$1" ]; then
    echo "usage: $0 source_schema"
    exit 1
fi
SOURCE_SCHEMA=$1
SOURCE_DIR=$DIRNAME/dumps/$1
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Directory does not exist: $SOURCE_DIR"
    exit 1
fi

SCHEMA_FILE=$SOURCE_DIR/schema.sql
if [ ! -f "$SCHEMA_FILE" ]; then
    echo "File does not exist: $SCHEMA_FILE"
    exit 2
fi
$PSQL_ADMIN < $SCHEMA_FILE
