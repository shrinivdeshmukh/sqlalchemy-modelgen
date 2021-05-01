alchemygen = '''from sqlalchemy import (String, Integer, Boolean, Float, 
                                Numeric, DateTime, Date, Table, Column, 
                                PrimaryKeyConstraint, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()

metadata = DeclarativeBase.metadata\

{% for table, schema in yaml_data[cst.key_tables].items() %}
{% if not bool(schema.get(cst.key_columns)) -%}
    {% set column_data = yaml_data[cst.key_tables][schema.get(cst.inherit_from)][cst.key_columns] %}
{% else -%}
    {% set column_data = schema.get(cst.key_columns) %}
{%- endif %}
{{ table }} = Table('{{ table }}', 
            metadata,{%- for col in column_data -%}
            {%- if bool(col.get(cst.key_column_length)) -%}
                {% set length = col.get(cst.key_column_length) %}
            {%- endif %}
            Column('{{ col[cst.key_column_name] }}'
                    {%- if bool(col.get(cst.key_column_length)) -%}
                        ,{{ cst.sqlalchemy_python_types[col[cst.key_column_type]] }}({{ col.get(cst.key_column_length) }})
                    {%- else -%}
                        ,{{ cst.sqlalchemy_python_types[col[cst.key_column_type]] }}
                    {%- endif %}
                    {%- if bool(col.get(cst.key_foreign_key)) -%}
                        ,ForeignKey('{{ col.get(cst.key_foreign_key) }}')
                    {%- endif %}
                    {%- if cst.key_primary_key in col -%}
                        ,primary_key={{ col.get(cst.key_primary_key) }}
                    {%- endif %}
                    {%- if cst.key_unique in col -%}
                        ,unique={{ col.get(cst.key_unique) }}
                    {%- endif %}
                    {%- if cst.key_nullable in col -%}
                        ,nullable={{ col.get(cst.key_nullable) }}
                    {%- endif %}),
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
from models.{{ splitext(file)[0] }} import metadata as {{ meta_obj }}\
{{ import_list.append(meta_obj)|default("", True)  }}
{% endfor %}
metadata = [{{ import_list|join(', ') }}]
'''