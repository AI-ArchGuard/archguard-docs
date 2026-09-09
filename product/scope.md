# ArchGuard 范围与仓库职责

- 状态：Accepted
- 生效日期：2026-09-09
- 决策依据：[产品愿景](vision.md)、[ADR-0006](../adr/0006-java-first-phased-delivery.md)

## 七个仓库

| 仓库 | 技术栈 | 最终职责 | 首次主要启用阶段 |
|---|---|---|---|
| `archguard-platform` | Java、Spring Boot | 控制中心、项目、规则、任务、Agent 编排和治理结果 | 阶段 2；现有代码是预实现资产 |
| `archguard-scanner` | Java | 代码扫描、依赖分析、确定性规则和统一中间模型 | 阶段 1 |
| `archguard-mcp-gateway` | Go | MCP 工具网关、鉴权、限流、审计、超时和工具注册 | 阶段 5 |
| `archguard-evals` | Python | Agent 评估、安全测试、数据集和回归报告 | 阶段 6；阶段 4 起积累案例 |
| `archguard-samples` | Java、Go、Python | 正确/错误合成示例和稳定测试样本 | 阶段 1 |
| `archguard-deploy` | Docker、CI/CD | 本地/云端部署、监控和基础设施配置 | 阶段 2 起逐步启用，阶段 7 完成 |
| `archguard-docs` | Markdown、OpenAPI、ADR | 需求、架构、接口、规则、部署和演示文档 | 全阶段 |

七个仓库独立版本和发布，不建立跨仓库 `common` 源码包。生产者拥有可执行契约制品，Docs 汇总和发布规范语义，Deploy 记录已验证的制品兼容组合。

## 当前产品范围

阶段 0 已关闭，当前工作目标是完成阶段 1 `v0.2.0-scanner`。S1 构建和五模块边界已完成，下一切片是 S2 统一模型与 `0.1.0` JSON Schema。阶段 1 只承诺本地 Java CLI、统一模型、首批规则、合成样例和稳定 JSON；不承诺 Platform 闭环、Git/PR、Agent、MCP、Python Evals 或生产部署。

## 最终职责边界

- Platform 拥有业务状态、资源归属、权限、任务和用户决策；不解析源码。
- Scanner 拥有分析运行时、语言前端、统一模型、规则执行和扫描契约；不管理用户或业务数据库。
- Gateway 只拥有工具通信与访问控制；不拥有 Project、RuleSet、ScanJob 或 Finding。
- Agent/RAG 是 Platform 编排的智能能力；不能形成确定性 Finding 或绕过 Gateway 使用高风险工具。
- Evals 通过公开 Schema 和黑盒端点评估，不参与线上请求。
- Samples 只包含合成、可公开、稳定的数据，不含真实客户代码。
- Deploy 只组合已发布制品，不复制业务默认值或暴露内部端口。

## 明确非目标

- 为展示技术而提前加入微服务、Kafka、Kubernetes 或 Service Mesh。
- 在统一模型中保存某个解析库的 AST 或 Platform 数据库实体。
- 让 Agent 自动修改代码、合并 PR、修改治理规则或执行任意 Shell。
- 让 Gateway 直接读取 Platform 数据库或复制资源授权逻辑。
- 让 Evals 成为生产请求成功的必要条件。
- 在没有独立需求、样例和验收证据时声称支持新语言。
