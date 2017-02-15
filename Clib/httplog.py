
import logging
import os,time
from logging.handlers import TimedRotatingFileHandler

class HttpLog():
    def __init__(self,name):
        time1=time.strftime('%Y%m%d',time.localtime(time.time()))
        self.file_name = os.getcwd()+"/"+time1+"-"+name+".log"
        self.log=logging.getLogger()
        logformatter = logging.Formatter('%(asctime)s %(filename)s:%(module)s %(levelname)s %(message)s')
        loghandle = TimedRotatingFileHandler(self.file_name, 'midnight', 1, 10)
        loghandle.setFormatter(logformatter)
        loghandle.suffix = '%Y%m%d'
        self.log.addHandler(loghandle)
        self.log.setLevel(logging.DEBUG)


def log(name):
    return HttpLog(name=name)





