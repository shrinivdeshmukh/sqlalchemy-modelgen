
# sqlalchemy-modelgen

[![codecov](https://codecov.io/gh/shree14/sqlalchemy-modelgen/branch/main/graph/badge.svg?token=N0XQENE6IL)](https://codecov.io/gh/shree14/sqlalchemy-modelgen)


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
alembic revision --autogenerate -m "COMMIT_MESSAGE"
alembic upgrade head
```
<br />

**<li> Alter table support:</li>**

* Change column type, length, add contraint, etc in the yaml file. Then run:
```
modelgen createmodel --source yaml --path templates/example.yaml --alembic
alembic revision --autogenerate -m "COMMIT_MESSAGE"
alembic upgrade head
```

<ol>

## Credits

* The code that reads the structure of an existing database and generates the appropriate SQLAlchemy model code is based on [agronholm/sqlacodegen's](https://github.com/agronholm/sqlacodegen) repository (Copyright (c) Alex Grönholm), license: [MIT License](https://github.com/agronholm/sqlacodegen/blob/master/LICENSE)