
# sqlalchemy-modelgen

[![codecov](https://codecov.io/gh/shrinivdeshmukh/sqlalchemy-modelgen/branch/main/graph/badge.svg?token=N0XQENE6IL)](https://codecov.io/gh/shrinivdeshmukh/sqlalchemy-modelgen)
[![PyPI](https://img.shields.io/pypi/v/alchemy-modelgen)](https://pypi.org/project/alchemy-modelgen/)


Create sqlalchemy python model files by defining tables and columns in a yaml file or by specifying database url

# Installation

```
pip install alchemy-modelgen
```

# Usage

<ol>

**<li> Initialize modelgen folder:</li>**

```
modelgen init -d /path/to/YOUR_FOLDER
cd /path/to/YOUR_FOLDER
```
<br />

**<li> Create sqlalchemy model code from: </li>** 
 
 **(Option 1)** `yaml` template:

**For details on how to write the yaml file, please follow [docs](https://github.com/shree14/sqlalchemy-modelgen/blob/main/docs/yaml_creation.md)**
```
modelgen createmodel --source yaml --path templates/example.yaml --alembic # path to your schema yaml file 
```
   **(Option 2)** existing `database`: 
```
modelgen createmodel --source database --path mysql+mysqlconnector://root:example@localhost:3306/modelgen --outfile models/YOUR_FILENAME.py --alembic
```
<br />

**<li> Running alembic migrations:</li>**

```
modelgen migrate revision --autogenerate -m "COMMIT_MESSAGE" -p mysql+mysqlconnector://root:example@localhost:3306/modelgen

modelgen migrate upgrade head -p mysql+mysqlconnector://root:example@localhost:3306/modelgen
```

The arguments passed after `modelgen migrate` are based on alembic. Any command true for `alembic` can be used with `modelgen migrate`.

**The database url can be passed using `-p` or `--path` argument, or can be set in the environment by the env var `DATABASE_URI`. If `DATABASE_URI` is set, `-p` or `--path` will be ignored**

<br />

**<li> Alter table support:</li>**

* Change column type, length, add contraint, etc in the yaml file. Then run:
```
modelgen createmodel --source yaml --path templates/example.yaml --alembic
modelgen migrate revision --autogenerate -m "COMMIT_MESSAGE" -p mysql+mysqlconnector://root:example@localhost:3306/modelgen

modelgen migrate upgrade head -p mysql+mysqlconnector://root:example@localhost:3306/modelgen
```

<ol>

## Credits

* The code that reads the structure of an existing database and generates the appropriate SQLAlchemy model code is based on [agronholm/sqlacodegen's](https://github.com/agronholm/sqlacodegen) repository (Copyright (c) Alex Grönholm), license: [MIT License](https://github.com/agronholm/sqlacodegen/blob/master/LICENSE)
