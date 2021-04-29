from unittest import TestCase, mock
from modelgen import ModelGenerator, Base
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
    
        self.logger = Base().logger

    @mock.patch('modelgen.modelgenerator.Validate')
    @mock.patch('modelgen.ModelGenerator.__init__')
    @mock.patch('modelgen.modelgenerator.Helper.write_to_file')
    @mock.patch('modelgen.modelgenerator.Path')
    @mock.patch('modelgen.modelgenerator.Parser')
    @mock.patch('modelgen.modelgenerator.Template')
    def test_create_model_wo_alembic(self, mock_templt, mock_prsr, mock_pth, 
                          mock_wrtf, mock_init, mock_validate):
        mock_init.return_value = None
        mock_validate.validate.return_value = True
        mock_wrtf.return_value = True
        mock_prsr.data.return_value = self.yaml

        model_obj = ModelGenerator()

        response = model_obj._create_model('test')

        self.assertEqual(True, response)

        mock_prsr.assert_called_with(filepath=path.join(getcwd(), 'templates/test.yaml'))

        mock_wrtf.assert_called_with(path=path.join(getcwd(), 'models/test.py'), 
                                     data=mock_templt().render())

    @mock.patch('modelgen.modelgenerator.ModelGenerator._create_alembic_meta')
    @mock.patch('modelgen.modelgenerator.Validate')
    @mock.patch('modelgen.ModelGenerator.__init__')
    @mock.patch('modelgen.modelgenerator.Helper.write_to_file')
    @mock.patch('modelgen.modelgenerator.Path')
    @mock.patch('modelgen.modelgenerator.Parser')
    @mock.patch('modelgen.modelgenerator.Template')
    def test_create_model_w_alembic(self, mock_templt, mock_prsr, mock_pth, 
                          mock_wrtf, mock_init, mock_validate, mock_cam):
        mock_init.return_value = None
        mock_validate.validate.return_value = True
        mock_wrtf.return_value = True
        mock_prsr.data.return_value = self.yaml
        mock_cam.return_value = True

        model_obj = ModelGenerator()

        response = model_obj._create_model(datasource='./test', alembic=True)

        self.assertEqual(True, response)

        mock_prsr.assert_called_with(filepath=path.join(getcwd(), 'templates/./test.yaml'))

        mock_wrtf.assert_called_with(path=path.join(getcwd(), 'models/./test.py'), 
                                     data=mock_templt().render())

    @mock.patch('modelgen.modelgenerator.Validate')
    @mock.patch('modelgen.ModelGenerator.__init__')
    @mock.patch('modelgen.modelgenerator.Helper.write_to_file')
    @mock.patch('modelgen.modelgenerator.Path')
    @mock.patch('modelgen.modelgenerator.Parser')
    @mock.patch('modelgen.modelgenerator.Template')
    def test_create_alembic_meta(self, mock_templt, mock_prsr, mock_pth, 
                          mock_wrtf, mock_init, mock_validate):
        mock_init.return_value = None
        mock_validate.validate.return_value = True
        mock_wrtf.return_value = True
        mock_prsr.data.return_value = self.yaml
        
        model_obj = ModelGenerator()
        response = model_obj._create_alembic_meta()

        self.assertEqual(True, response)

        mock_wrtf.assert_called_with(path=path.join(getcwd(), 'metadata/__init__.py'), 
                                     data=mock_templt().render())
    
    @mock.patch('modelgen.modelgenerator.path')
    @mock.patch('modelgen.modelgenerator.Path')
    @mock.patch('modelgen.modelgenerator.copyfile')
    def test_create_template_folder(self, mock_cpyfile, mock_pth, mock_ospth):
        mock_ospth.join.side_effects = ['./test', './test', './test', './test']
        mock_ospth.exists.return_value = False
        mock_pth.mkdir.return_value = True
        mock_cpyfile.return_value = True
        model_obj = ModelGenerator()
        response = model_obj._create_template_folder(init='./testfolder')
        self.assertEqual(response, True)
        mock_cpyfile.assert_called_with(mock_ospth.join(), mock_ospth.join())

    @mock.patch('modelgen.ModelGenerator._create_alembic_folder')
    @mock.patch('modelgen.modelgenerator.Path')
    @mock.patch('modelgen.modelgenerator.path')
    @mock.patch('modelgen.modelgenerator.copyfile')
    def test_create_template_folder_exists(self, mock_cpyfile, mock_ospth, mock_pth, mock_caf):
        mock_pth.mkdir.return_value = FileExistsError
        mock_caf.return_value = True
        mock_ospth.join.side_effects = ['./test', './test', './test', './test']
        mock_ospth.exists.return_value = True
        mock_cpyfile.return_value = True
        model_obj = ModelGenerator()
        with self.assertRaises(FileExistsError) as err:
            model_obj._create_template_folder(init='./models')

    @mock.patch('modelgen.modelgenerator.copytree')
    @mock.patch('modelgen.modelgenerator.path')
    @mock.patch('modelgen.modelgenerator.Path')
    @mock.patch('modelgen.modelgenerator.copyfile')
    def test_create_alembic_folder(self, mock_cpyfile, mock_pth, mock_ospth, 
                                   mock_cptr):
        mock_cptr.return_value = True
        mock_ospth.join.return_value = './testfolder'
        mock_ospth.isabs.return_value = False
        mock_ospth.exists.return_value = False
        mock_pth.mkdir.return_value = True
        mock_cpyfile.return_value = True
        model_obj = ModelGenerator()
        response = model_obj._create_alembic_folder(init='./testfolder')
        self.assertEqual(response, True)
        mock_cptr.assert_called_with(mock_ospth.join(), mock_ospth.join())

    @mock.patch('modelgen.modelgenerator.copytree')
    @mock.patch('modelgen.modelgenerator.path')
    @mock.patch('modelgen.modelgenerator.Path')
    @mock.patch('modelgen.modelgenerator.copyfile')
    def test_create_alembic_folder_absolute_path(self, mock_cpyfile, mock_pth, mock_ospth, 
                                   mock_cptr):
        mock_cptr.return_value = True
        mock_ospth.join.return_value = '/testfolder'
        mock_ospth.exists.return_value = False
        mock_pth.mkdir.return_value = True
        mock_cpyfile.return_value = True
        model_obj = ModelGenerator()
        response = model_obj._create_alembic_folder(init='/testfolder')
        self.assertEqual(response, True)
        mock_cptr.assert_called_with(mock_ospth.join(), mock_ospth.join())

    @mock.patch('modelgen.ModelGenerator._create_template_folder')
    @mock.patch('modelgen.modelgenerator.path')
    @mock.patch('modelgen.modelgenerator.copytree')
    @mock.patch('modelgen.modelgenerator.copyfile')
    def test_create_alembic_folder_exists(self, mock_cpyfile, mock_cptr, mock_ospth, mock_ctf):
        mock_ctf.return_value = True
        mock_cptr.return_value = True
        mock_ospth.join.side_effects = ['./test', './test', './test', './test']
        mock_ospth.exists.return_value = True
        mock_cpyfile.return_value = True
        model_obj = ModelGenerator()
        with self.assertRaises(FileExistsError) as err:
            model_obj._create_alembic_folder(init='./docs')

    @mock.patch('modelgen.modelgenerator.ModelGenerator._create_alembic_folder')
    @mock.patch('modelgen.modelgenerator.ModelGenerator._create_template_folder')
    @mock.patch('modelgen.modelgenerator.ModelGenerator._create_checkpoint_file')
    def test_modelgenerator_init(self, mock_cafldr, mock_ctfldr, mock_cchk):
        obj = ModelGenerator(init='./test')
        mock_cafldr.assert_called_with(init='./test')
        mock_cchk.assert_called_with(init='./test')
        mock_ctfldr.assert_called_with(init='./test')

    @mock.patch('modelgen.modelgenerator.path')
    @mock.patch('modelgen.modelgenerator.ModelGenerator._create_model')
    @mock.patch('modelgen.modelgenerator.ModelGenerator._find_checkpoint_file')
    def test_modelgenerator_init_create_model_elif_w_yaml_extn(self, mock_fcf, 
                                                                 mock_cm, mock_ospth):
        mock_ospth.return_value = True
        mock_cm.return_value = True
        mock_fcf = True
        obj = ModelGenerator(createmodel=True, file='./test.yaml')

    @mock.patch('modelgen.modelgenerator.path')
    @mock.patch('modelgen.modelgenerator.ModelGenerator._create_model')
    @mock.patch('modelgen.modelgenerator.ModelGenerator._find_checkpoint_file')
    def test_modelgenerator_init_create_model_elif_w_yml_extn(self, mock_fcf, 
                                                                 mock_cm, mock_ospth):
        mock_ospth.return_value = True
        mock_cm.return_value = True
        mock_fcf = True
        obj = ModelGenerator(createmodel=True, file='./test.yml')

    @mock.patch('modelgen.modelgenerator.path')
    @mock.patch('modelgen.modelgenerator.ModelGenerator._create_model')
    @mock.patch('modelgen.modelgenerator.ModelGenerator._find_checkpoint_file')
    def test_modelgenerator_init_create_model_elif_wo_yaml_extn(self, mock_fcf, mock_cm, mock_ospth):
        mock_ospth.return_value = True
        mock_cm.return_value = True
        mock_fcf = True
        with self.assertRaises(NameError) as err:
            obj = ModelGenerator(createmodel=True, file='./test.txt')
        
    @mock.patch('modelgen.modelgenerator.path')
    @mock.patch('modelgen.modelgenerator.ModelGenerator._create_model')
    @mock.patch('modelgen.modelgenerator.ModelGenerator._find_checkpoint_file')
    def test_modelgenerator_createmodel_find_checkpoint_file_true(self, mock_fcf, 
                                                                mock_cm, mock_ospth):
        mock_ospth.return_value = True
        mock_cm.return_value = True
        mock_fcf = True
        obj = ModelGenerator(createmodel=True, file='./test.yaml')

    @mock.patch('modelgen.modelgenerator.path')
    @mock.patch('modelgen.modelgenerator.ModelGenerator._create_model')
    @mock.patch('modelgen.modelgenerator.ModelGenerator._find_checkpoint_file')
    def test_modelgenerator_createmodel_find_checkpoint_file_false(self, mock_fcf, 
                                                                mock_cm, mock_ospth):
        mock_ospth.return_value = True
        mock_cm.return_value = True
        mock_fcf.return_value = False
        obj = ModelGenerator(createmodel=True, file='./test.yaml')
        mock_fcf.assert_called_with()

    @mock.patch('modelgen.modelgenerator.Helper.write_to_file')
    def test_create_checkpoint_file(self, mock_wrtf):
        mock_wrtf.return_value = True
        obj = ModelGenerator()
        obj._create_checkpoint_file(init='./dummy')
        mock_wrtf.assert_called_with(path='./dummy/.modelgen', data='')

    @mock.patch('modelgen.modelgenerator.path')
    def test_find_checkpoint_file_exists(self, mock_ospth):
        mock_ospth.exists.return_value = True
        obj = ModelGenerator()
        response = obj._find_checkpoint_file()
        self.assertEqual(response, True)
        mock_ospth.exists.assert_called_with(mock_ospth.join())

    @mock.patch('modelgen.modelgenerator.path')
    def test_find_checkpoint_file_not_found(self, mock_ospth):
        mock_ospth.exists.return_value = False
        obj = ModelGenerator()
        with self.assertRaises(FileNotFoundError) as err:
            obj._find_checkpoint_file()

    @classmethod
    def tearDownClass(self):
        pass