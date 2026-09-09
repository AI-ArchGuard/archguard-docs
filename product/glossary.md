# ArchGuard 术语表

- 状态：Accepted
- 适用范围：产品、需求、架构、契约和用户界面的公共术语
- 所有者：ArchGuard 项目所有者
- 依赖决策：M0 仓库与治理基线
- 最后评审：2026-09-09（同步 G2 架构边界；G1 术语结论不变）
- 取代/被取代：无

## 本文解决的问题

本文为 ArchGuard 的核心名词规定唯一含义，防止产品能力、实现组件和结果类型混用。Registry、Analyzer 和进程所有权由 G2 架构文档定义；字段级 Schema、Rule 职责和执行安全由 G3 切片定义。

## 当前事实

- 现有阶段提示词使用了 Scan、Violation、Rule、ADR 和 Tool 等词，但尚无冻结的公共数据模型。
- 当前没有已实现的 Scanner 或 Analyzer；下列定义用于规范后续文档，不代表能力已经交付。

## 规范术语

| 术语 | 规范含义 | 不表示什么 |
|---|---|---|
| ArchGuard | 面向多技术栈、V1 聚焦 Java/Spring 的软件架构治理平台。 | 当前已经支持多个技术栈。 |
| Platform | 管理项目、仓库、策略、扫描任务、结果、权限和审计等治理状态的产品能力集合。 | 源码解析器或某个 Analyzer。 |
| Project | ArchGuard 中的治理边界，聚合仓库、策略、成员和结果。 | Git 托管平台中的仓库。 |
| Repository | 登记到 Project 下、可被授权分析的版本控制代码库。 | ArchGuard 的七个实现仓库之一；语境不清时必须写全称。 |
| Scan | 对一个明确输入版本、配置和资源边界进行的一次分析执行。 | 持续监控、任意构建或无限制代码执行。 |
| Scanner | 承载受控分析执行、协调一个或多个 Analyzer 并产出扫描结果的分析运行时边界。 | 单个语言解析器、单条 Rule 或 Platform 的业务状态机。 |
| Analyzer | 声明一组能力并把特定输入转换为 Fact、Finding 或 Diagnostic 的分析单元。 | 未经声明即可动态加载和执行的任意插件。 |
| Capability | Analyzer 或产品边界明确声明、配置和验证的一项能力。 | 路线图中出现即视为已支持。 |
| Fact | 从目标输入中确定性提取、可由 Evidence 验证的观察结果，例如“A 依赖 B”。 | 对合规与否的判断。 |
| Rule | 对 Fact 或其关系施加的、可重复求值的架构约束或策略。 | LLM 的主观建议或一次执行错误。 |
| Finding | Rule 求值后形成的架构结论，包含规则身份、严重性、影响对象和 Evidence。 | 解析失败、超时或运行时故障。 |
| Evidence | 支撑 Fact 或 Finding 的最小可验证依据，例如规范化路径、符号、位置、边或摘要标识。 | 默认保存完整源码、凭据或无关上下文。 |
| Diagnostic | 描述输入、配置、解析或执行问题的诊断信息。 | Rule 被违反的业务结论。 |
| Policy | 某个治理范围内启用哪些 Rule、参数和严重性的配置。 | Rule 的解析或执行代码。 |
| Result | 一次 Scan 的总体输出封装；可以包含 Fact、Finding、Diagnostic、统计和状态。 | Scan 必然全部成功。 |
| ADR | 对一个重要架构选择及其背景、替代方案、影响和替代关系的不可变决策记录。 | 可直接覆盖已接受结论的普通说明文档。 |

## 推荐表达

- 使用“Finding”作为规范结果名；“Violation”只用于描述某个 Finding 的判定结果，不建立第二套结果模型。
- 使用“当前已支持”表示实现和验收证据已经存在；使用“V1–V4 目标”或“后续候选”描述规划。
- 使用“V1 增强项”表示希望在 V1 周期内交付、但不构成 V1 发布门槛的能力。
- 需要指代代码仓库时写“Repository”；需要指代七仓库工程时写具体仓库名，例如 `archguard-scanner`。
- 需要指代一次执行时写“Scan”；需要指代分析运行时边界时写“Scanner”。

## 示例

假设 Java 类 `OrderService` 依赖 `JdbcOrderRepository`：

- Fact：`OrderService` 依赖 `JdbcOrderRepository`。
- Evidence：两个符号的规范名称、依赖类型及最小源码位置。
- Rule：应用层不得直接依赖基础设施层。
- Finding：该依赖违反上述 Rule，严重性按当前 Policy 计算。
- Diagnostic：某个源文件无法解析；它不自动等于 Finding。

## 目标状态

- 产品、需求、架构、ADR、契约、API 和测试统一使用本表术语。
- 新术语必须说明与现有概念的关系，避免为同一概念建立同义模型。
- 字段级定义冻结后，从本文链接到唯一契约，而不复制完整 Schema。

## 非目标

- 不在本文定义 Java 类型、JSON 字段、错误码或序列化格式。
- 不决定 Analyzer Registry、进程边界、插件发现或版本协商机制。
- 不定义 Rule Policy 与 Rule Executor 的最终所有权。

## 已接受决策

- ADR 必须编号、记录状态和替代关系；已接受结论通过新 ADR 取代，不原地改写。
- 确定性 Rule 形成事实基础，LLM 不替代确定性违规判断。

本术语表已在 G1 评审中接受；运行时、Registry、Analyzer 和仓库所有权已由 G2 接受，字段级契约、Rule 职责和执行安全已由 G3 接受。

## 开放问题

- 公共 API 是否继续暴露 `Violation` 兼容名，还是在首个版本只使用 `Finding`？
- Fact 是否对 Platform 可见，还是只在 Scanner 结果中按需公开？
- Evidence 的最小位置粒度和脱敏规则是什么？

这些问题由扫描契约、规则模型和安全设计切片处理。

## 验收证据

- Scanner、Analyzer、Rule、Finding、Evidence、Fact 和 Diagnostic 已给出互不重叠的定义。
- [产品定位](positioning.md)使用本表规范用语。
- [G1 产品边界评审记录](../reports/g1-product-boundary-review.md)确认公共术语可作为后续产品与架构文档的统一口径。
