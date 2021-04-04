from unittest import TestCase, mock
from modelgen import create_model, create_alembic_meta
from os import getcwd, path

class TestModelgen(TestCase):

    @classmethod
    def setUpClass(self):
        self.yaml = {'tables': {'userinfo':{'columns': 
                                        [{'name': 'firstname', 'type': 'varchar'},
                                         {'name': 'lastname', 'type': 'varchar'},
                                         {'name': 'dob', 'type': 'date'},
                                         {'name': 'contact', 'type': 'numeric'},
                                         {'name': 'address', 'type': 'varchar'}]}}}
    
    @mock.patch('modelgen.Helper.write_to_file')
    @mock.patch('modelgen.Path')
    @mock.patch('modelgen.Parser')
    @mock.patch('modelgen.Template')
    def test_create_model(self, mock_templt, mock_prsr, mock_pth, mock_wrtf):
        mock_wrtf.return_value = True
        mock_prsr.data.return_value = self.yaml
        
        response = create_model('test')

        self.assertEqual(True, response)

        mock_prsr.assert_called_with(filepath=path.join(getcwd(), 'templates/test.yaml'))

        mock_wrtf.assert_called_with(path=path.join(getcwd(), 'models/test.py'), 
                                     data=mock_templt().render())

    @mock.patch('modelgen.Helper.write_to_file')
    @mock.patch('modelgen.Path')
    @mock.patch('modelgen.Parser')
    @mock.patch('modelgen.Template')
    def test_create_model(self, mock_templt, mock_prsr, mock_pth, mock_wrtf):
        mock_wrtf.return_value = True
        mock_prsr.data.return_value = self.yaml
        
        response = create_alembic_meta()

        self.assertEqual(True, response)

        mock_wrtf.assert_called_with(path=path.join(getcwd(), 'metadata/__init__.py'), 
                                     data=mock_templt().render())


    @classmethod
    def tearDownClass(self):
        pass