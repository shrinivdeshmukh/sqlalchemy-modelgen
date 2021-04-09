
# sqlalchemy-modelgen

[![codecov](https://codecov.io/gh/shree14/sqlalchemy-modelgen/branch/main/graph/badge.svg?token=N0XQENE6IL)](https://codecov.io/gh/shree14/sqlalchemy-modelgen)


Create sqlalchemy python model files by defining tables and columns in a yaml file

# Run example

<b> Clone this repository:</b>
```
 git clone git@github.com:shree14/sqlalchemy-modelgen.git
 cd sqlalchemy-modelgen
```
<b> Start MySQL and Adminer:</b>
```
docker-compose up -d
```
<b> Create python virtual environment and install required packages (python version >= 3.8.8):</b>
  ##### Option 1: Using conda:
  ```
  conda create -n <your-env> python=3.8.8 -y
  conda activate <your-env>
  pip install -r requirements.txt
  ``` 
  <b> OR </b>
  ##### Option 2: Using virtualenv:
  
  ```
  pip install virtualenv
  virtualenv <your-env>
  source <your-env>/bin/activate
  <your-env>/bin/pip install -r requirements.txt
  ```
<b> Open python shell:</b>
```
# from your terminal:
python
>>> from modelgen import create_model
>>> create_model('userinfo', alembic=True) 
```
<b> Run `alembic` migrations:</b>
```
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```
<b>Go to http://localhost:8080 and login with username: root and password: example</b> <br />
* The first screen will look like this:
  <img src='docs/images/list_databases.png' height=75% width=75% /> <br />
* In the above screen, click `modelgen`. The next screen will look like this: <br />
  <img src='docs/images/list_tables.png' height=75% width=75% /> <br />
* Click any of the two tables `(userinfo, orders)` to view their schema <br />

  

# Installation

`python version 3.8.8 used here`

### The `docker-compose.yaml` can be used to test out the code with mysql database

1. Create a python virtual environment using `virtualenv` or `conda environment`

2. Run `pip install -r requirements.txt`

# Define the schema in a yaml file

For details on how to write the yaml file, please follow [docs](docs/yaml_creation.md)

1. Create a yaml file with your datasource as it's name with extension `.yaml` in the `templates` folder.
Ex: we create a file `userinfo.yaml` in the `templates` folder. Here `userinfo` is considered as the datasource
```
tables:
  userinfo:
    columns:
      - name: firstname
        type: varchar

      - name: lastname
        type: varchar

      - name: dob
        type: date

      - name: contact
        type: numeric

      - name: address
        type: varchar
```

2. Open python3 shell in your terminal and write the following lines:
```
>>>from modelgen import create_model
>>>
>>>create_model('userinfo')
True
```

3. A folder named `models` will be created in the `modelgen` folder. In the `models` folder, a file by the name `datasource.py` (or `userinfo.py` in this case) will be created that'll look something like this:

```
from sqlalchemy import String, Integer, Boolean, Float, Numeric, DateTime, Date, Table, Column
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()

metadata = DeclarativeBase.metadata


    
userinfo = Table('userinfo', 
             metadata,
             Column('firstname', String),             
             Column('lastname', String),             
             Column('dob', Date),             
             Column('contact', Numeric),             
             Column('address', String),                                       
           )
```

# Alembic Support

#### Start MySQL server:
```
docker-compose up -d
```
wait for few seconds. <br />
Go to http://localhost:8080 to view the adminer UI. To access the mysql database and the adminer UI ,the username is `root` and password is `example` 

To enable alembic support:

##### 1. Add sqlalchemy database url: <br />
 <b> Option 1:</b> Add your sqlalchemy(database) url at `line 42` in `alembic.ini` file. <br /> 
The line should look something like this:<br /> `sqlalchemy.url = dialect+driver://username:password@host:port/database` <br /><br />
ex: In the `alembic.ini` of this repo, line 42 is <br /><br />
`sqlalchemy.url = mysql+mysqlconnector://root:example@localhost:3306/modelgen`
  ###### OR
 <b>Option 2:</b> Create a file `.env` in the main folder of the repository and add the following variable:
  `DATABASE_URI=dialect+driver://username:password@host:port/database`<br /><br />
  ex: For MySQL specified in the `docker-compose.yaml`, the above variable will be <br />`DATABASE_URI=mysql+mysqlconnector://root:example@localhost:3306/modelgen` <br />
  ###### OR
 <b>Option 3:</b> In your terminal, execute the following command:<br />
  `export DATABASE_URI=dialect+driver://username:password@host:port/database`<br /><br />
  ex: `export DATABASE_URI=mysql+mysqlconnector://root:example@localhost:3306/modelgen` <br />

##### 2. Run model generation code and set `alembic=True`
  ```
  >>>from modelgen import create_model
  >>>
  >>>create_model('userinfo', alembic=True)
  True
  ```

##### 3. Run alembic revision and upgrade:
  ```
  alembic revision --autogenerate -m 'YOUR MESSAGE'
  alembic upgrade head 
  ```
