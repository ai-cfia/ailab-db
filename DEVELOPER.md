# Development guidelines for louis-db

## Making changes to the database schema

### Run latest schema locally

* Setup .env environment variables
  * LOUIS_DSN: Data Source Name (DSN) used for configuring a database connection in Louis's system.

  * PGBASE: the base directory where PostgreSQL related files or resources are stored or accessed.

  * PGUSER: the username or role required to authenticate and access a PostgreSQL database.

  * USER: the username required for validation and access

  * PGHOST: the hostname or IP address of the server where the PostgreSQL database is hosted.

  * PGPASSWORD: the password for the user authentication when connecting to the PostgreSQL database.

  * POSTGRES_PASSWORD: the password for the database, for authentication when connecting to the PostgreSQL database.

  * PGDATA: path to the directory where PostgreSQL data files are stored.

  * OPENAI_API_KEY: the API key required for authentication when making requests to the OpenAI API.

  * AZURE_OPENAI_SERVICE: information related to an Azure-based service for OpenAI.

  * LOUIS_SCHEMA: the Louis schema within database.

  * DB_SERVER_CONTAINER_NAME: name of your database server container.

* Run database locally (see bin/postgres.sh)
* Restore latest schema dump

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
