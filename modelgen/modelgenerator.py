from os import path, getcwd
from pathlib import Path
from shutil import copyfile, copytree

from modelgen.helper import Helper
from modelgen import (__file__, constants, Validate, Parser, 
                      Template, alchemygen, metagen, walk)

class ModelGenerator(Helper):

    def __init__(self, init=False, createmodel=False, file=None, alembic=False,**kwargs):
        Helper.__init__(self)
        self.init = init
        if bool(self.init):
            if path.isabs(self.init):
                self.dst_path = path.join(self.init)
            else:
                self.dst_path = path.join(getcwd(), self.init)
            self._create_alembic_folder()
            self._create_template_folder()
            self._create_checkpoint_file()
        if self._find_checkpoint_file():
            self.dst_path = path.join(getcwd())
        if createmodel:
            if file.endswith('.yaml'):
                datasource = file.split('.yaml')[0].split('/')[-1]
            elif file.endswith('yml'):
                datasource = file.split('.yml')[0].split('/')[-1]
            else:
                raise NameError('Please specify a .yaml or .yml file')
            self._find_checkpoint_file()
            self._create_model(datasource=datasource, alembic=alembic)
        
    def _create_template_folder(self):
        try:
            templates_src_path = path.join('/',*(__file__.split('/')[:-1]),'templates')
            templates_dst_path = path.join(self.init, 'templates')
            self.logger.info(f'Creating templates folder at {templates_dst_path}')
            Path(templates_dst_path).mkdir(parents=True, exist_ok=False)
            self.logger.debug('Templates folder creation successful')
            self.logger.info(f'Creating an example yaml schema file at {templates_dst_path}/example.yaml')
            copyfile((path.join(templates_src_path, 'example.yaml')), 
                    path.join(templates_dst_path, 'example.yaml'))
            return True
        except FileExistsError as e:
            self.logger.exception('Error occurred while creating templates folder')
            self.logger.exception(e)
            raise FileExistsError("Folder exists. Please specify a new folder name") from FileExistsError 
        except Exception as e:
            raise e from Exception

    def _create_alembic_folder(self):
        try:
           
            alembic_path = path.join('/',*(__file__.split('/')[:-1]),'alembic')
            self.logger.info(f'Creating alembic folder at {self.dst_path}')
            ini_src_path = path.join('/',*(__file__.split('/')[:-1]),'alembic.ini')
            copytree(alembic_path, path.join(self.dst_path, 'alembic'))
            Path(path.join(self.dst_path, 'alembic','versions')).mkdir(parents=True, exist_ok=False)
            copyfile(ini_src_path, path.join(self.dst_path, 'alembic.ini'))
        except FileExistsError as e:
            self.logger.exception('Error occurred while creating templates folder')
            self.logger.exception(e)
            raise FileExistsError("Folder exists. Please specify a new folder name") from FileExistsError 
        except Exception as e:
            raise e from Exception

    def _create_checkpoint_file(self):
        open(path.join(self.init, '.modelgen'), 'w').close()
        return True

    def _find_checkpoint_file(self):
        chkpnt_filepath = path.join(getcwd(), '.modelgen')
        if not path.exists(chkpnt_filepath):
            err_str = 'Either modelgen is not initialized, or you are in the wrong folder\n'
            err_str += 'Please initialize modelgen (modelgen --source yaml --init ./YOUR_FOLDER_NAME)'
            err_str += ' or execute commands from /path/YOUR_FOLDER_NAME'
            raise Exception(err_str)
        else:
            return True

    def _create_model(self, datasource: str, alembic: bool=False, filepath: str=None) -> bool:
        if not filepath:
            filepath = path.join(constants.templates_folder, f"{datasource}.yaml")
        Validate(filepath=filepath)
        parser = Parser(filepath=filepath)
        src_template = Template(alchemygen)
        py_code = src_template.render(datasource=datasource,yaml_data=parser.data, cst=constants, bool=bool)
        Path(constants.models_folder).mkdir(parents=True, exist_ok=True)
        py_filepath = path.join(constants.models_folder, f'{datasource}.py')
        self.write_to_file(path=py_filepath, data=py_code)
        if alembic:
            self._create_alembic_meta()
        return True

    def _create_alembic_meta(self) -> bool:
        alembic_template = Template(metagen)
        _, _, filenames = next(walk(constants.models_folder))
        alembic_meta = alembic_template.render(filenames=filenames, cst=constants,
                                            splitext=path.splitext)
        Path(constants.alembic_meta_folder).mkdir(parents=True, exist_ok=True)
        alembic_meta_filepath = path.join(constants.alembic_meta_folder, '__init__.py')
        self.write_to_file(path=alembic_meta_filepath, data=alembic_meta)
        return True