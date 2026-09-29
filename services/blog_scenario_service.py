from __future__ import annotations

from services.blog_service import BlogService
from services.scenario_result import CreateBlogScenarioResult
from utils.assert_util import ApiAssert


class BlogScenarioService:
    def __init__(self, blog_service: BlogService):
        self.blog_service = blog_service

    def create_and_verify(self, title: str, content: str, token: str) -> CreateBlogScenarioResult:
        add_response = self.blog_service.add_blog(title, content, token)
        created = ApiAssert.success(add_response).get("data") or {}
        if not isinstance(created, dict):
            raise AssertionError(f"新增博客 data 应为对象，实际为: {created!r}")
        blog_id = created.get("id")
        ApiAssert.not_empty(blog_id, "新增博客响应中缺少 id")

        list_response = self.blog_service.get_list(token)
        blogs = ApiAssert.success(list_response).get("data", [])
        assert any(item.get("id") == blog_id for item in blogs), "新增博客未出现在列表中"

        detail_response = self.blog_service.get_detail(blog_id, token)
        detail = ApiAssert.success(detail_response).get("data") or {}
        assert detail.get("title") == title, f"博客详情标题不符: {detail}"
        assert detail.get("content") == content, f"博客详情内容不符: {detail}"
        return CreateBlogScenarioResult(blog_id, created, add_response, list_response, detail_response)
