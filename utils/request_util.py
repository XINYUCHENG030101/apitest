import requests

from utils.log_util import logger
host = "http://115.190.63.202:9090/"

class request:
    log = logger.getlog()
    def get(self,url,**kwargs):
        #打印接口信息
        self.log.info("接口url{}".format(url))
        self.log.info("接口信息{}".format(kwargs))
        r = requests.get(url=url,**kwargs)
        self.log.info("接口状态码{}".format(r.status_code))
        self.log.info("接口返回值{}".format(r.text))
        return r
    def post(self,url,**kwargs):
        self.log.info("接口url{}".format(url))
        self.log.info("接口信息{}".format(kwargs))
        r = requests.post(url=url,**kwargs)
        self.log.info("接口状态码{}".format(r.status_code))
        self.log.info("接口返回值{}".format(r.text))
        return r

