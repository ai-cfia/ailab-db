DIRNAME=`dirname $0`
. $DIRNAME/lib.sh
RELPATH=dumps/$TARGET_SCHEMA
SOURCE_DIR=`realpath $RELPATH`
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Directory does not exist: $SOURCE_DIR"
    exit 1
fi

$PSQL_ADMIN -d $PGBASE < $DIRNAME/sql/csv_to_schema.sql
$PSQL_ADMIN -d $PGBASE -c "select * from csv_to_schema('$TARGET_SCHEMA', '$SOURCE_DIR', array['crawl', 'chunk', 'token', 'ada_002', 'link', 'score', 'query'])"