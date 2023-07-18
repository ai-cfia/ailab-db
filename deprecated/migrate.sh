
set -x

SCHEMA_CHANGES=sql/schema2.sql

DUMP_FILENAME="sql/2023-06-01-inspectioncanadaca.pgdump_schema.sql"
if [ ! -f "$DUMP_FILENAME" ]; then
    pg_dump -s --no-owner --no-privileges --no-comments --no-publications --no-security-labels --no-subscriptions --no-table-access-method --no-tablespaces \
        -h inspectioncanadaca.postgres.database.azure.com \
        -d inspectioncanadaca -U louisreadonly \
        > sql/2023-06-01-inspectioncanadaca.pgdump_schema.sql
fi

PUBLIC_NEW="$DUMP_FILENAME.public_new.sql"

if [ ! -f "$PUBLIC_NEW" ]; then
    cat $DUMP_FILENAME | sed -e 's/public/public_new/g' > $PUBLIC_NEW
fi

psql -v ON_ERROR_STOP=1 -U postgres -d inspection.canada.ca -c "CREATE SCHEMA IF NOT EXISTS public_new";

if [ "$?" -eq 0 ]; then
    cat $PUBLIC_NEW | psql -v ON_ERROR_STOP=1 --single-transaction -d inspection.canada.ca -U postgres
else
    echo "create schema failed"
    exit 1
fi

SCHEMA_CHANGES_PUBLIC_NEW="$SCHEMA_CHANGES.public_new.sql"
cat $SCHEMA_CHANGES | sed -e 's/public/public_new/g' > $SCHEMA_CHANGES_PUBLIC_NEW

if [ "$?" -eq 0 ]; then
    psql -v ON_ERROR_STOP=1 --single-transaction -d inspection.canada.ca -U postgres < $SCHEMA_CHANGES_PUBLIC_NEW
else
    echo "update schema failed"
    exit 1
fi