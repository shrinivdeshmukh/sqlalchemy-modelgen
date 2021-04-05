alchemygen = '''from sqlalchemy import String, Integer, Boolean, Float, Numeric, DateTime, Date, Table, Column, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()

{{ datasource }}_metadata = DeclarativeBase.metadata\

{% for table, schema in yaml_data[cst.key_tables].items() %}
{% if not bool(schema.get(cst.key_columns)) -%}
    {% set column_data = yaml_data[cst.key_tables][schema.get(cst.inherit_from)][cst.key_columns] %}
{% else -%}
    {% set column_data = schema.get(cst.key_columns) %}
{%- endif %}
{{ table }} = Table('{{ table }}', 
            {{ datasource }}_metadata,{%- for col in column_data -%}
            {%- if bool(col.get(cst.key_column_length)) -%}
                {% set length = col.get(cst.key_column_length) %}
            {%- endif %}
            {% if bool(col.get(cst.key_primary_key)) -%}
                Column('{{ col[cst.key_column_name] }}', {{ cst.sqlalchemy_python_types[col[cst.key_column_type]] }}({{ length }}), primary_key=True),
            {% else -%}
                Column('{{ col[cst.key_column_name] }}', {{ cst.sqlalchemy_python_types[col[cst.key_column_type]] }}({{ length }})),
            {%- endif %}
            {%- endfor %}
            {% if bool(schema.get(cst.key_extra_params)) -%}              
                {% for params in schema.get(cst.key_extra_params) -%}
            {{ params[cst.key_extra_params_name] }}={{ params[cst.key_extra_params_value] }},\
                {%- endfor %}
            {%- endif %}             
        )
{% endfor %}
'''

metagen = '''{% set import_list = [] %}\
{% for file in filenames %}\
{% set meta_obj = splitext(file)[0]+'_metadata' %}\
from models.{{ splitext(file)[0] }} import {{ meta_obj }}\
{{ import_list.append(meta_obj)|default("", True)  }}
{% endfor %}
metadata = [{{ import_list|join(',') }}]
'''