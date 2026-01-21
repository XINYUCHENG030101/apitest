import logging
import os.path
from cgitb import handler
import time


class infoFilter(logging.Filter):
    def filter(self, record):
        return  record.levelno == logging.INFO

class errFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR


class logger:
    @classmethod
    def getlog(cls):
        #创建日志对象
        cls.logger = logging.getLogger(__name__)
        #设置日志等级
        cls.logger.setLevel(logging.DEBUG)
        LOG_PATH = "./logs/"
        if not os.path.exists(LOG_PATH):
            os.mkdir(LOG_PATH)

        #创建日志名称
        now = time.strftime("%Y-%m-%d")
        logname = LOG_PATH+ now + ".log"
        infologname = LOG_PATH + now + "-info" + ".log"
        errlogname = LOG_PATH + now + "-err" + ".log"
        #设置输出格式
        formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] [%(filename)s (%(funcName)s:%(lineno)d)]-%(message)s")

        allhandler = logging.FileHandler(filename=logname,encoding="utf-8")
        infohandler = logging.FileHandler(filename=infologname,encoding="utf-8")
        errhandler = logging.FileHandler(filename=errlogname,encoding="utf-8")

        allhandler.setFormatter(formatter)
        infohandler.setFormatter(formatter)
        errhandler.setFormatter(formatter)

        infohandler.addFilter(infoFilter())
        errhandler.addFilter(errFilter())

        cls.logger.addHandler(allhandler)
        cls.logger.addHandler(infohandler)
        cls.logger.addHandler(errhandler)
        return cls.logger


