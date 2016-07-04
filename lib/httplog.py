
import logging
import os
from logging.handlers import TimedRotatingFileHandler

class httplog():
    def __init__(self):
        self.file_name = os.getcwd()+"\httplog.log"
        self.log=logging.getLogger()
        logformatter = logging.Formatter('%(asctime)s %(filename)s:%(module)s [line:%(lineno)d] %(levelname)s %(message)s')
        loghandle = TimedRotatingFileHandler(self.file_name, 'midnight', 1, 2)
        loghandle.setFormatter(logformatter)
        loghandle.suffix = '%Y%m%d'
        self.log.addHandler(loghandle)
        self.log.setLevel(logging.DEBUG)

httplog=httplog()
