from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Iterator

import allure
import pytest

from services.blog_scenario_service import BlogScenarioService
from services.blog_service import BlogService
from services.user_scenario_service import UserScenarioService
from services.user_service import UserService
from utils.assert_util import ApiAssert
from utils.config_util import Settings, get_settings
from utils.db_util import DatabaseClient
from utils.request_util import ApiClient


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default=os.getenv("APITEST_ENV"),
        help="运行环境，对应 config/settings.yml 中 environments 的键",
    )


@pytest.fixture(scope="session")
def settings(pytestconfig: pytest.Config) -> Settings:
    return get_settings(pytestconfig.getoption("--env"))


@pytest.fixture(scope="session")
def api_client(settings: Settings) -> Iterator[ApiClient]:
    client = ApiClient(settings)
    yield client
    client.close()


@pytest.fixture(scope="session")
def user_service(api_client: ApiClient) -> UserService:
    return UserService(api_client)


@pytest.fixture(scope="session")
def blog_service(api_client: ApiClient) -> BlogService:
    return BlogService(api_client)


@pytest.fixture(scope="session")
def user_scenario_service(
    user_service: UserService,
    blog_service: BlogService,
) -> UserScenarioService:
    return UserScenarioService(user_service, blog_service)


@pytest.fixture(scope="session")
def blog_scenario_service(blog_service: BlogService) -> BlogScenarioService:
    return BlogScenarioService(blog_service)


@pytest.fixture(scope="session")
def auth_token(settings: Settings, user_service: UserService) -> str:
    account = settings.account("default")
    response = user_service.login(account["username"], account["password"])
    token = ApiAssert.success(response).get("data")
    ApiAssert.not_empty(token, "登录 fixture 未获取到 token")
    return str(token)


@pytest.fixture(scope="session")
def db_client(settings: Settings) -> DatabaseClient:
    return DatabaseClient(settings)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    context = {
        "nodeid": item.nodeid,
        "environment": item.config.getoption("--env") or "settings default",
        "failure": str(report.longrepr),
    }
    allure.attach(
        json.dumps(context, ensure_ascii=False, indent=2),
        name="failure-context",
        attachment_type=allure.attachment_type.JSON,
    )


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    results_dir = Path("reports/allure-results")
    if not results_dir.exists():
        return
    environment = session.config.getoption("--env") or os.getenv("APITEST_ENV") or "test"
    (results_dir / "environment.properties").write_text(
        f"Environment={environment}\nPython={os.sys.version.split()[0]}\n",
        encoding="utf-8",
    )
