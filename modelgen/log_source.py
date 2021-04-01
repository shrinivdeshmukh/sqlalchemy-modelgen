import logging, os

class Logging:

    def __init__(self, log_level, filename=None):
        self.log_level = log_level
        self.root_log_dir = 'logs'
        self.filename = 'logs/{}'.format(filename)
        self.logger = logging.getLogger(__name__)

    def get_logger(self):
        logging.basicConfig(level=(self.log_level), format='%(asctime)s - %(message)s',
          datefmt='%d-%b-%y %H:%M:%S')
        return self.logger
