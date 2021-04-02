from modelgen.base import Base
from modelgen.helper import Helper
from utils import constants
from templates.alchemygen import alchemygen
from os import path, getcwd
from jinja2 import Template
from pathlib import Path
from modelgen.parser import Parser

def create_model(datasource: str) -> bool:
    h = Helper()
    filepath = path.join(constants.templates_folder, f"{datasource}.yaml")
    parser = Parser(filepath=filepath)
    src_template = Template(alchemygen)
    py_code = src_template.render(yaml_data=parser.data, cst=constants, bool=bool)
    Path(constants.models_folder).mkdir(parents=True, exist_ok=True)
    py_filepath = path.join(constants.models_folder, f'{datasource}.py')
    h.write_to_file(path=py_filepath, data=py_code)
    return True