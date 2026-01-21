from jsonschema.validators import validate

from utils.request_util import host, request
from utils.yaml_util import read_yaml


class TestList:
    url = host + "blog/getList"
    schema = {
      "type": "object",
      "required": ["code","errMsg"],
      "additionalProperties": False,
      "properties": {
        "code": {
          "type": "string"
        },
        "errMsg": {
          "type": "string"
        },
        "data": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id","title","content","userId","deleteFlag","createTime","updateTime","loginUser"],
            "additionalProperties": False,
            "properties": {
              "id": {
                "type": "number"
              },
              "title": {
                "type": "string"
              },
              "content": {
                "type": "string"
              },
              "userId": {
                "type": "number"
              },
              "deleteFlag": {
                "type": "integer"
              },
              "createTime": {
                "type": "string"
              },
              "updateTime": {
                "type": "string"
              },
              "loginUser": {
                "type": "boolean"
              }
            }
          }
        }
      }
    }
    def test_list_nologin(self):
        r = request().get(self.url)
        assert r.status_code == 401
    def test_list_login(self):
        token = read_yaml("data.yml","user_token_hearder")
        header = {"User_token_header":token}
        r = request().get(url=self.url,headers=header)
        validate(r.json(),self.schema)
        assert r.status_code == 200
        assert r.json()["code"] == "SUCCESS"