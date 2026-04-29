# Agent Harness Lab 中文说明

Agent Harness Lab 是一个面向真实本地项目的 TDD-first Agent Harness。它不是聊天机器人，也不是只用于展示的 Demo，而是一个让 Agent 工作流更安全进入项目的工程化底座：先扫描项目、读取任务、执行配置好的检查命令，再生成可复查的报告和机器可读结果。

## 它解决什么问题

在让 AI Agent 直接参与项目之前，项目通常需要先回答几个问题：

- 当前项目有哪些代码、文档、配置和关键工件？
- 这个任务的目标、风险和下一步是什么？
- 项目自己的测试、lint 或 build 能不能跑通？
- Agent 工作流的运行过程有没有可追踪的事件记录？
- 输出能不能既给人看，也给程序或 CI 继续处理？

Agent Harness Lab 解决的是“进入项目之前”和“运行之后可复盘”的工程问题。

## 核心能力

- 扫描任意本地项目目录。
- 读取 Markdown 任务文件。
- 通过 `harness.yaml` 配置项目名、输出目录、忽略目录和检查命令。
- 执行项目自定义 checks，例如单元测试、lint、build。
- 输出 `run-report.md`，给人阅读和复盘。
- 输出 `run-result.json`，给脚本、CI 或后续工具读取。
- 输出 `events.jsonl`，记录运行事件，例如任务加载、项目扫描、检查完成、报告生成。
- 内置轻量评测，确认报告包含关键结构和运行结果。

## 快速运行

在本仓库中运行：

```powershell
python .\agent_workflow.py
```

运行内置评测：

```powershell
python .\agent_workflow.py --eval
```

对另一个项目运行：

```powershell
python -m agent_harness_lab.cli run --project D:\path\to\project --task D:\path\to\task.md
```

对另一个项目运行并评测报告：

```powershell
python -m agent_harness_lab.cli eval --project D:\path\to\project --task D:\path\to\task.md
```

## 配置文件示例

在目标项目根目录放一个 `harness.yaml`：

```yaml
project_name: My Service
output_dir: harness-results
max_artifact_files: 12
check_timeout_seconds: 60
ignore_dirs:
  - node_modules
  - dist
  - tmp
checks:
  - name: unit-tests
    command: python -m unittest discover -s tests -v
  - name: lint
    command: python -m ruff check .
```

`checks` 会在目标项目根目录执行。不要在不可信仓库里直接运行未知的 `harness.yaml`，需要先检查命令内容。

## 输出产物

默认输出目录由 `harness.yaml` 的 `output_dir` 决定。

`run-report.md`
给人看的报告，包含项目扫描结果、项目工件、运行契约、事件、项目检查结果、风险和下一步。

`run-result.json`
给程序读取的结构化结果，包含项目名、扫描分类、项目工件、checks 结果和下一步。

`events.jsonl`
逐行 JSON 事件日志，适合后续接入 CI、观测系统或更完整的 Agent Runtime。

## 当前边界

- 当前版本是本地确定性 harness，不会自动调用外部 LLM。
- 当前不会自动修改代码。
- 当前不会自动创建 PR。
- 当前重点是项目扫描、检查执行、报告生成、事件记录和轻量评测。

## 后续方向

- 增加 checkpoint 和 cancel，让长任务可中断、可恢复。
- 增加工具注册表，让业务工具有明确参数契约。
- 接入 LLM provider，把扫描结果和 checks 结果交给模型做更深入分析。
- 增加多 Agent 审查流程，例如 planner、executor、verifier 分工。
- 增加 CI 示例，让每次提交都生成 harness 报告。

## 项目定位

可以这样描述：

```text
Agent Harness Lab 是一个面向真实项目的 TDD-first Agent Harness。它可以扫描本地代码库，读取任务说明，执行项目配置的测试或构建检查，生成 Markdown 报告、JSON 结果和 JSONL 事件日志，用于让 Agent 工作流具备可复现、可评测和可复盘的工程基础。
```

适合的项目场景：

- 长上下文代码库分析前的项目扫描。
- 多轮任务拆解和验证。
- 工具调用结果摘要和审计。
- 自动化测试和修复循环前的基线检查。
- 多 Agent 协作审查前的上下文整理。
