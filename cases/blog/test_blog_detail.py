import allure

from services.blog_service import BlogService
from utils.assert_util import ApiAssert
from utils.schema_util import BLOG_DETAIL_RESPONSE_SCHEMA, assert_schema


@allure.epic("接口自动化")
@allure.feature("博客")
class TestBlogDetail:
    @allure.story("获取博客详情")
    def test_get_first_blog_detail(self, auth_token: str, blog_service: BlogService) -> None:
        blogs = ApiAssert.success(blog_service.get_list(auth_token)).get("data", [])
        ApiAssert.not_empty(blogs, "博客列表为空，无法校验详情")
        response = blog_service.get_detail(blogs[0]["id"], auth_token)
        body = ApiAssert.success(response)
        assert_schema(body, BLOG_DETAIL_RESPONSE_SCHEMA, "blog detail response")
        assert body["data"]["id"] == blogs[0]["id"]
