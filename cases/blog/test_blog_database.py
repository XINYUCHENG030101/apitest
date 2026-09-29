import allure
import pytest

from services.blog_service import BlogService
from utils.assert_util import ApiAssert
from utils.db_util import DatabaseClient


@allure.epic("接口自动化")
@allure.feature("博客")
@allure.story("博客数据库校验")
@pytest.mark.db
def test_blog_matches_database(
    auth_token: str,
    blog_service: BlogService,
    db_client: DatabaseClient,
) -> None:
    if not db_client.enabled:
        pytest.skip("config/settings.yml 未启用数据库校验")

    blogs = ApiAssert.success(blog_service.get_list(auth_token)).get("data", [])
    ApiAssert.not_empty(blogs, "博客列表为空，无法进行数据库校验")
    actual = db_client.fetch_one(
        "SELECT id, title, content, user_id AS userId FROM blog WHERE id = %s",
        (blogs[0]["id"],),
    )
    assert actual is not None, "数据库中不存在该博客"
    assert actual["title"] == blogs[0]["title"]
    assert actual["content"] == blogs[0]["content"]
