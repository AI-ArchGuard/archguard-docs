# ArchGuard 阶段化产品路线图

- 状态：Accepted
- 规划周期：9～12 个月
- 生效日期：2026-09-09
- 决策依据：[ADR-0006](../adr/0006-java-first-phased-delivery.md)
- 唯一阶段体系：阶段 0–7

## 当前基线

- 七个仓库的 README、贡献指南、Issue/PR 模板、基础 CI 和统一 Apache-2.0 许可证已在本地准备；除 Docs 外，另外六个仓库的许可证和 CI 变更尚未提交，阶段 0 仍在远端收口。
- `archguard-platform` 已提前实现 Java 21/Spring Boot 模块化单体、Project/OIDC、Flyway/PostgreSQL、统一错误、traceId、审计和相关测试。该成果保留为阶段 2 预实现资产。
- `archguard-scanner` 的 S1 父工程、五模块和边界测试已在本地通过，但尚未提交并由托管 CI 验证；`archguard-samples`、`archguard-mcp-gateway`、`archguard-evals` 和 `archguard-deploy` 仍只有本地工程基线变更。
- 当前主线：按 Docs → Scanner → Platform → Gateway/Evals 顺序完成 Foundation 远端收口。Scanner S2 统一模型和 `0.1.0` JSON Schema 在阶段 0 关卡关闭后启用；Platform 继续冻结功能扩展。

## 路线图

| 阶段 | 时间 | 版本 | 主要仓库 | 可独立演示的结果 | 当前状态 |
|---|---:|---|---|---|---|
| 0 工程治理基础 | 2 周 | `v0.1.0-foundation` | 全部，Docs 主导 | 七仓库工程标准、治理和文档导航 | 远端收口中；六仓库待提交和 CI |
| 1 Java Scanner MVP | 6～8 周 | `v0.2.0-scanner` | Scanner、Samples、Docs | 本地 CLI 扫描三个 Java 样例并输出稳定 JSON | 未正式进入；S1 本地验证完成，S2 被阶段 0 关卡阻断 |
| 2 治理平台 MVP | 8～10 周 | `v0.3.0-platform` | Platform、Scanner、Deploy、Docs | 创建项目/规则集/任务并查看和处置结果 | Platform 有预实现资产，未进入正式集成 |
| 3 持续治理闭环 | 6～8 周 | `v0.4.0-governance` | Platform、Scanner、Samples、Deploy、Docs | 错误依赖使 CI 失败，修复后通过 | 未启用 |
| 4 Java Agent 增强 | 6～8 周 | `v0.5.0-agent` | Platform、Scanner、Docs | 引用证据生成解释、摘要和修复建议 | 未启用 |
| 5 Go MCP Gateway | 4～6 周 | `v0.6.0-mcp` | Gateway、Platform、Deploy | 受控工具调用具备权限、限流、取消和审计 | 未启用 |
| 6 Python Evals | 5～7 周 | `v0.7.0-evals` | Evals、Samples、Docs | 一条命令比较候选/基线并生成 JSON/HTML 报告 | 未启用 |
| 7 生产化与多语言 | 4～8 周 | `v1.0.0` | 全部按需启用 | 可部署、可观测、可恢复，并接入首个有需求证据的新语言 | 未启用 |

各阶段允许文档设计与前一阶段收尾小幅重叠，但功能实现只有在前一阶段退出证据齐全后才进入。任何阶段都必须能够单独发布和演示。

## 阶段退出关卡

### 阶段 0：`v0.1.0-foundation`

- 七仓库都有 README、LICENSE、贡献指南、Issue/PR 模板和基本 CI。
- 产品愿景、范围、版本、API、错误、日志/trace、测试、数据库、DoD 和跨仓库兼容规则有唯一入口。
- 仓库职责没有重叠，生产者契约所有权明确。

### 阶段 1：`v0.2.0-scanner`

- CLI 支持 `archguard scan <path> --rules <file> --output <file>`。
- `scanner-domain`、`scanner-parser-java`、`scanner-rule-engine`、`scanner-report`、`scanner-cli` 边界通过架构测试。
- 至少三个 Java 合成样例覆盖正常、违规、循环和失败场景。
- 每个 Finding 都有 Rule、位置和 Evidence；同一输入重复扫描结果稳定。
- Scanner 完全独立于 Platform 运行，并发布版本化语言无关契约。

### 阶段 2：`v0.3.0-platform`

- 创建 Project、RuleSet、ScanJob、查询状态/结果、误报/风险接受和历史查询形成闭环。
- Platform 通过公开 Scanner 契约集成，不导入 Scanner 内部类。
- PostgreSQL 迁移、鉴权、审计、结构化日志和一键 Compose 启动可验证。

### 阶段 3：`v0.4.0-governance`

- Git/PR 增量扫描、基线、忽略到期、质量门禁、Webhook、CI 退出码、趋势和规则版本可用。
- 新问题与历史问题区分稳定；扫描失败与规则违规使用不同退出码。
- 规则、基线、忽略和治理操作全部可审计。

### 阶段 4：`v0.5.0-agent`

- Agent 输出含结论、规则依据、代码证据、建议、置信度、模型和 Prompt 版本。
- 输出经过 Schema、权限和业务校验；模型不可用不影响确定性扫描。
- 调用具备 traceId、Token、延迟和费用统计；不自动修改代码或规则。

### 阶段 5：`v0.6.0-mcp`

- Java Agent 不再直接调用已纳入目录的内部工具实现。
- 每个工具有独立权限、严格参数、超时、限流、取消和审计。
- Gateway 不直连 Platform 数据库，也不复制业务逻辑。

### 阶段 6：`v0.7.0-evals`

- 版本化数据集覆盖解释、引用、工具、RAG、注入、授权和回归。
- 一条命令运行完整评估并生成 JSON/HTML；支持基线与候选比较。
- 安全测试进入 CI，模型或 Prompt 变更必须通过回归。

### 阶段 7：`v1.0.0`

- 镜像、多环境、HTTPS、Secret、备份、健康、优雅停机、OpenTelemetry、告警、恢复和自动发布有证据。
- 先完成 Compose 和单机云演示，再基于容量证据决定 Kubernetes。
- 首个新语言扫描器把语言结构转换为统一模型；控制面无需认识语言 AST。

## 跨仓库兼容顺序

1. Docs 接受 Feature Spec、契约语义和 ADR。
2. Samples 增加不依赖实现的固定输入、预期输出和 digest。
3. Scanner 发布 Schema、规则、CLI 和提供方测试。
4. Platform 更新消费方测试，再启用真实适配器。
5. Gateway 只消费已发布 Platform API；Evals 只评估已发布黑盒契约。
6. Deploy 最后记录已验证的制品组合、发布顺序和回滚步骤。

破坏性 Scanner 契约变化使用新的 `0.MINOR` 兼容线并并行迁移。正常发布按内部提供方到入口消费方推进；回滚先关闭入口功能或切回 Platform 消费线，再回退 Scanner/Gateway 制品。已发布 Flyway 迁移不回写。

## 技术引入门槛

- Kafka：只有数据库任务表经可靠性测试证明无法满足需求时评审。
- Kubernetes：只有 Compose/单机部署出现可测量的容量、隔离或恢复需求时评审。
- 微服务：只有模块出现独立扩缩、团队、发布或合规边界时评审。
- Service Mesh：只有多服务通信治理问题真实存在且现有控制不足时评审。
- 新语言：必须有用户需求、独立 Feature Spec、样例、规则、黄金测试和兼容报告。
