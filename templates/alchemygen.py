alchemygen = '''from sqlalchemy import String, Integer, Boolean, Float, Numeric, DateTime, Date, Table, Column
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()

metadata = DeclarativeBase.metadata\

{% for table, schema in yaml_data[cst.key_tables].items() %}
{% if not bool(schema.get(cst.key_columns)) %}
    {% set column_data = yaml_data[cst.key_tables][schema.get(cst.inherit_from)][cst.key_columns] %}
{% else %}
    {% set column_data = schema.get(cst.key_columns) %}
{% endif %}\
{{ table }} = Table('{{ table }}', 
             metadata,{% for col in column_data %}
             Column('{{ col[cst.key_column_name] }}', {{ cst.sqlalchemy_python_types[col[cst.key_column_type]] }}),\
             {% endfor %}\
             {% if bool(schema.get(cst.key_extra_params)) %}              
                {% for params in schema.get(cst.key_extra_params) %}
             {{ params[cst.key_extra_params_name] }}={{ params[cst.key_extra_params_value] }},\
                {% endfor %}
            {% endif %}             
           )
{% endfor %}
'''