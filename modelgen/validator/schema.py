table_key_schema = '''
tables:
    type: dict
    required: true
    valuesrules:
        type: dict
        allow_unknown: true
'''

columns_key_schema = '''
columns:
    type: list
    valuesrules:
        type: dict
'''

columns_value_schema = '''
name:
    type: string
    required: true
type:
    type: string
    required: true
primary_key:
    type: boolean
    required: false
foreign_key:
    type: string
    required: false
length:
    type: integer
    required: false
nullable: 
    type: boolean
    required: false
unique:
    type: boolean
    required: false
'''
