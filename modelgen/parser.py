from modelgen import Base, constants as cst
from yaml import safe_load, YAMLError

class Parser(Base):

    def __init__(self, filepath: str):
        Base.__init__(self)
        self.data = self.read_yaml(filepath)
        self.tables = list(self.data[cst.key_tables].keys())
        self.schema = self.get_tables_w_columns()

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

    def get_tables_w_columns(self) -> dict:
        self.logger.info('Creating schema from YAML')
        schema = dict()
        tables_data = self.data[cst.key_tables]
        for table in self.tables:
            self.logger.debug(f"Getting schema for table {table}")
            column_data = dict()
            if cst.key_inherit_from in tables_data[table]:
                self.logger.debug('Found keyword `inherit_from`')
                self.logger.info(f"Inheriting structure from table {tables_data[table][cst.key_inherit_from]}")
                iter_table = tables_data[tables_data[table][cst.key_inherit_from]][cst.key_columns]
            else:
                self.logger.info(f"Getting structure from table {table}")
                iter_table = tables_data[table][cst.key_columns]
            for column in iter_table:
                column_data.update({column[cst.key_column_name]: column[cst.key_column_type]})

            schema.update({table: column_data})

        return schema
