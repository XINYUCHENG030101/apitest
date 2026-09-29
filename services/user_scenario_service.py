from __future__ import annotations

from services.blog_service import BlogService
from services.scenario_result import AuthorFromFirstBlogScenarioResult, LoginUserScenarioResult
from services.user_service import UserService
from utils.assert_util import ApiAssert


class UserScenarioService:
    def __init__(self, user_service: UserService, blog_service: BlogService):
        self.user_service = user_service
        self.blog_service = blog_service

    def login_and_get_user_info(self, username: str, password: str) -> LoginUserScenarioResult:
        login_response = self.user_service.login(username, password)
        login_body = ApiAssert.success(login_response)
        token = login_body.get("data")
        ApiAssert.not_empty(token, "登录成功后未返回 token")
        info_response = self.user_service.get_user_info(str(token))
        return LoginUserScenarioResult(str(token), login_response, info_response)

    def get_first_blog_author(self, token: str) -> AuthorFromFirstBlogScenarioResult:
        list_response = self.blog_service.get_list(token)
        blogs = ApiAssert.success(list_response).get("data", [])
        ApiAssert.not_empty(blogs, "博客列表为空，无法获取首篇博客作者")
        first_blog = blogs[0]
        author_response = self.user_service.get_author_info(first_blog["userId"], token)
        return AuthorFromFirstBlogScenarioResult(first_blog, list_response, author_response)
