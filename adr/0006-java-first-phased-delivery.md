# ADR-0006：采用 Java-first、Scanner-first 的阶段化交付顺序

- 状态：Accepted
- 日期：2026-09-09
- 决策者：ArchGuard 项目所有者
- 取代：此前“Platform 先于 Scanner、MCP/Evals 先于 Agent”的交付顺序
- 保留：ADR-0001 至 ADR-0005 的契约、确定性、安全、模块化单体和数据所有权决策

## 背景

现有路线先建设 Platform，再建设 Scanner，并把 MCP Gateway 与 Evals 放在 Agent 之前。项目所有者重新确认最终定位为“一个 Java-first、语言无关架构、AI 增强的软件架构治理平台”，要求先证明确定性代码分析能力，再建设控制面和持续治理；Agent 先在 Java Platform 内形成稳定用例，随后才把成熟工具访问边界抽离为 Go MCP Gateway，最后把阶段 4 起积累的案例建设成正式 Python 评估体系。

作出本决策时，Platform 已存在可运行的 Project/OIDC 垂直切片，而 Scanner、Samples、Gateway、Evals 和 Deploy 仍处于仓库基线。因此纠偏不能靠删除已有 Platform 成果完成，而应保留其作为阶段 2 预实现资产，冻结进一步扩展，并把当前主线切回 Scanner。

## 决策驱动因素

- 架构治理首先需要可重复的组件、依赖、规则、证据和指标事实。
- Scanner 的公共模型与契约必须天然支持未来 Go、Python、JavaScript 前端，不能泄漏 Java AST 或 Platform DTO。
- 每个阶段必须能独立演示、发布和回滚，不能等待七仓库全部完成。
- Platform 的业务边界仍在变化，初期保持模块化单体。
- Gateway 边界应由真实 Agent 工具用例驱动，不能为了使用 Go 提前造空壳。
- 正式 Evals 依赖相对稳定的 Agent 输出和工具 Schema，但阶段 4 起必须持续保存评估案例。

## 决策

采用以下唯一交付序列：

1. 阶段 0，`v0.1.0-foundation`：七仓库工程治理基础。
2. 阶段 1，`v0.2.0-scanner`：独立 Java Scanner CLI、语言无关模型、确定性规则和合成样例。
3. 阶段 2，`v0.3.0-platform`：Java/Spring Boot 模块化单体控制面和完整手动扫描闭环。
4. 阶段 3，`v0.4.0-governance`：Git/PR/CI、基线、增量问题、门禁、趋势和审计。
5. 阶段 4，`v0.5.0-agent`：基于确定性证据的解释、建议、摘要和 RAG；默认只读。
6. 阶段 5，`v0.6.0-mcp`：把成熟工具访问控制抽离为 Go MCP Gateway。
7. 阶段 6，`v0.7.0-evals`：Python 黑盒评估、安全、回归和基线比较。
8. 阶段 7，`v1.0.0`：生产化和由真实需求驱动的多语言扩展。

阶段按关卡启用，不并行物化七个运行时。Docs 跨阶段持续维护；Samples 在阶段 1 起启用；Deploy 在阶段 2 先提供本地 Compose，并在阶段 7 完成生产化；Evals 在阶段 4 起积累案例，但阶段 6 前不成为正式运行系统。

现有 Platform 代码按以下规则处理：

- 保留源码、迁移、OpenAPI、OIDC、Project、审计和测试，不回退已发布迁移。
- 标记为阶段 2 预实现资产；阶段 1 期间仅允许安全修复、构建修复和文档同步。
- 在 Scanner `v0.2.0` 契约和样例通过阶段 1 退出门禁前，不新增 Repository、RuleSet、ScanJob、Finding 或 Agent 业务能力。
- 阶段 2 开始时重新以当时契约做消费方评审，不假定现有 Platform 设计已经冻结扫描接口。

## 六个最终平面

| 平面 | 实现 | 所有权 |
|---|---|---|
| 控制平面 | Java Platform | 项目、规则、任务、权限、结果和 Agent 编排 |
| 分析平面 | Java Scanner | 语言前端、统一模型、确定性规则和证据 |
| 工具平面 | Go Gateway | MCP、认证、工具权限、限流、超时和审计 |
| 智能平面 | Agent/RAG/LLM | 解释、问答、归纳和低风险修复建议 |
| 质量平面 | Python Evals | 黑盒评估、回归和安全测试 |
| 运维平面 | Deploy | 发布、配置、监控、追踪、备份和恢复 |

## 影响

### 正面影响

- 先获得可演示、可测试、可复用的分析事实基础。
- Platform 只消费公开契约，未来语言前端不会迫使控制面重构。
- Agent、Gateway、Evals 的边界由真实调用和风险证据形成。
- 已完成 Platform 资产得到保留，不用通过破坏性回滚完成路线纠偏。

### 代价与风险

- 已有 Platform 分支会在一段时间内领先于正式路线，状态声明必须非常清楚。
- 过渡计划和实现提示不再作为长期文档保存，唯一执行顺序由本 ADR 和路线图给出。
- 阶段 1 的模型若伪装成语言无关但携带 Java 专属字段，会把耦合推迟到后续暴露，必须用契约测试限制。

## 验证

- 所有入口文档只声明本 ADR 的八阶段顺序。
- Scanner `scanner-domain` 不依赖 Java parser、Spring、数据库和模型 SDK。
- 相同输入、规则和版本至少重复三次，规范输出完全一致。
- 阶段 1 未通过前，Platform 不新增扫描、规则、结果或 Agent 模块。
- 每个阶段都有版本、主要仓库、独立演示、退出证据和回滚边界。

## 何时重新评估

只有真实用户、容量、安全、团队所有权或多语言实现证据证明该顺序阻碍交付时，才能用新 ADR 取代本决策。不得仅为展示微服务、Kafka、Kubernetes、Service Mesh、Go 或 Python 而改序。
