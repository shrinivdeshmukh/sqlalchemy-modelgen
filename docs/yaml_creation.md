# This document gives a high level idea of how to write the yaml schema file

## Structure

```
tables: # In this section, we define the tables, their name and schema
    userinfo: # This is the table name
        columns: # In this section, we define column names and their data types
            - name: firstname # Column name
              type: varchar # Column datatype
            - name: lastname
              type: varchar
            - name: dob
              type: date
            - name: contact
              type: numeric
            - name: address
              type: varchar
              length: 200 # specify length of the column
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
            - name: redshift_distkey # Name of the parameter
              value: userid # Value of the parameter
```