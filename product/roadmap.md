# ArchGuard 阶段化产品路线图

- 状态：Accepted
- 规划周期：9～12 个月
- 生效日期：2026-09-09
- 决策依据：[ADR-0006](../adr/0006-java-first-phased-delivery.md)
- 唯一阶段体系：阶段 0–7

## 当前基线

- 七个仓库的 README、贡献指南、Issue/PR 模板、基础 CI 和统一 Apache-2.0 许可证均已合入 `main`，合并后的托管 CI 全部成功；阶段 0 已关闭。
- `archguard-platform` 已提前实现 Java 21/Spring Boot 模块化单体、Project/OIDC、Flyway/PostgreSQL、统一错误、traceId、审计和相关测试。该成果保留为阶段 2 预实现资产。
- `archguard-scanner` S1–S7、三个项目样例、三个失败夹具、黄金/重复性/性能门禁和 `v0.2.0` Release 已通过托管 CI 与[阶段验收](../reports/2026-09-19-scanner-v0.2.0-acceptance.md)；阶段 1 已关闭。
- `archguard-platform`、`archguard-scanner`、`archguard-web` 和 `archguard-deploy` 已完成阶段 2 发布与[阶段验收](../reports/2026-09-22-platform-v0.3.0-acceptance.md)；阶段 2 已关闭。
- 阶段 3 的 3A–3H 已完成，Platform、Web 和 Deploy 发布及[阶段验收](../reports/2026-09-27-governance-v0.4.0-acceptance.md)通过；PR 修订差异按 [ADR-0009](../adr/0009-pr-revision-delta.md) 独立于基线门禁。
- 阶段 4 的 4A–4G 合成范围完成，4H 合成 Compose、固定候选矩阵及本地旧应用回滚/恢复已验证；[ADR-0012](../adr/0012-personal-deepseek-release-scope.md)接受个人自用版范围，[Agent Feature Spec](../requirements/agent-v0.5-feature-spec.md)仍要求获批合成真实调用、制品和唯一退出报告。真实出口及 Project 启用未完成，模型继续关闭；ADR-0010/0011 的技术防护和企业/客户严格审批保留。Gateway/Evals 未启用。

## 路线图

| 阶段 | 时间 | 版本 | 主要仓库 | 可独立演示的结果 | 当前状态 |
|---|---:|---|---|---|---|
| 0 工程治理基础 | 2 周 | `v0.1.0-foundation` | 全部，Docs 主导 | 七仓库工程标准、治理和文档导航 | 已关闭；七仓库 `main` CI 成功 |
| 1 Java Scanner MVP | 6～8 周 | `v0.2.0-scanner` | Scanner、Samples、Docs | 本地 CLI 扫描三个 Java 样例并输出稳定 JSON | 已关闭；`v0.2.0` Release 与阶段验收通过 |
| 2 治理平台 MVP | 8～10 周 | `v0.3.0-platform` | Platform、Scanner、Web、Deploy、Docs | 登录并创建项目/规则集/任务，查看和处置结果 | 已关闭；`v0.3.0` 发布与阶段验收通过 |
| 3 持续治理闭环 | 6～8 周 | `v0.4.0-governance` | Platform、Web、Samples、Deploy、Docs；Scanner 条件参与 | 错误依赖使 CI 失败，修复后通过 | 已关闭；版本发布与阶段验收通过 |
| 4 Java Agent 增强 | 6～8 周 | `v0.5.0-agent` | Platform、Web、Samples、Deploy、Docs；Scanner 仅提供已发布事实 | 个人自用版：引用证据生成解释、摘要和低风险建议 | ADR-0012 范围已接受；4A–4G 合成完成，4H 真实验收/发布/退出未完成 |
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

- GitHub PR 的 CI 在自己的工作区运行 Scanner 并向 Platform 提交报告和 Git 元数据；Platform 不持有 Git 凭据或克隆源码。
- 不可变基线按 Project、Repository、目标分支和 RuleSetVersion 隔离，`NEW`、`EXISTING`、`RESOLVED` 分类稳定且不依赖行号。
- 默认只有未被有效例外覆盖的新增 `high`/`critical` Finding 阻断；门禁 `PASS`、`FAIL`、`ERROR` 与 CI `0/2/64/70` 映射明确。
- Webhook、报告提交、基线、例外、门禁和治理操作满足签名、防重放、幂等、乱序保护、权限隔离和审计要求。
- PR 修订差异以已验签的前后 head 为参考，可把新引入又修复的问题展示为 `RESOLVED`；它与基线门禁分类分离，不能改变 CI 结果。

### 阶段 4：`v0.5.0-agent`

- 用户在 Web 中显式请求单个 Finding 解释或所选 Finding 摘要；后台事件不隐式触发模型。
- Agent 输出含结论、规则依据、可验证引用、低风险建议、Platform 计算的证据覆盖等级、状态、traceId、模型、Prompt 和 Schema 版本。
- 引用只解析到获授权的真实 Evidence 或不可变项目文档版本；输出经过 Schema、Project 权限、引用和业务校验，无法验证的内容不展示为事实。
- Maintainer 显式上传的 Markdown/纯文本文档按 Project 隔离和不可变版本管理；初版复用 PostgreSQL 有界检索，不引入向量数据库或 Platform 侧 Git clone。
- 个人自用、本地部署和个人官方账户范围按 ADR-0012 冻结；模型默认关闭，满足有效风险/启用记录、最小外发、后端 Secret、Project 授权、Token/延迟/费用硬上限及单独运行授权。CI 使用假模型/假 HTTP，真实验收只发送合成数据并核对提供方实际用量。
- 模型不可用、超时、输出无效、引用不实、越权或额度耗尽均明确失败；不改变 Finding、基线、门禁或 CI 退出码，不自动修改代码、PR、规则或例外。
- 真实适配器、默认关闭双开关、Web 解释/摘要/引用闭环和最终候选回滚通过，相关 PR/main CI 成功，发布个人版制品并合入唯一阶段报告后才关闭阶段。报告不得宣称零保留、账户级供应商审批或企业/客户/生产验收通过；延期严格条件可追溯。

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
- 若启用企业/客户数据、多人或公网服务，先重新评审个人范围，满足 ADR-0010/0011 的严格账户级数据处理关卡；阶段 4 个人版完成不代表这些条件已满足。
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
