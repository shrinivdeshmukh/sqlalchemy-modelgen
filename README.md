# sqlalchemy-modelgen
Create sqlalchemy python model files by defining tables and columns in a yaml file

# Installation

`python version 3.8.8 used here`

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

3. A folder named `models` will be created. In the folder, a file by the name `datasource.py` (or `userinfo.py` in this case) will be created that'll look something like this:

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
