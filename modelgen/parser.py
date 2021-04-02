from modelgen import constants as cst, Helper

class Parser(Helper):

    def __init__(self, filepath: str):
        Helper.__init__(self)
        self.data = self.read_yaml(filepath)
        self.tables = list(self.data[cst.key_tables].keys())
        self.schema = self.get_tables_w_columns()


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
