#!/bin/bash
DIRNAME=$(dirname "$0")
. $DIRNAME/lib.sh

check_environment_variables_defined PGBASE DB_SERVER_CONTAINER_NAME PSQL_ADMIN

# set -x -e  
DOCKER_EXEC="docker exec -it $DB_SERVER_CONTAINER_NAME"  

## Check if user already exist  
$DOCKER_EXEC psql -U postgres -c "    
DO    
\$do\$    
BEGIN    
   IF NOT EXISTS (    
      SELECT FROM pg_roles WHERE rolname = '$USER'  
   ) THEN  
      CREATE USER $USER WITH PASSWORD '$PGPASSWORD';    
      ALTER USER $USER WITH SUPERUSER;    
   END IF;    
END    
\$do\$;"

## Print all existing users
# $DOCKER_EXEC psql -U postgres -c '\du'  

## Check if database already exist  
DB_EXISTS=$($DOCKER_EXEC psql -U "$USER" -d "$PGBASE" -tAc "SELECT 1 FROM pg_database WHERE datname='$PGBASE'" | tr -d '\r')  

if [ "$DB_EXISTS" = '1' ]  
then  
    echo "Database $PGBASE already exists."  
else  
    echo "Database $PGBASE does not exist, creating..."  
    $DOCKER_EXEC createdb -E utf-8 -U postgres "$PGBASE"
fi

## Print all existing databases
# $DOCKER_EXEC psql -U postgres -c '\l'

$DOCKER_EXEC pip install pgxnclient

VECTOR_INSTALLED=$(docker exec -u 0 -i "$DB_SERVER_CONTAINER_NAME" psql -U postgres -tAc "SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'vector');")  
  
if [ "$VECTOR_INSTALLED" = "t" ]  
then  
    echo "Extension vector is already installed."  
else  
    echo "Extension vector is not installed. Installing..."  
    docker exec -u 0 -it "$DB_SERVER_CONTAINER_NAME" pgxn install vector  
fi  

$DOCKER_EXEC psql -U postgres -v ON_ERROR_STOP=1 --single-transaction -d inspection -c 'SET search_path TO public; CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; CREATE EXTENSION IF NOT EXISTS vector;'

# $DOCKER_EXEC $PSQL_ADMIN -c "SET search_path TO public; CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"; CREATE EXTENSION IF NOT EXISTS vector;"
# User creation
# $DOCKER_EXEC $PSQL_ADMIN -c "CREATE USER $USER; ALTER USER $USER WITH SUPERUSER;"