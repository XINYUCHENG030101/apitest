# API 自动化测试项目

基于 `pytest + requests + PyYAML + Allure` 的接口自动化测试项目，支持多环境配置、YAML 数据驱动、登录鉴权、场景服务封装、数据库校验、日志记录及 Allure 测试报告。

## 技术栈

- Python 3.10+
- pytest
- requests
- PyYAML
- jsonschema
- PyMySQL
- allure-pytest

## 项目结构

```text
apitest/
├── cases/                         # pytest 测试用例
│   ├── blog/                      # 博客相关用例
│   │   ├── test_blog_create.py
│   │   ├── test_blog_database.py
│   │   ├── test_blog_detail.py
│   │   └── test_blog_list.py
│   └── user/                      # 用户相关用例
│       ├── test_login.py
│       └── test_user_info.py
├── config/
│   └── settings.yml               # 环境、账号、接口、数据库、报告等配置
├── data/
│   └── cases/                     # YAML 数据驱动测试数据
│       ├── blog.yml
│       └── user.yml
├── services/                      # 业务接口及组合场景封装
│   ├── blog_service.py
│   ├── blog_scenario_service.py
│   ├── user_service.py
│   ├── user_scenario_service.py
│   └── scenario_result.py
├── utils/                         # 公共工具
│   ├── assert_util.py             # 接口断言工具
│   ├── config_util.py             # 配置读取及环境合并
│   ├── db_util.py                 # 数据库访问工具
│   ├── log_util.py                # 日志工具
│   ├── request_util.py            # HTTP 请求客户端
│   ├── schema_util.py             # JSON Schema 校验工具
│   └── yaml_util.py               # YAML 数据读取工具
├── logs/                          # 运行日志（执行时生成）
├── reports/                       # Allure 结果与报告（执行时生成）
├── conftest.py                    # pytest 配置、fixture 与失败信息收集
├── pytest.ini                     # pytest 发现规则、marker 及默认参数
├── requirements.txt               # Python 依赖
├── run.py                         # 跨平台统一执行入口
├── run.ps1                        # Windows PowerShell 启动脚本
└── run.cmd                        # Windows CMD 启动脚本
```

## 环境准备

进入项目根目录：

```powershell
cd apitest
```

创建并激活虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

如果 PowerShell 禁止执行激活脚本，可以直接使用 `.venv\Scripts\python.exe` 执行后续命令，或者在当前终端临时调整执行策略：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

安装依赖：

```powershell
python -m pip install -r requirements.txt
```

运行前请根据实际测试服务修改 `config/settings.yml` 中的环境地址、测试账号及数据库配置。

## 启动命令

### 使用统一 Python 入口（推荐）

运行默认环境：

```powershell
python run.py
```

指定环境：

```powershell
python run.py --env test
python run.py --env staging
```

按 marker 运行：

```powershell
python run.py --env test -m smoke
python run.py --env test -m "smoke and not destructive"
```

运行指定文件或指定用例：

```powershell
python run.py --env test cases/user/test_login.py
python run.py --env test cases/user/test_login.py::test_login_success
```

向 pytest 透传其他参数：

```powershell
python run.py --env test -k login -s
python run.py --env test --maxfail=3
```

### 使用 PowerShell 脚本

```powershell
.\run.ps1
.\run.ps1 -EnvName test
.\run.ps1 -EnvName test -Marker smoke
```

`run.ps1` 会优先使用 `.venv\Scripts\python.exe`，不存在虚拟环境时使用系统的 `python`。

### 使用 CMD 脚本

```bat
run.cmd
run.cmd test
run.cmd test -m smoke
run.cmd staging -k login -s
```

`run.cmd` 的第一个位置参数为环境名，其余参数会继续传递给 `run.py`/pytest；未传环境时默认为 `test`。

### 直接使用 pytest

```powershell
pytest --env test
pytest cases/user/test_login.py --env test -v
pytest -m smoke --env test
```

> 直接执行 pytest 时使用 `pytest.ini` 中的默认参数；使用 `run.py` 时还会读取 `settings.yml` 的 `run` 配置并按配置清理、创建 Allure 结果目录。

## 启动参数说明

### `run.py` 参数

| 参数 | 是否必填 | 说明 | 示例 |
| --- | --- | --- | --- |
| `--env` | 否 | 指定运行环境，对应 `settings.yml` 中 `environments` 的键；未传时依次读取 `APITEST_ENV` 和 `active_env` | `--env staging` |
| `-m`, `--marker` | 否 | pytest marker 表达式；优先级高于 `run.markers` | `-m "smoke and not destructive"` |
| 其他参数 | 否 | 未被 `run.py` 识别的参数会原样传给 pytest | `-k login -s --maxfail=2` |

### 常用 pytest 参数

| 参数 | 说明 | 示例 |
| --- | --- | --- |
| `-v` | 输出更详细的用例执行信息 | `-v` |
| `-s` | 不捕获标准输出，显示 `print` 内容 | `-s` |
| `-k EXPRESSION` | 按用例名称关键字筛选 | `-k login` |
| `-m EXPRESSION` | 按 marker 筛选 | `-m smoke` |
| `--maxfail=N` | 失败达到 N 条后停止 | `--maxfail=1` |
| `--lf` | 只执行上次失败的用例 | `--lf` |
| `--tb=short` | 使用简短错误堆栈 | `--tb=short` |
| `--collect-only` | 只收集并展示用例，不执行 | `--collect-only` |

### 已注册的 marker

| marker | 说明 |
| --- | --- |
| `smoke` | 核心冒烟用例 |
| `destructive` | 会新增或修改服务端数据的用例 |
| `db` | 依赖数据库连接的校验用例；数据库未启用时自动跳过 |

示例：排除可能修改服务端数据的用例：

```powershell
python run.py --env test -m "not destructive"
```

## 配置参数说明

项目主配置位于 `config/settings.yml`。

### 环境配置

```yaml
active_env: test

environments:
  test:
    base_url: "http://example.com"
    verify_ssl: false
    timeout: 10
```

| 参数 | 说明 |
| --- | --- |
| `active_env` | 未通过命令行或环境变量指定环境时使用的默认环境 |
| `environments.<name>` | 环境配置；`<name>` 即 `--env` 可用值 |
| `base_url` | 被测服务基础地址 |
| `verify_ssl` | 是否校验 HTTPS 证书，生产或正式环境建议设为 `true` |
| `timeout` | HTTP 请求超时时间，单位为秒 |

环境选择优先级为：`--env` 命令行参数 > `APITEST_ENV` 环境变量 > `active_env`。

通过环境变量运行示例：

```powershell
$env:APITEST_ENV = "staging"
python run.py
```

### 账号与鉴权

| 参数 | 说明 |
| --- | --- |
| `accounts.<name>.username` | 指定账号的用户名 |
| `accounts.<name>.password` | 指定账号的密码 |
| `auth.token_header` | 后续请求携带登录令牌时使用的请求头名称 |

测试代码可通过 `settings.account("default")` 获取指定账号。请勿将真实生产账号或密码提交到代码仓库，建议在 CI/CD 中使用密钥变量注入。

### 接口地址

`endpoints` 按业务域维护接口相对路径，例如：

```yaml
endpoints:
  user:
    login: "/user/login"
    info: "/user/getInfo"
  blog:
    list: "/blog/getList"
```

最终请求地址由 `base_url + endpoint` 组成。新增接口时，需要同时在对应的 service 中增加调用方法。

### 数据库配置

| 参数 | 说明 |
| --- | --- |
| `database.enabled` | 是否启用数据库连接；为 `false` 时 `db` 用例会跳过 |
| `database.driver` | 数据库驱动，当前项目使用 MySQL/PyMySQL |
| `database.host` | 数据库主机地址 |
| `database.port` | 数据库端口 |
| `database.database` | 数据库名称 |
| `database.username` | 数据库用户名 |
| `database.password` | 数据库密码 |
| `database.charset` | 数据库字符集 |

### 报告配置

| 参数 | 说明 |
| --- | --- |
| `report.allure_results` | Allure 原始结果目录 |
| `report.allure_report` | Allure HTML 报告输出目录 |
| `report.clean_results` | 每次通过 `run.py` 执行前是否删除旧结果 |

### 运行配置

| 参数 | 说明 |
| --- | --- |
| `run.paths` | 默认执行的测试目录或文件列表 |
| `run.markers` | 默认 marker 表达式；命令行 `-m` 会覆盖此值 |
| `run.maxfail` | 最大失败数；设置为 `0` 表示不限制 |
| `run.verbose` | 是否默认添加 pytest 的 `-v` 参数 |
| `run.extra_args` | 额外传给 pytest 的参数列表，例如 `["-s", "--tb=short"]` |

### 日志配置

| 参数 | 说明 |
| --- | --- |
| `logging.level` | 日志级别，如 `DEBUG`、`INFO`、`WARNING` |
| `logging.directory` | 日志输出目录 |
| `logging.max_bytes` | 单个日志文件最大字节数 |
| `logging.backup_count` | 滚动日志保留数量 |

## 测试数据说明

数据驱动文件位于 `data/cases/`，按业务模块拆分。每条数据建议提供唯一的 `id`，方便 pytest 参数化结果与 Allure 报告定位，例如：

```yaml
login_failure:
  - id: wrong-password
    username: zhangsan
    password: "123"
    expected_message: "密码错误"
```

## Allure 报告

Python 依赖中的 `allure-pytest` 负责生成结果文件。查看 HTML 报告还需要在本机安装 Allure Commandline，并确保 `allure` 命令已加入 `PATH`。

执行测试：

```powershell
python run.py --env test
```

临时启动报告服务：

```powershell
allure serve reports/allure-results
```

生成静态报告：

```powershell
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

## 执行结果

pytest 进程退出码可用于本地脚本或 CI 判断结果：

| 退出码 | 含义 |
| --- | --- |
| `0` | 所有已执行用例通过 |
| `1` | 存在失败用例 |
| `2` | 执行被中断 |
| `3` | pytest 内部错误 |
| `4` | 命令行参数错误 |
| `5` | 未收集到测试用例 |
