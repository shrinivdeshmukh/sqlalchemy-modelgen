from unittest import TestCase, mock
from cerberus import Validator

from modelgen.validator import Validate, ValidationError
from modelgen.validator.schema import (table_key_schema, 
                                       columns_key_schema, 
                                       columns_value_schema)

class TestValidator(TestCase):

    @classmethod
    def setUpClass(self):
        self.yaml_data = {'tables': {'example_user_table': {'columns': [{'name': 'id',
                            'type': 'integer',
                            'primary_key': True},
                            {'name': 'firstname', 'type': 'varchar', 'length': 50, 
                             'nullable': False},
                            {'name': 'lastname', 'type': 'varchar', 'length': 50}]},
                        'example_meta_table': {'columns': [{'name': 'meta_id',
                            'type': 'integer',
                            'foreign_key': 'example_user_table.id'},
                            {'name': 'address', 'type': 'varchar', 'length': 250},
                            {'name': 'contact', 'type': 'numeric', 'unique': True}]}}}

        self.incorrect_table_yaml_data = {'tabel': {'example_user_table': {'columns': [{'name': 'id',
                            'type': 'integer',
                            'primary_key': True},
                            {'name': 'firstname', 'type': 'varchar', 'length': 50, 
                             'nullable': False},
                            {'name': 'lastname', 'type': 'varchar', 'length': 50}]},
                        'example_meta_table': {'columns': [{'name': 'meta_id',
                            'type': 'integer',
                            'foreign_key': 'example_user_table.id'},
                            {'name': 'address', 'type': 'varchar', 'length': 250},
                            {'name': 'contact', 'type': 'numeric', 'unique': True}]}}}

        self.incorrect_column_yaml_data = {'tables': {'example_user_table': {'wrong_column_key': [{'name': 'id',
                            'type': 'integer',
                            'primary_key': True},
                            {'name': 'firstname', 'type': 'varchar', 'length': 50, 
                             'nullable': False},
                            {'name': 'lastname', 'type': 'varchar', 'length': 50}]},
                        'example_meta_table': {'columns': [{'name': 'meta_id',
                            'type': 'integer',
                            'foreign_key': 'example_user_table.id'},
                            {'name': 'address', 'type': 'varchar', 'length': 250},
                            {'name': 'contact', 'type': 'numeric', 'unique': True}]}}}

        self.incorrect_column_meta_data = {'tables': {'example_user_table': {'columns': [{'name': 'id',
                            'type': 'integer',
                            'primary_key': 55}, # Integer instead of boolean,
                            {'name': 'firstname', 'type': 'varchar', 'length': 50, 
                             'nullable': False},
                            {'name': 'lastname', 'type': 'varchar', 'length': 'string_instead_of_integer'}]},
                        'example_meta_table': {'columns': [{'name': 'meta_id',
                            'type': 'integer',
                            'foreign_key': 'example_user_table.id'},
                            {'name': 'address', 'type': 'varchar', 'length': 250},
                            {'name': 'contact', 'type': 'numeric', 'unique': 'random_false_string'}]}}}

    @mock.patch('modelgen.validator.Helper.read_yaml')
    def test_validate_table_w_correct_schema(self, mock_rdyml):
        mock_rdyml.return_value = self.yaml_data
        obj = Validate('./modelgen/templates/example.yaml')
        obj._doc = self.yaml_data
        validate_table_response = obj._validate_table()
        self.assertEqual(validate_table_response, None)

    @mock.patch('modelgen.validator.Helper.read_yaml')
    def test_validate_column_w_correct_schema(self, mock_rdyml):
        mock_rdyml.return_value = self.yaml_data
        obj = Validate('./modelgen/templates/example.yaml')
        obj._doc = self.yaml_data
        validate_column_response = obj._validate_column()
        self.assertEqual(validate_column_response, None)

    @mock.patch('modelgen.validator.Helper.read_yaml')
    def test_validate_column_meta_w_correct_schema(self, mock_rdyml):
        mock_rdyml.return_value = self.yaml_data
        obj = Validate('./modelgen/templates/example.yaml')
        obj._doc = self.yaml_data
        validate_col_meta_response = obj._validate_column_meta()
        self.assertEqual(validate_col_meta_response, None)

    @mock.patch('modelgen.validator.Helper.read_yaml')
    def test_validate_table_w_incorrect_schema(self, mock_rdyml):
        mock_rdyml.return_value = self.incorrect_table_yaml_data
        obj = Validate('./modelgen/templates/example.yaml')
        obj._doc = self.incorrect_table_yaml_data
        with self.assertRaises(ValidationError) as err:
            validate_table_response = obj._validate_table()

    @mock.patch('modelgen.validator.Helper.read_yaml')
    def test_validate_column_w_incorrect_schema(self, mock_rdyml):
        mock_rdyml.return_value = self.incorrect_table_yaml_data
        obj = Validate('./modelgen/templates/example.yaml')
        obj._doc = self.incorrect_column_yaml_data
        with self.assertRaises(ValidationError) as err:
            validate_table_response = obj._validate_column()

    @mock.patch('modelgen.validator.Helper.read_yaml')
    def test_validate_column_meta_w_incorrect_schema(self, mock_rdyml):
        mock_rdyml.return_value = self.incorrect_column_meta_data
        obj = Validate('./modelgen/templates/example.yaml')
        obj._doc = self.incorrect_column_meta_data
        with self.assertRaises(ValidationError) as err:
            validate_table_response = obj._validate_column_meta()

    @mock.patch('modelgen.validator.Validate._validate_table')
    @mock.patch('modelgen.validator.Validate._validate_column')
    @mock.patch('modelgen.validator.Validate._validate_column_meta')
    @mock.patch('modelgen.validator.Helper.read_yaml')
    def test_validate(self, mock_rdyml, mock_vtbl, mock_vclm, mock_vclm_meta):
        mock_rdyml.return_value = self.incorrect_column_meta_data
        mock_vtbl.return_value = None
        mock_vclm.return_value = None
        mock_vclm_meta.return_value = None
        obj = Validate('./modelgen/templates/example.yaml')
        obj._doc = self.incorrect_column_meta_data
        validate_table_response = obj.validate()
        mock_rdyml.assert_called_with('./modelgen/templates/example.yaml')
    @classmethod
    def tearDownClass(self):
        pass