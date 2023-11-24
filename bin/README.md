# creating a new schema

## environment

This assumes:

* you are running WSL
* you are running a dockerized version of Postgresql 15 under WSL
* you are running ailab-db in a DevContainer under Visual Studio Code
* your source is on WSL under ~/src

## configuration

database connection parameters is set in .env file

you can create multiple .env.NAME and symlink as needed:

working on local source:

```
ln -sf .env.louis_v004_local .env
```

switching to target

```
ln -sf .env.louis_v005_azure .env
```

## Running the database server locally

* use Dockerfile in postgres directory
* use ```bin/postgres.sh``` script as your startup script (symlink)

## Editing

* Create adhoc modifications as scripts in sql/ with proper YYYY-mm-dd prefix
* Create tests that apply these sql scripts in a transaction and test them
* Once satisfied, commit changes to database



## backing up schema and data

in this example, the modified louis_v004 becomes the louis_v005 schema:

```
./bin/dump-versioned-schema.sh louis_v004 louis_v005
./bin/dump-versioned-data.sh louis_v004 louis_v005
```

## loading schema

change your .env to link to your target database first

```
./bin/load-versioned-schema.sh louis_v005
```

validate manually that schema is as expected here (dbBeaver ERD diagram) before loading the data:

```
./bin/load-versioned-data.sh louis_v005
```
