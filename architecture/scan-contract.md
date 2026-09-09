# Scanner 版本化契约

- 状态：Accepted
- 切片：D11
- 适用范围：Platform 与 Scanner 之间的请求、结果、错误、版本、幂等和部分成功语义
- 所有者：`archguard-scanner` 发布机器契约，`archguard-docs` 维护规范语义
- 依赖决策：D08 容器架构、D10 Analyzer 架构和 G2 评审
- 目标契约版本：`0.1.0`
- 最后评审：2026-09-09（G3 契约与安全评审通过）
- 取代/被取代：无

## 本文解决的问题

本文冻结首个 Scanner 跨进程契约应表达哪些字段、如何判断一次执行成功或部分成功，以及提供方和消费方如何兼容升级。M4 在 `archguard-scanner` 中发布 JSON Schema 和测试制品；本文不选择 HTTP、gRPC、命令协议或消息中间件。

## 当前事实

- 当前没有 ScanRequest/ScanResult 代码、Schema、Scanner 制品或跨仓库契约测试。
- Platform 与 Scanner 已由 G2 确认为独立进程，Scanner 不接收 Platform 内部类或数据库权限。
- Platform 先保存业务 Scan，再异步调用 Scanner；业务状态机和重试租约不属于 Scanner 契约。
- V1 输入方式和精确分析能力仍由 D14 Feature Spec 决定，契约只能预留受控输入类型。

## 表达与版本基线

- 机器可验证形式采用 JSON Schema Draft 2020-12，JSON 文本编码固定为 UTF-8。
- 每个请求、结果和可解析错误都包含 `schemaVersion`；首个版本为 `0.1.0`。
- 开发期按 SemVer `0.MINOR.PATCH` 管理：`MINOR` 表示兼容线，结构或语义破坏必须使用新 `MINOR`；`PATCH` 不改变字段、枚举或语义。
- 每个对象默认拒绝未声明字段。增加字段或枚举值也进入新 `MINOR`，不得依赖旧消费者忽略未知内容。
- Platform 和 Scanner 显式配置共同支持的兼容线；无共同版本时在读取 Repository 内容前失败。
- JSON Schema 的 `$id` 包含契约名与完整版本；Schema 文件、示例和兼容测试由 `archguard-scanner` 随制品发布。

标准引用：[JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12)、[Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html)和[JSON Canonicalization Scheme RFC 8785](https://www.rfc-editor.org/rfc/rfc8785)。选择固定版本不表示自动继承未来标准变化。

## ScanRequest 顶层字段

| 字段 | 类型 | 必需 | 语义与约束 |
|---|---|---:|---|
| `schemaVersion` | SemVer 字符串 | 是 | 请求所用契约版本，首版为 `0.1.0` |
| `scanId` | UUID 字符串 | 是 | Platform 分配的业务 Scan 身份；所有执行尝试保持不变 |
| `requestId` | UUID 字符串 | 是 | 一次 Scanner 调用的幂等身份；传输重试必须复用 |
| `attempt` | 正整数 | 是 | 同一 `scanId` 的执行尝试序号，从 1 单调增加 |
| `requestedAt` | UTC ISO-8601 | 是 | Platform 创建本次调用的时间，只用于审计，不参与分析结果 |
| `input` | `InputReference` | 是 | 不含凭据的不可变输入引用 |
| `capabilities` | 非空字符串数组 | 是 | 稳定 Capability ID，去重并按字典序排列 |
| `policySnapshot` | `PolicySnapshot` | 是 | 本次 Scan 的不可变 Rule 配置，不允许执行中回读 Platform |
| `limits` | `ExecutionLimits` | 是 | 调用预算；Scanner 取请求值与部署硬上限中更严格者 |
| `trace` | `TraceContext` | 是 | `traceId` 与 `correlationId`，不得承载身份凭据 |

Platform 的 `projectId`、`repositoryId`、actor、权限和数据库键不进入 Scanner 公共模型。若运行审计需要业务关联，Platform 通过 `scanId` 在授权边界内完成。

## InputReference

| 字段 | 类型 | 必需 | 语义与约束 |
|---|---|---:|---|
| `type` | 枚举 | 是 | `git-commit`、`content-archive` 或 `managed-directory`；实际支持集合由 Capability 声明和 D14 限定 |
| `reference` | 字符串 | 是 | 由受控输入适配器解释的无密钥引用；禁止 URL userinfo、Token 和任意 Shell 片段 |
| `revision` | 字符串 | 条件 | `git-commit` 必需，必须是解析后的完整不可变对象 ID，不接受分支或标签 |
| `digest` | 字符串 | 条件 | archive/directory 必需，格式 `sha256:<64 lowercase hex>`；Git 输入可同时提供快照摘要 |
| `subpath` | 字符串 | 否 | `/` 分隔的规范相对路径；禁止空段、`.`、`..`、绝对路径、反斜杠和 NUL |

凭据通过受控运行环境临时注入输入适配器，不序列化进请求、结果、错误或日志。`managed-directory` 只表示由 ArchGuard 管理的已物化输入，不能指向任意主机路径。

## PolicySnapshot 与 ExecutionLimits

`PolicySnapshot` 必须包含 `policyId`、`policyVersion` 和按 `ruleId` 排序的 `rules`。每个 Rule 项包含 `ruleId`、精确 `ruleVersion`、`enabled`、最终 `severity` 和由该 Rule Schema 严格校验的 `parameters`；未知 Rule、版本或参数导致请求失败，不能静默跳过。

`ExecutionLimits` 必须包含绝对 `deadline` 以及 `maxFiles`、`maxTotalBytes`、`maxFileBytes`、`maxDirectoryDepth`、`maxResultItems`、`maxResultBytes` 六个正整数。生产部署缺少任一硬上限时 Scanner 拒绝就绪；具体初始数值由 M4 可复现基线确定并由 Deploy 固定，调用方不能请求放宽部署上限。

## ScanCancel

取消是独立、机器可验证且幂等的消息，包含 `schemaVersion`、`scanId`、当前 `requestId`、`requestedAt`、`reason` 和 `trace`。`reason` 只允许 `USER_REQUEST`、`DEADLINE_EXCEEDED`、`PLATFORM_SHUTDOWN` 或 `SUPERSEDED`，不得携带自由文本或敏感数据。

- 重复取消同一 `requestId` 返回相同已知终态，不产生第二次副作用。
- 若终态已在 Scanner 提交点完成，完成结果获胜；否则 Scanner 停止产生业务结论并返回 `CANCELLED`。
- 未知或不属于当前执行的 `requestId` 返回 `contract.request_not_active`，不能取消同一 `scanId` 的其他尝试。
- transport 可以用 HTTP、消息或进程信号实现，但必须保留以上身份和竞态语义。

## ScanResult 顶层字段

| 字段 | 类型 | 必需 | 语义与约束 |
|---|---|---:|---|
| `schemaVersion` | SemVer 字符串 | 是 | 结果契约版本，必须位于已协商兼容线 |
| `scanId` / `requestId` / `attempt` | 与请求一致 | 是 | 必须逐项回显，Platform 用于幂等和当前尝试校验 |
| `status` | 枚举 | 是 | `SUCCEEDED`、`PARTIAL`、`FAILED` 或 `CANCELLED` |
| `input` | `ResolvedInput` | 是 | 回显 type、不可变 revision/digest 和实际分析 subpath，不回显密钥引用 |
| `scanner` | 对象 | 是 | `scannerVersion`、`contractVersion` 和 allowlist `runtimeProfile`；不得输出主机名、路径或环境变量 |
| `capabilities` | 数组 | 是 | 每项请求能力的状态、Analyzer 身份/版本和相关 Diagnostic ID |
| `facts` | D12 `Fact` 数组 | 是 | 只包含可跨边界且被 Finding 引用或明确请求导出的 Fact |
| `findings` | D12 `Finding` 数组 | 是 | Rule 判定的架构结论；存在 Finding 不表示 Scan 失败 |
| `evidence` | D12 `Evidence` 数组 | 是 | 结果引用的最小证据，不含源码片段 |
| `diagnostics` | D12 `Diagnostic` 数组 | 是 | 输入、解析、执行、超限、安全或清理问题 |
| `statistics` | 对象 | 是 | 文件、Fact、Rule、Finding、Diagnostic 数量和阶段耗时；不参与结果身份 |
| `truncation` | 对象 | 是 | 每类输出的 `truncated` 与原始/返回计数；任何截断都要求 Diagnostic |
| `startedAt` / `completedAt` | UTC ISO-8601 | 是 | 执行观测时间，不参与确定性内容和排序 |

空集合必须使用 `[]`，不得用 `null`。可选标量缺失表示“未提供”，不得同时引入空字符串或魔法值作为第二种语义。

## CapabilityResult

每个请求 Capability 恰有一项结果，字段为 `capabilityId`、`status`、`analyzerId`、`analyzerVersion`、`diagnosticIds` 和统计摘要。状态取值：

| 状态 | 含义 |
|---|---|
| `COMPLETED` | 该能力按完整输入和预算完成，可有 warning/info Diagnostic |
| `PARTIAL` | 产生可用输出，但部分输入、前置能力或输出受限 |
| `FAILED` | 未产生可依赖的能力输出 |
| `SKIPPED` | 因依赖失败或取消而未启动；必须关联 Diagnostic |

`statistics` 固定包含 `discoveredFiles`、`analyzedFiles`、`skippedFiles`、`inputBytes`、`exportedFacts`、`evaluatedRules`、`findings`、`diagnostics` 和按已声明阶段键记录的 `durationMs`。`truncation` 为 facts/findings/evidence/diagnostics 四个固定成员，每项包含 `truncated`、`producedCount` 和 `returnedCount`。

## 总体状态与部分成功

| `status` | 判定规则 | 结果集合处理 |
|---|---|---|
| `SUCCEEDED` | 所有请求 Capability 均 `COMPLETED`，且没有 error Diagnostic 或截断 | 可持久化所有通过 D12/D13 校验的结果 |
| `PARTIAL` | 至少一项 Capability 为 `COMPLETED/PARTIAL`，且至少一项非 `COMPLETED`；或输出被截断；或清理失败但结果仍可验证 | 只持久化来源为可用能力且引用闭合的结果，并显式展示不完整性和清理告警 |
| `FAILED` | 没有请求 Capability 产生可依赖输出，或请求/输入/安全/输出校验失败 | `facts/findings/evidence` 必须为空；保留最小 Diagnostic |
| `CANCELLED` | Scanner 已确认取消并停止产生业务结论 | `facts/findings/evidence` 必须为空；能力状态和取消 Diagnostic 可保留 |

- Finding 表示 Rule 被违反，不把 `SUCCEEDED` 改为失败。
- 解析失败是 Diagnostic；只有它造成能力不完整时才影响 Capability/总体状态。
- 截断不能标为 `SUCCEEDED`，也不能省略原始计数和 `output.limit_exceeded` Diagnostic。
- Platform 不把 `PARTIAL` 默认为完整合规结果，产品展示和 API 必须保留状态。

## 幂等、重复与重试

- 同一 `requestId` 只允许对应一份规范化请求；语义字段不同则返回 `contract.idempotency_conflict`。
- 网络重试复用 `requestId` 和 `attempt`；Platform 因可重试失败发起新执行时使用新 `requestId`、递增 `attempt`、保持 `scanId`。
- Scanner 可以返回缓存终态或重新执行相同请求，但规范化结果内容必须一致；时间和阶段耗时可不同。
- Platform 只接受当前有效尝试的结果，并以 `scanId` 幂等写入；迟到结果进入审计而不覆盖更新终态。
- `retryable` 只是 Scanner 对故障类别的提示；Platform 仍应用自己的最大尝试、退避和截止时间。

## ContractError 与错误码

若顶层 JSON、版本或必需身份无法解析，返回独立 `ContractError`：`schemaVersion`（可判定时）、`code`、安全的 `message`、`traceId` 和 `retryable`。若身份可解析，则优先返回 `FAILED` ScanResult。

错误码使用稳定点分命名空间：`contract.*`、`input.*`、`capability.*`、`rule.*`、`execution.*`、`output.*`、`security.*`、`cleanup.*`。未知错误码在当前兼容线内拒绝；代码、默认 retryable 和允许 scope 由 D12/D13 的目录冻结。

## 规范化与排序

- JSON 属性顺序不具有语义；黄金测试先移除 `startedAt`、`completedAt`、阶段 `durationMs` 等观测字段，再按 JSON Canonicalization Scheme（RFC 8785）比较确定性投影。完整结果仍必须通过 Schema 校验。
- 数组排序固定：capabilities 按 ID，Evidence/Fact/Finding/Diagnostic 按各自 D12 身份字段。
- 路径统一为相对输入根的 `/` 分隔 Unicode 字符串；不输出盘符、UNC、主机临时根或 `..`。
- 数字使用 Schema 定义的整数范围；时间统一 UTC 并以 `Z` 结尾。
- 输出引用必须闭合：不存在悬空 Evidence、Fact、Diagnostic 或 Capability 引用。

## 兼容、发布和回滚

1. Docs 先接受 D11–D13 与对应 ADR。
2. Scanner 发布 `0.1.0` Schema、有效/无效示例和提供方测试。
3. Platform 引入消费者测试并保持 Fake adapter 语义一致，再启用真实适配器。
4. Samples 固定契约版本，Deploy 记录共同兼容线后才能组合发布。
5. 破坏性变化发布新 `0.MINOR` 并与旧线并行；Platform 先回退消费线，随后才能回退 Scanner。

当前文档没有运行时制品；回滚只需撤销本分支，不修改数据库或其他仓库。

## 候选决策

- 首个契约为严格 JSON Schema 2020-12，版本 `0.1.0`，Scanner 拥有机器制品。
- `scanId` 标识业务 Scan，`requestId` 标识幂等调用，`attempt` 标识执行尝试。
- `SUCCEEDED/PARTIAL/FAILED/CANCELLED` 与 Capability 状态共同表达部分成功；Finding 不决定执行成功。
- 请求携带不可变 Policy 快照和全部有限预算，不允许 Scanner 回读 Platform 可变状态。
- 凭据不进入契约，未知字段/枚举/错误码在兼容线内失败关闭。

以上公共契约语义已于 2026-09-09 通过 G3 评审。

## 非目标

- 不选择传输协议、Java DTO/SDK 生成器、Schema Registry 或消息 Broker。
- 不决定 V1 实际开放哪种 `InputReference`，也不承诺远程 Git 获取。
- 不定义 Platform REST 状态机、租约、重试次数或数据库结构。
- 不把文档表格冒充 M4 必须发布的机器 JSON Schema。

## 开放问题

- `0.1.0` 的 Schema 文件组织、代码生成和兼容测试工具由 M4 Technical Design 选择。
- V1 启用哪些输入类型和 Capability ID 由 D14 冻结。
- 初始 `ExecutionLimits` 数值由 M4 基线和 Deploy 环境共同确定；缺省时生产 Scanner 不得就绪。

## 验收证据

- 请求、结果、能力状态、错误、幂等和排序规则均有唯一语义。
- [结果与 Rule 模型](result-rule-model.md)定义跨边界结果项，[不可信 Repository 安全](untrusted-repository-security.md)定义输入和输出安全。
- [ADR-0001](../adr/0001-versioned-scanner-contract.md)记录独立版本化契约选择。
