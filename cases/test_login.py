#测试登录接口
import re

import pytest
from jsonschema.validators import validate

from utils.request_util import host,request
from utils.yaml_util import write_yaml


class Test_login:
    url=host+"user/login"
    schema = {
          "type": "object",
          "required": ["code","errMsg","data"],
          "additionalProperties":False,
          "properties": {
            "code": {
              "type": "string"
            },
            "errMsg": {
              "type": "string"
            },
            "data": {
              "type": ["string","null"]
            }
          }
        }
    @pytest.mark.parametrize("login",[
        #正确的用户名错误的密码
        {"username":"zhangsan","password":"123","errMsg": "密码错误"},
        #正确的密码错误的用户名
        {"username":"zhangsa","password":"123456","errMsg": "用户不存在"},
        #用户名和密码都是错误的
        {"username":"zhangsa","password":"123","errMsg": "用户不存在"},
        #使用空用户名登录
        {"username":"","password":"123456","errMsg": "账号或密码不能为空"},
        # 使用空密码
        {"username": "zhangsan", "password": "", "errMsg": "账号或密码不能为空"},
        #使用长用户名
        {"username": "这是一个长用户名这是一个长用户名这是一个长用户名这是一个长用户名这是一个长用户名这是一个长用户名这是一个长用户名这是一个长用户名这是一个长用户名这是一个长用户名这是一个长用户名这是一个长用户名这是一个长用户名这是一个长用户名这是一个长用户名这是一个长用户名这是一个长用户名这是一个长用户名",
         "password": "123456", "errMsg": "用户不存在"},
        #使用长密码
        {"username": "zhangsan", "password": "这是一个长密码这是一个长密码这是一个长密码这是一个长密码这是一个长密码这是一个长密码这是一个长密码这是一个长密码这是一个长密码这是一个长密码这是一个长密码这是一个长密码这是一个长密码这是一个长密码这是一个长密码这是一个长密码这是一个长密码这是一个长密码这是一个长密码这是一个长密码",
         "errMsg": "密码错误"}
        ])


    def test_login_fail(self,login):
        data = {"username":login["username"],
                "password":login["password"]}
        r = request().post(url=self.url,data=data)
        validate(r.json(), self.schema)
        assert r.json()["code"] == "FAIL"
        assert r.json()['errMsg'] == login["errMsg"]

    @pytest.mark.parametrize("login",[{"username": "zhangsan","password":"123456"},
                                         {"username": "lisi","password":"123456"}])
    def test_login_success(self,login):
        data = {"username":login["username"],
                "password":login["password"]}
        r = request().post(url=self.url,data=data)
        validate(r.json(),self.schema)
        assert r.json()["code"] == "SUCCESS"
        assert re.match(r'\S{100,}', r.json()['data'])
        data = {"user_token_hearder":r.json()['data']}
        write_yaml("data.yml",data)