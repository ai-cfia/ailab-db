# Development guidelines for louis-db

## Making changes to the database schema

### Run latest schema locally

1. Setup .env environment variables
    * **LOUIS_DSN:** Data Source Name (DSN) used for configuring a database connection in Louis's system. It should follow this pattern, replacing each variable with your own values : 
  `LOUIS_DSN=postgresql://PGUSER:PGPASSWORD@DB_SERVER_CONTAINER_NAME/PGBASE`
    * **PGBASE:** The base directory where PostgreSQL related files or resources are stored or accessed. it can be the name of your folder followed by test (ex: louis-test).
    * **PGUSER:** The username or role required to authenticate and access a PostgreSQL database.
    * **USER:** The username required for validation and access, it can be the same as PGUSER.
    * **PGHOST:** The hostname or IP address of the server where the PostgreSQL database is hosted. If you want to use it locally, it should be `localhost`.
    * **PGPASSWORD:** The password for the user authentication when connecting to the PostgreSQL database.
    * **POSTGRES_PASSWORD:** The password for the database, for authentication when connecting to the PostgreSQL database.
    * **PGDATA:** Path to the directory where PostgreSQL data files are stored. If it's not set, it will automatically select it for you.
    * **OPENAI_API_KEY:** The API key required for authentication when making requests to the OpenAI API. It can be found [here](https://portal.azure.com/#home).
    * **OPENAI_ENDPOINT:** The link used to call into Azure OpenAI endpoints. It can be found at the same place as the OPENAI_API_KEY.
    * **OPENAI_API_ENGINE:** The name of the model deployment you want to use (ex:ailab-gpt-35-turbo).
    * **LOUIS_SCHEMA:** The Louis schema within database (ex: louis_v005).
    * **DB_SERVER_CONTAINER_NAME:** The name of your database server container (ex: louis-db-server).
    * **AILAB_SCHEMA_VERSION:** The version of the schema you want to use.
1. Run database locally (see bin/postgres.sh)
1. Restore latest schema dump

### before every change

* pgdump the schema using ```bin/backup-db-docker.sh```

### Create change

* make sure to create a Github Issue issue #X first describing the work to be done
* create a branch ```issueX-descriptive-name```
* add a new SQL file YYYY-mm-dd-issueX-descriptive-name
  * explain in top header comment the changes to be made
  * provide original DDL of files to be modified
* create a test case in tests/test_db.py
  * load your new SQL file within a transaction (that will be rolled back)
  * ensure you have an assert to test for
* once your test passes, commit change to the database by running your script with bin/psql.sh
  * you should now be able to remove the load SQL file and run the test successfully
* re-run test suite and fix exposed database functions affected by your changes (failing)
* dump the new schema as louis_v00X with X+1
* test new schema with your client apps.
