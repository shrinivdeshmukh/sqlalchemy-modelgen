from yaml import safe_load
from cerberus import Validator
from typing import Union
from modelgen.validator.schema import (table_key_schema, 
                                       columns_key_schema, 
                                       columns_value_schema
                                       )
from modelgen import Helper

class Validate(Helper):

    def __init__(self, filepath: str):
        Helper.__init__(self)
        self._doc = self.read_yaml(filepath)
        self.validator = Validator()

    def _validate_table(self):
        self.validator.validate(self._doc, safe_load(table_key_schema))
        if self.validator.errors:
            raise ValidationError('', self.validator.errors)

    def _validate_column(self):
        err_dict = dict()
        for table_name, table_data in self._doc['tables'].items():
            err_list = list()
            for i in table_data:
                self.validator.validate(table_data, safe_load(columns_key_schema))
                if bool(self.validator.errors):
                    err_list.append(self.validator.errors)
            if bool(err_list):
                err_dict.update({table_name: err_list})
        if err_dict:
            raise ValidationError('Invalid column schema', err_dict)

    def _validate_column_meta(self):
        err_dict = dict()
        for table_name, table_data in self._doc['tables'].items():
            err_list = list()
            for i in table_data['columns']:
                self.validator.validate(i, safe_load(columns_value_schema))
                if bool(self.validator.errors):
                    err_list.append(self.validator.errors)
            if bool(err_list):
                err_dict.update({table_name: err_list})
        if err_dict:
            raise ValidationError('Invalid column information', err_dict)

    def validate(self):
        self._validate_table()
        self._validate_column()
        self._validate_column_meta()
        return True

class ValidationError(ValueError):
    def __init__(self, message, errors):
        err_str = str()
        if isinstance(errors, dict):
            for table_name, error in errors.items():
                err_str += f'\nkey = {table_name},  error = {error}'
        message = f'{message} {err_str}'
        super().__init__(message)