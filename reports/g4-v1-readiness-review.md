# G4 V1 可开发性评审记录

- 状态：Accepted
- 适用范围：D14–D16 V1 可开发性关卡
- 所有者：ArchGuard 项目所有者
- 依赖决策：G1 产品边界、G2 架构边界、G3 契约与安全
- 跟踪 Issue：[Docs #8](https://github.com/AI-ArchGuard/archguard-docs/issues/8)、[Docs #9](https://github.com/AI-ArchGuard/archguard-docs/issues/9)、[Docs #10](https://github.com/AI-ArchGuard/archguard-docs/issues/10)
- 最后评审：2026-09-09
- 取代/被取代：无

## 本文解决的问题

本文记录 V1 Java/Spring 目标是否已经具备可开发、可验收、可追踪的唯一边界，以及 M2–M5 是否具备清晰的阶段入口。它不替代 D14–D16，也不表示 Platform、Scanner、Schema、Samples 或任何产品能力已经交付。

## 当前事实

- G1–G3 已分别接受产品、架构、契约和安全边界。
- 当前仍只有治理和文档证据，没有可运行 Platform、Scanner、Analyzer、机器 Schema 或端到端流程。
- D14 定义 13 项功能需求和 8 项非功能需求，D15 为全部 21 项需求提供一对一验收场景，D16 完成一对一交付追踪。
- D14–D16 的跟踪 Issue 已创建，本评审不使用未开立 Issue 的占位符。
- Platform README 中 Maven Wrapper 的初始化阶段已在独立 `docs/align-m2-platform-skeleton` 分支从 M1 更正为 M2。

## 评审输入

| 切片或决策 | 文档 | 评审问题 | 评审结果 |
|---|---|---|---|
| D14 | [V1 Java/Spring Feature Spec](../requirements/v1-java-spring-feature-spec.md) | 用户闭环、版本、输入、Capability、Fact、Rule、需求和非目标是否没有阻断歧义？ | Ready |
| D15 | [V1 验收矩阵](../requirements/v1-acceptance-matrix.md) | 每项需求是否有可定位场景、样例、责任仓库和证据类型？ | Accepted |
| D16 | [V1 交付追踪与阶段入口](../requirements/v1-delivery-traceability.md) | 需求是否可双向追踪，M2–M5 的入口、交付和退出是否可独立判断？ | Accepted |
| ADR-0004 | [Platform 模块化单体](../adr/0004-platform-modular-monolith.md) | 单体选择、模块所有权、Scanner 隔离和重评条件是否明确？ | Accepted |
| ADR-0005 | [PostgreSQL 业务事实来源](../adr/0005-postgresql-business-source-of-truth.md) | 数据所有权、迁移、事务、访问和辅助存储边界是否明确？ | Accepted |
| 跨仓库同步 | Platform README | Maven Wrapper 是否与路线图的 M2 骨架阶段一致？ | Accepted，待独立 PR 合并 |

## 一致性检查

| 检查项 | 结论 |
|---|---|
| 与 G1 产品边界一致 | V1 只保留 Java/Spring 主路径和 Maven 只读静态元数据；字节码、Gradle、PR、MCP、AI 和多技术栈没有被提升为必选 |
| 与 G2 架构边界一致 | Platform 继续是模块化单体，Scanner 是独立进程，Registry/Analyzer 在 Scanner 内，七仓库职责不变 |
| 与 G3 契约与安全一致 | `content-archive` 只提供不可变输入；不执行目标代码、不访问分析网络、不越过版本化契约，Finding 仍只由确定性 Rule 产生 |
| 兼容范围可判定 | Java 17/21、Boot 3.4.x/3.5.x、Framework 6.2.x、Maven POM 4.0.0 与不支持行为均已冻结 |
| 能力边界可判定 | 4 个 Capability、7 类公共 Fact 和 4 条首批 Rule 有稳定 ID、最小覆盖和明确限制 |
| 需求覆盖闭合 | 21/21 个 D14 需求各有唯一 D15 场景，并在 D16 映射到架构、仓库和里程碑；无空白或重复需求 ID |
| 当前与目标分离 | 所有验收场景仍为“计划”，支持矩阵仍为“未支持/V1 目标”，未把文档或 Issue 冒充实现证据 |
| 阶段声明可判定 | M2 只能声称 Platform 骨架，M3 的 Fake 不等于真分析，M4 不等于真集成，M5 不等于发布级“已支持” |
| 开放问题有去向 | API/表结构在 M2/M3，parser/Schema/资源基线在 M4，传输/隔离在 M5，发布、性能和最终审计在 M11–M13 |

## 评审结论

G4 通过。D14 状态为 Ready，D15–D16 与 ADR-0004–ADR-0005 状态为 Accepted。M1 文档关卡完成，允许在 M2 Issue 和 Technical Design 评审后开始 Platform 骨架。

为保持跨仓库一致，进入 M2 前必须合并 Docs G4 变更和 Platform README 更正，然后从各自最新 `main` 创建实现分支。本结论不授权绕过各阶段 Issue、Technical Design、测试和 PR。

## 已接受决策

- V1 生产输入只启用 `content-archive`，以 SHA-256 digest 作为不可变输入身份。
- V1 只支持 Java 17/21、Spring Boot 3.4.x/3.5.x、Spring Framework 6.2.x 和 Maven POM 4.0.0 的明确静态子集。
- V1 必须交付 `java.source-structure`、`java.type-dependencies`、`spring.component-model` 和 `maven.project-model`。
- 首批确定性 Rule 为禁止依赖、包循环、Spring 字段注入和 Maven 禁止依赖。
- Platform 初期为一个 Java/Spring Boot 模块化单体，领域所有权和跨模块公开边界必须可自动验证。
- PostgreSQL 是 Platform 业务事实的唯一持久来源，只能由 Platform 适配器访问，Schema 只通过不可改写的 Flyway 迁移演进。

## 开放问题及去向

| 开放问题 | 后续所有者或关卡 |
|---|---|
| Platform 的具体模块名、API、角色、表与初始迁移 | M2/M3 Technical Design |
| Java/Spring/Maven parser、代码模块、机器 Schema、Rule 参数 Schema 和初始资源值 | M4 Technical Design 与基线 |
| Platform–Scanner 首个传输适配器、安全隔离组件、取消与补偿机制 | M5 Technical Design 与 Deploy |
| Platform 业务结果/审计保留、备份恢复与回滚参数 | M11 Runbook 与演练 |
| 小/中样例规模、性能回归阈值和产品体验基线 | M4/M5 首次测量、M12 接受 |

上述问题不改变 V1 的用户、输入、版本、Capability、Rule、安全或数据边界，因此不阻断 G4；它们分别阻断对应工程阶段的入口或退出。

## 非目标

- 不在 G4 选择 parser、Web/UI 框架、传输协议、容器厂商、云服务或性能 SLO。
- 不创建机器 Schema、SDK、业务代码、数据库迁移、样例或运行时制品。
- 不把 Java 25、Boot 4、远程 Git、字节码、Gradle、PR、MCP 或 AI 静默纳入 V1。
- 不把本评审作为 V1 “已支持”或可发布的证据。

## 验收证据

- D14 的 21 个需求 ID 在 D15 和 D16 各出现一次主映射，责任仓库与里程碑非空。
- D15 覆盖正常、违规、不支持、恶意、超限、取消、恢复、确定性、授权和清理路径。
- ADR-0004/0005 包含背景、选择、备选方案、影响、验证与重评条件，不复制实现细节。
- Docs 和 Platform 变更保持独立分支；进入 M2 前按 Docs 决策→Platform 口径→最新 `main` 实现分支的顺序同步。
- Markdown 链接、结构、空白、覆盖计数和高置信 Secret 模式纳入本地检查；YAML 未改动。

## 变更与取代规则

- 改变 V1 目标用户、生产输入、技术版本、Capability、Rule、信任边界或发布门禁时，必须重新执行 G4 级评审。
- 反转模块化单体或 PostgreSQL 事实来源时，必须用新 ADR 记录迁移、兼容和回滚，并明确取代关系。
- 实现可以在不改变已接受语义的前提下增加证据链接；机器 Schema 或运行行为与本关卡冲突时必须阻止阶段退出。
