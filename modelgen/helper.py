from modelgen import Base
from yaml import safe_load, YAMLError

class Helper(Base):

    def __init__(self):
        Base.__init__(self)

    def unpack_kwargs(self, kwargs: dict) -> str:
        """
        Function to format kwargs and translate the dictionary
        to be used to render the jinja template

        Args:
            kwargs (dict): Parameters packed in a python dictionary
                    ex: {'redshift_distkey': 'id', 'redshift_diststyle': 'KEY'}

        Returns:
            (str): ex: redshift_distkey='id',redshift_diststyle='KEY'
        """
        stmt = ','.join((f"{a}={b}" for a, b in kwargs.items()))
        return stmt

    def read_yaml(self, filepath: str) -> dict:
        """
        Function to read yaml and return it's contents in
        the form of python dictionary

        Args:
            filepath (str): path where the yaml file is stored
                            ex: './templates/file.yaml'
        Returns:
            (dict): Python-dictionary representation of the yaml file
        """
        try:
            self.logger.info(f"Reading file {filepath} and converting it to python dict")
            with open(filepath, 'r') as f:
                data = safe_load(f)
            return data
        except YAMLError as e:
            try:
                self.logger.exception(e)
                raise Exception(e)
            finally:
                e = None
                del e

    def write_to_file(self, path, data):
        with open(path, 'w') as f:
            f.write(data)
        return True
