# sqlalchemy-modelgen

Create sqlalchemy python model files by defining tables and columns in a yaml file

# Installation

```
pip install alchemy-modelgen
```

# Usage

1. Initialize alchemy-modelgen folder

```
modelgen --init FOLDER_NAME
```

2. Create schema template
# This document gives a high level idea of how to write the yaml schema file

## Structure

```
tables: # In this section, we define the tables, their name and schema
    userinfo: # This is the table name
        columns: # In this section, we define column names and their data types
            - name: id
              type: integer
              primary_key: true     # Set this value for the primary key column
            - name: firstname       # Column name
              type: varchar         # Column datatype
            - name: lastname
              type: varchar
            - name: dob
              type: date
            - name: contact
              type: numeric
              nullable: false/true      # Allow / disallow null values in the column, default `true`
              unique: true/false        # Apply unique constraint for the column, default `false`
            - name: address
              type: varchar
              length: 200       # specify length of the column
```

## Injecting extra parameters

It is possible to inject database dialect parameters. For example, for [redshift](https://aws.amazon.com/redshift/) we can specify `redshift_diststyle` or `redshift_distkey` or any other feature supported by redshift.

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
        extra_params: # Here we can specify dialect specific extra parameters
            - name: redshift_distkey        # Name of the parameter
              value: userid                 # Value of the parameter
```

3. Run model generation code

```
modelgen -c path/to/yaml_schema.yaml -a
```

4. Run alembic migrations

```
alembic revision --autogenerate -m "YOUR_COMMIT_MESSAGE"
alembic upgrade head
```

# Alter Table support

* To alter any column's schema, make the relevant changes in the YAML template file.

* Run the model generation code

```
modelgen -c path/to/yaml_schema.yaml -a
```

* Run alembic migrations

```
alembic revision --autogenerate -m "YOUR_COMMIT_MESSAGE"
alembic upgrade head
```
