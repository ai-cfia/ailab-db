# Development guidelines for louis-db

## Making changes to the database schema

### Run latest schema locally

* Setup .env environment variables
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
