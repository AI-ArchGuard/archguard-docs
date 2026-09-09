# ArchGuard 容器与平面

- 状态：Accepted
- 生效日期：2026-09-09
- 决策依据：[ADR-0004](../adr/0004-platform-modular-monolith.md)、[ADR-0005](../adr/0005-postgresql-business-source-of-truth.md)、[ADR-0006](../adr/0006-java-first-phased-delivery.md)

| 平面/容器 | 部署边界 | 数据所有权 | 启用阶段 |
|---|---|---|---|
| Platform | Java/Spring Boot 模块化单体 | PostgreSQL 中的业务事实 | 2 |
| Scanner | 独立 Java CLI/进程/容器 | 默认无业务持久状态，只有有界工作区 | 1；阶段 2 接入 Platform |
| Agent/RAG | Platform 的应用编排与可替换模型适配器 | 建议、Prompt/模型版本和必要审计 | 4 |
| MCP Gateway | 独立 Go 进程 | 最小可重建配置和调用审计，不拥有业务事实 | 5 |
| Evals | 独立 Python 离线运行器 | 版本化数据集、评分器和报告 | 6 |
| PostgreSQL | Platform 私有数据存储 | Project、RuleSet、ScanJob、Finding、基线和审计 | 2 |
| Deploy/Observability | Compose/云环境和遥测系统 | 配置引用、兼容矩阵、指标和恢复证据 | 2 起，7 完成 |

## 允许通信

- 用户/CI → Platform：版本化 REST；阶段 3 增加 Git/PR/Webhook。
- Platform → Scanner：版本化 Scan Request/Result，超时、取消和幂等明确。
- Platform → 模型：阶段 4 的最小必要证据，经授权和输出校验。
- Platform → Gateway：阶段 5 的 Agent 工具调用；Gateway 再访问公开 Platform/外部工具边界。
- Evals → Platform/Gateway：阶段 6 的黑盒测试，不读内部数据库。
- 只有 Platform 基础设施适配器 → PostgreSQL。

## 禁止通信

- Scanner、Gateway、Evals 或外部客户端直连 Platform 数据库。
- Platform 领域层导入 Scanner、数据库、Web 或模型 SDK。
- Gateway 执行业务决策、确定性规则或任意 Shell。
- Evals 成为线上同步或异步请求成功的必要条件。
- Scanner 语言前端默认访问网络、凭据或目标项目可执行内容。
