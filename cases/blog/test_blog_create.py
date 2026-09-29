import allure
import pytest

from services.blog_scenario_service import BlogScenarioService
from utils.yaml_util import case_ids, load_cases

CREATE_CASES = load_cases("cases/blog.yml", "create_blog")


@allure.epic("接口自动化")
@allure.feature("博客")
class TestCreateBlog:
    @allure.story("新增后校验列表和详情")
    @pytest.mark.destructive
    @pytest.mark.parametrize("case", CREATE_CASES, ids=case_ids(CREATE_CASES))
    def test_create_and_verify(
        self,
        case: dict,
        auth_token: str,
        blog_scenario_service: BlogScenarioService,
    ) -> None:
        result = blog_scenario_service.create_and_verify(
            case["title"], case["content"], auth_token
        )
        assert result.created_blog["id"] == result.blog_id
