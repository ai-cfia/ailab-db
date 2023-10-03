# Workflow

## Installing python package

If you need to interface with the database, use this to install:

```
pip install git+https://github.com/ai-cfia/louis-db@main
```

You'll often want to add, move or modify existing database layer functions found in louis-db from a client repository.

To edit, you can install an editable version of the package dependencies such as:

```
pip install -e git+https://github.com/ai-cfia/louis-db#egg=louis_db
```

this will checkout the latest source in a local git in src/louis-db allowing edits in that directory to be immediately available for use by louis-crawler.

Don't forget to create a PR with your changes once you're done!

## More documentation

* [Developer documentation](DEVELOPER.md)
* [Working with Postgresql](DB.md)