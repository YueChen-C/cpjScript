
import logging
import os,time
from logging.handlers import TimedRotatingFileHandler

class HttpLog():
    def __init__(self,name):
        time1=time.strftime('%Y%m%d',time.localtime(time.time()))
        self.file_name = os.getcwd()+"/"+time1+"-"+name+".log"
        self.log=logging.getLogger(name)
        logformatter = logging.Formatter('%(asctime)s %(filename)s:%(module)s %(levelname)s %(message)s')
        loghandle = TimedRotatingFileHandler(self.file_name, 'midnight', 1, 10)
        loghandle.setFormatter(logformatter)
        loghandle.suffix = '%Y%m%d'
        self.log.addHandler(loghandle)
        self.log.setLevel(logging.DEBUG)
        self.log.removeHandler(loghandle)



def log(name, err):
    time1=time.strftime('%Y%m%d',time.localtime(time.time()))
    file_name = os.getcwd()+"/"+time1+"-"+name+".log"
    log=logging.getLogger(name)
    logformatter = logging.Formatter('%(asctime)s %(filename)s:%(module)s %(levelname)s %(message)s')
    loghandle = TimedRotatingFileHandler(file_name, 'midnight', 1, 10)
    loghandle.setFormatter(logformatter)
    loghandle.suffix = '%Y%m%d'
    log.addHandler(loghandle)
    log.setLevel(logging.DEBUG)
    log.exception(err)
    log.removeHandler(loghandle)






