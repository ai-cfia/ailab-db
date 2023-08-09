#!/bin/bash
DIRNAME=`dirname $0`
. $DIRNAME/lib.sh

docker cp $DIRNAME/backup-db.sh louis-db-server:backup-db.sh
docker cp $DIRNAME/lib.sh louis-db-server:lib.sh
docker exec -it -e PGDUMP_FILENAME=/dev/stdout --env-file $ENV_FILE louis-db-server ./backup-db.sh > $PGDUMP_FILENAME