# What is ailab-db ?

Ailab-db contains the database of [Louis](https://github.com/ai-cfia/louis),
[Nachet](https://github.com/ai-cfia/nachet-backend) and any other product of the
CFIA's AI Lab. It includes all of the python and bash scripts as well as sql
functions. It uses ada-002 API (Application Programming Interface) for semantic
search. Ada is a model that vectorises text to make a semantic representation
out of it. It follows this process : 
> Taking the text, passing it through the model, putting it in an embedding
> table that will work like an index.

- The *bin* folder : This folder contains all of the bash scripts that would be
  useful for the backends or to set up the database.

- The *ailab* folder : This folder is a python module structure that allows
  connections to the database or the api as well as containing useful functions
  for product backends.

- The *postgres* folder : This folder contains the bash script that will set up
  the docker container.

- The *sql* folder : This folder holds all of the sql functions and scripts.

- The *tests* folder : This is the test folder, it allows you to test the code.

Here is the database schema : ![database schema](img/database-schema.png)

If you need to set up the database locally, please follow [this
procedure](setup-procedure.md).

---

# Workflow

## Installing python package

If you need to interface with the database, use this to install:

```
pip install git+https://github.com/ai-cfia/ailab-db@v0.0.5-alpha3
```

You'll often want to add, move or modify existing database layer functions found
in ailab-db from a client repository.

To edit, you can install an editable version of the package dependencies such
as:

```
pip install -e git+https://github.com/ai-cfia/louis-db#egg=louis_db
```

this will checkout the latest source in a local git in src/louis-db allowing
edits in that directory to be immediately available for use by louis-crawler.

Don't forget to create a PR with your changes once you're done!
