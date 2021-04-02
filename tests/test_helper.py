from unittest import TestCase, mock
from modelgen import Helper

class TestHelper(TestCase):

    @classmethod
    def setUpClass(self):
        self.helper = Helper()

    def test_unpack_kwargs(self):
        '''
        Function to test the unpack_kwargs method of Helper class 
        in modelgen/helper.py file.

        Basic working of the function is, pass a dictionary object
        to the method and it returns a string with the format
        dictionary_key_1=dictionary_value_1,dictionary_key_2=dictionary_value_2
        '''
        kwargs_dict = {'key1': 'value1', 'key2': 'value2'}

        assert_response = 'key1=value1,key2=value2'

        actual_response = self.helper.unpack_kwargs(kwargs_dict)

        self.assertEqual(assert_response, actual_response)

    @mock.patch('modelgen.helper.safe_load')
    @mock.patch('builtins.open')
    def test_read_yaml(self, mock_op, mock_sl):
        yaml_filepath = './test.yaml'
        test_data = {"key1": [{"key2": "value2", "key3": "value3"}]}

        mock_sl.return_value = test_data

        with mock.patch("builtins.open", mock.mock_open(read_data='data')) as mock_file:
            mock_op.return_value = mock_file
            response = self.helper.read_yaml(yaml_filepath)
            mock_sl.assert_called_with(mock_file())
            self.assertEqual(response, test_data)

    def test_read_yaml_w_wrong_filepath(self):
        yaml_filepath = './wrong_path.yaml'
        test_data = {"key1": [{"key2": "value2", "key3": "value3"}]}

        with self.assertRaises(FileNotFoundError) as context:
            response = self.helper.read_yaml(yaml_filepath)

    @classmethod
    def tearDownClass(self):
        self.helper = None