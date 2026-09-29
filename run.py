from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import pytest

from utils.config_util import PROJECT_ROOT, get_settings


def build_args(env: str | None, marker: str | None, passthrough: list[str]) -> list[str]:
    settings = get_settings(env)
    run_config = settings.get("run", {})
    result_dir = settings.resolve_path(settings.get("report.allure_results", "reports/allure-results"))
    if settings.get("report.clean_results", True) and result_dir.exists():
        shutil.rmtree(result_dir)
    result_dir.mkdir(parents=True, exist_ok=True)

    args = [str(PROJECT_ROOT / path) for path in run_config.get("paths", ["cases"])]
    args.extend(["--alluredir", str(result_dir), "--env", settings.env])
    if run_config.get("verbose", True):
        args.append("-v")
    maxfail = int(run_config.get("maxfail", 0))
    if maxfail:
        args.append(f"--maxfail={maxfail}")
    selected_marker = marker if marker is not None else run_config.get("markers")
    if selected_marker:
        args.extend(["-m", selected_marker])
    args.extend(str(value) for value in run_config.get("extra_args", []))
    args.extend(passthrough)
    return args


def main() -> int:
    parser = argparse.ArgumentParser(description="apitest 统一执行入口")
    parser.add_argument("--env", help="运行环境，如 test、staging")
    parser.add_argument("-m", "--marker", help="pytest marker 表达式")
    known, passthrough = parser.parse_known_args()
    return pytest.main(build_args(known.env, known.marker, passthrough))


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
