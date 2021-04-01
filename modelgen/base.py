from modelgen.log_source import Logging
from os import environ

class Base:

    def __init__(self):
        log_level = environ.get('LOG_LEVEL', 'INFO')
        self.logger = Logging(log_level=log_level).get_logger()
