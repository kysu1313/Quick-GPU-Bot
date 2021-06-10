import logging
import sys
from datetime import datetime

class Logger():
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.logger = logging.getLogger()
        self.logger.addHandler(self.file_handler)
        self.logger.setLevel(logging.INFO)
        self.logger = logging.getLogger()

    def log_info(self, msg):
        date = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " ===> "
        self.logger.log(logging.INFO, date + msg)

    def log_warning(self, msg):
        date = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " ===> "
        self.logger.log(logging.WARNING, date + msg)

    def log_error(self, msg):
        date = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " ===> "
        self.logger.log(logging.ERROR, date + msg)
