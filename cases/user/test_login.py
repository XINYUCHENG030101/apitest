import allure
import pytest

from services.user_service import UserService
from utils.assert_util import ApiAssert
from utils.config_util import Settings
from utils.schema_util import LOGIN_RESPONSE_SCHEMA, assert_schema
from utils.yaml_util import case_ids, load_cases

FAILURE_CASES = load_cases("cases/user.yml", "login_failure")
SUCCESS_CASES = load_cases("cases/user.yml", "login_success")


@allure.epic("接口自动化")
@allure.feature("用户")
class TestLogin:
    @allure.story("登录失败")
    @pytest.mark.parametrize("case", FAILURE_CASES, ids=case_ids(FAILURE_CASES))
    def test_login_failure(self, case: dict, user_service: UserService) -> None:
        response = user_service.login(case["username"], case["password"])
        body = ApiAssert.business_error(response, case["expected_message"])
        assert_schema(body, LOGIN_RESPONSE_SCHEMA, "login failure response")

    @allure.story("登录成功")
    @pytest.mark.smoke
    @pytest.mark.parametrize("case", SUCCESS_CASES, ids=case_ids(SUCCESS_CASES))
    def test_login_success(
        self,
        case: dict,
        settings: Settings,
        user_service: UserService,
    ) -> None:
        account = settings.account(case["account"])
        response = user_service.login(account["username"], account["password"])
        body = ApiAssert.success(response)
        assert_schema(body, LOGIN_RESPONSE_SCHEMA, "login success response")
        ApiAssert.not_empty(body.get("data"), "登录成功后 token 为空")
