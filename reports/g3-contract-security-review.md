# G3 契约与安全评审记录

- 状态：Accepted
- 适用范围：D11–D13 契约与安全关卡
- 所有者：ArchGuard 项目所有者
- 依赖决策：G2 架构边界、D11 Scanner 契约、D12 结果与 Rule 模型、D13 不可信 Repository 安全
- 最后评审：2026-09-09
- 取代/被取代：无

## 本文解决的问题

本文记录 G3 是否接受 Platform 与 Scanner 的公共契约语义、结果与 Rule 模型，以及不可信 Repository 的默认安全边界。它是进入 G4 V1 可开发性设计的关卡证据，不替代 D11–D13，也不表示机器 Schema、运行时、安全基础设施或产品能力已经交付。

## 当前事实

- G1 已接受长期产品定位、V1 Java/Spring 范围、支持状态和 V1–V5 优先级。
- G2 已接受 Platform、Scanner、Analyzer Registry、Analyzer、七仓库和运行进程的职责边界。
- 当前仍只有治理与文档能力，没有 ScanRequest/ScanResult Schema、Scanner 制品、Platform 持久化实现或安全运行环境。
- D11–D13 已分别给出公共字段语义、确定性结果模型和默认拒绝安全策略。
- 项目所有者于 2026-09-09 要求先审阅并确认 G3，再提交、推送并创建 PR。
- G4 V1 可开发性尚未通过。

## 评审输入

| 切片 | 规范文档 | 评审问题 | 评审结果 |
|---|---|---|---|
| D11 | [Scanner 版本化契约](../architecture/scan-contract.md) | 请求、结果、版本、幂等、取消、错误和部分成功是否具有唯一跨进程语义？ | Accepted |
| D12 | [结果与 Rule 模型](../architecture/result-rule-model.md) | Fact、Finding、Evidence、Diagnostic、Policy 和 Rule 的结构、身份、引用与所有权是否清楚？ | Accepted |
| D13 | [不可信 Repository 安全](../architecture/untrusted-repository-security.md) | 输入、路径、进程、网络、凭据、输出、清理和保留是否默认拒绝且责任明确？ | Accepted |
| ADR-0001 | [独立版本化契约](../adr/0001-versioned-scanner-contract.md) | 是否采用严格 JSON Schema 契约而不复用 Platform 内部模型？ | Accepted |
| ADR-0002 | [确定性 Rule 执行](../adr/0002-deterministic-rule-execution.md) | Rule 执行、Analyzer 领域知识和 Platform Policy 的所有权是否唯一？ | Accepted |
| ADR-0003 | [Repository 默认拒绝](../adr/0003-untrusted-repository-default-deny.md) | V1 是否禁止目标代码执行并隔离获取与分析权限？ | Accepted |

## 一致性检查

| 检查项 | 结论 |
|---|---|
| 与 G1 V1 范围一致 | 没有把字节码、Gradle、PR、MCP、AI 或多技术栈能力提升为 V1 必选 |
| 与 G2 边界一致 | Scanner 不读取 Platform 数据库或内部类，Platform 不执行 Analyzer/Rule，实现边界保持独立 |
| 当前与目标状态分离 | 文档只接受规范语义，没有宣称 Schema、SDK、Scanner、Platform、容器或安全控制已经实现 |
| 契约兼容性闭合 | 首版为严格 JSON Schema Draft 2020-12 `0.1.0`，`0.MINOR` 为兼容线，未知内容失败关闭 |
| 执行状态闭合 | `SUCCEEDED/PARTIAL/FAILED/CANCELLED`、Capability 状态、截断、清理失败和取消竞态均有唯一处理规则 |
| 身份与引用闭合 | scan/request/attempt 身份分离；结果 ID、fingerprint、排序、去重和悬空引用失败均有确定规则 |
| Rule 所有权唯一 | Scanner runtime 统一执行，Analyzer 提供确定性 Fact/Rule，Platform 只拥有 Policy 生命周期和快照 |
| LLM 边界保持 | LLM 不能生成确定性 Fact/Finding、注册或执行 Rule，也不能改变 severity 或合并门禁 |
| 不可信输入默认拒绝 | Repository 不能触发构建、脚本、插件、子模块、LFS、网络或任意命令，分析阶段无凭据和外联 |
| 数据最小化闭合 | Evidence 不含源码片段，日志不含源码/凭据/主机路径，跨边界只输出引用闭合的最小结果 |
| 资源与清理闭合 | 生产无有限硬上限则拒绝就绪；工作区正常立即清理，失败隔离且须在 24 小时内补偿 |
| 后续交付有去向 | D14 冻结 V1 能力，M4/M5 交付机器 Schema、实现与运行控制，Deploy 固定资源和网络配置 |

## 评审结论

G3 通过。D11–D13 与 ADR-0001–ADR-0003 状态统一为 Accepted，允许进入 G4 V1 可开发性设计。

G3 冻结公共契约语义、确定性结果与 Rule 所有权，以及不可信 Repository 的安全默认值；不冻结 V1 输入类型和 Capability 清单、具体 Rule/Fact kind、机器文件组织、传输协议、技术组件或资源数值。

## 已接受决策

### 1. Scanner 公共契约

- Scanner 拥有独立 JSON Schema Draft 2020-12 机器制品，Docs 拥有规范语义，Platform 只消费公开契约。
- 首个目标版本为 `0.1.0`；`0.MINOR` 表示兼容线，PATCH 不改变字段、枚举或语义。
- `scanId` 标识业务 Scan，`requestId` 标识幂等调用，`attempt` 标识执行尝试。
- 请求携带不可变输入、Capability、PolicySnapshot 和全部有限预算，不携带 Platform 内部键或凭据。
- Finding 不决定执行成功；部分能力、截断和可验证的清理失败通过 `PARTIAL` 显式表达。

### 2. 结果与 Rule

- Fact 是确定性观察，Finding 是 Rule 结论，Evidence 是最小可验证依据，Diagnostic 是执行问题；四者不能互相冒充。
- Evidence `0.1.0` 不保存源码片段，公共路径只能是输入根内的规范相对路径。
- Scanner Rule Executor 统一负责快照校验、计划、预算、排序和结果校验；Analyzer 能力模块提供 Fact 抽取与能力特定 Rule。
- Platform 管理 Policy 生命周期和业务处置状态，不访问 Analyzer 私有模型，也不生成确定性 Finding。
- ID 使用 RFC 8785 规范 JSON 的 SHA-256；findingId 定位当前结果，fingerprint 关联跨 revision 问题。

### 3. 不可信 Repository

- Repository 永远是不可信数据；V1 不执行其中的构建、脚本、插件、任务、动态 Analyzer 或任意命令。
- 输入获取阶段只开放 allowlist 网络和短期只读凭据；验证与分析阶段无网络、无凭据且输入只读。
- Git、归档和受管目录都必须验证不可变身份、摘要、路径、类型、大小和任务根边界。
- Scanner 以非 root、无特权、无容器 socket 和有限资源运行；请求只能收紧部署硬上限。
- 工作区正常立即清理；失败时进入独立隔离区，24 小时内补偿，超期升级安全事件并停止受影响 worker 接收新任务。

## 对 G1/G2 的约束检查

- 没有扩大 V1 产品流程或技术栈范围。
- 没有让 Scanner 访问 Platform 数据库、业务授权或 Policy 生命周期。
- 没有把 Registry 拆成独立服务，也没有允许 Repository 提供可执行 Analyzer。
- 没有让 Platform、Gateway、Samples、Evals 或 Deploy 成为 Scanner 契约语义的第二事实来源。
- 没有选择 Broker、Schema Registry、容器厂商、Git 库、Secret Manager、SCA 厂商或云平台。

## 开放问题及去向

| 开放问题 | 后续所有者或关卡 |
|---|---|
| V1 启用的 InputReference、Capability、Java/Spring/Maven 版本和首批 Rule | G4：D14 Feature Spec |
| 需求—架构—里程碑追踪和开发阶段入口 | G4：D15–D16 |
| `0.1.0` JSON Schema 文件、示例、黄金向量、代码生成和兼容测试工具 | M4 Scanner Technical Design |
| Rule Executor、Fact Schema、Registry 接口和 Analyzer 模块代码组织 | M4 Scanner Technical Design |
| 初始文件、字节、时间、内存、进程和输出限制数值 | M4 基线与 Deploy 配置 |
| 首个传输适配器、输入适配器、取消实现和安全隔离组件 | M5 集成设计与对应 ADR |
| 24 小时清理补偿、worker 隔离和安全事件处置 | M5 Runbook 与 Deploy 演练 |
| Platform 结果、安全审计、模型数据和备份的产品保留时长 | D14 与运行规范 |

这些问题均有明确后续边界，不改变 G3 对契约语义、所有权和默认安全策略的结论。

## 非目标

- 不在本记录复制 D11–D13 的全部字段表、状态矩阵和安全控制。
- 不创建 JSON Schema、SDK、业务代码、数据库迁移、容器、凭据或网络策略。
- 不宣称 G4、M1 或任何产品版本已经完成。
- 不用评审结论替代 Feature Spec、Technical Design、自动化契约测试、安全测试或运行演练。

## 验收证据

- D11–D13 均包含状态、范围、当前事实、候选决策、非目标、开放问题和验收证据。
- 三份文档分别覆盖契约封装、结果/Rule 语义和运行安全，没有建立冲突的事实来源。
- ADR-0001–ADR-0003 分别记录契约、Rule 和安全选择及备选方案、风险、验证与重评条件。
- G3 决策逐项保持 G1 产品范围和 G2 进程/仓库边界，并把实现选择路由至 G4、M4、M5 与 Deploy。
- Markdown 相对链接、文档结构、空白、YAML 和高置信 Secret 模式纳入本地检查。

## 变更与取代规则

- D11–D13 的 Accepted 结论可以增加示例和实现链接，但不得原地反转严格版本化、确定性 Rule 或默认拒绝原则。
- 新字段、枚举、错误码或 ID 语义必须按 D11 兼容线演进；机器 Schema 与本文冲突时以已接受规范语义为准并阻止发布。
- 若未来需要目标代码执行、动态插件、Analyzer 外联、源码片段跨边界或更长工作区保留，必须新增安全 ADR 和 G3 级复审说明取代关系。
- G4 可以选择 V1 能力和验收标准，但不得通过 Feature Spec 绕过 G3 的契约、确定性和安全边界。
