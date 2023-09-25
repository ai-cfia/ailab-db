DIRNAME=`dirname $0`
. $DIRNAME/lib.sh
if [ -z "$1" ]; then
  psql
else
  SQL_SCRIPT=$1
  $PSQL_ADMIN -f "$SQL_SCRIPT"
fi