import allure

from services.user_scenario_service import UserScenarioService
from utils.assert_util import ApiAssert
from utils.config_util import Settings
from utils.schema_util import USER_INFO_RESPONSE_SCHEMA, assert_schema


@allure.epic("接口自动化")
@allure.feature("用户")
class TestUserInfo:
    @allure.story("登录后获取用户信息")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_info_after_login(
        self,
        settings: Settings,
        user_scenario_service: UserScenarioService,
    ) -> None:
        account = settings.account("default")
        result = user_scenario_service.login_and_get_user_info(
            account["username"], account["password"]
        )
        body = ApiAssert.success(result.user_info_response)
        assert_schema(body, USER_INFO_RESPONSE_SCHEMA, "user info response")
        ApiAssert.not_empty(body.get("data"), "用户信息为空")

    @allure.story("通过首篇博客获取作者信息")
    def test_get_author_from_first_blog(
        self,
        auth_token: str,
        user_scenario_service: UserScenarioService,
    ) -> None:
        result = user_scenario_service.get_first_blog_author(auth_token)
        body = ApiAssert.success(result.author_response)
        assert_schema(body, USER_INFO_RESPONSE_SCHEMA, "author response")
        ApiAssert.not_empty(body.get("data"), "作者信息为空")
