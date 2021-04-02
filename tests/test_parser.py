from unittest import TestCase, mock
from modelgen import Parser, Base

class TestParser(TestCase):

    @classmethod
    def setUpClass(self):
        self.yaml = {'tables': {'userinfo':{'columns': 
                                        [{'name': 'firstname', 'type': 'varchar'},
                                         {'name': 'lastname', 'type': 'varchar'},
                                         {'name': 'dob', 'type': 'date'},
                                         {'name': 'contact', 'type': 'numeric'},
                                         {'name': 'address', 'type': 'varchar'}]}}}

        self.logger = Base().logger

    @mock.patch('modelgen.parser.Helper.read_yaml')
    def test_get_tables_w_columns(self, mock_ry):
        mock_ry.return_value = self.yaml
        yaml_filepath = './test.yaml'

        parser = Parser(filepath=yaml_filepath)

        assert_response = {'userinfo': {'firstname': 'varchar', 'lastname': 'varchar', 
                                        'dob': 'date', 'contact': 'numeric', 
                                        'address': 'varchar'}}

        actual_response = parser.get_tables_w_columns()

        self.assertDictEqual(assert_response, actual_response)

        mock_ry.assert_called_with(yaml_filepath)
