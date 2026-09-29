import allure

from services.blog_service import BlogService
from utils.assert_util import ApiAssert
from utils.schema_util import BLOG_LIST_RESPONSE_SCHEMA, assert_schema


@allure.epic("接口自动化")
@allure.feature("博客")
class TestBlogList:
    @allure.story("未登录访问博客列表")
    def test_list_requires_login(self, blog_service: BlogService) -> None:
        response = blog_service.get_list()
        ApiAssert.status_code(response, 401)

    @allure.story("登录后获取博客列表")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_list_success(self, auth_token: str, blog_service: BlogService) -> None:
        response = blog_service.get_list(auth_token)
        body = ApiAssert.success(response)
        assert_schema(body, BLOG_LIST_RESPONSE_SCHEMA, "blog list response")
