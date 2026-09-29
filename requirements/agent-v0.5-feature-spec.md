# Feature Spec：Java Agent 增强 `v0.5.0-agent`

- 状态：Ready；仅 4A 范围评审进行中，功能实现未启用
- 阶段：4
- 阶段跟踪：[AI-ArchGuard/archguard-platform#34](https://github.com/AI-ArchGuard/archguard-platform/issues/34)
- 4A Issue：[AI-ArchGuard/archguard-docs#30](https://github.com/AI-ArchGuard/archguard-docs/issues/30)
- 主要仓库：`archguard-platform`、`archguard-web`、`archguard-samples`、`archguard-deploy`、`archguard-docs`
- 事实提供方：`archguard-scanner` 继续提供已发布的 Finding 和 Evidence；4A 不修改 Scanner 或 Schema
- 前置：[持续治理 `v0.4.0-governance` 阶段验收](../reports/2026-09-27-governance-v0.4.0-acceptance.md)
- 架构决策：[ADR-0001](../adr/0001-versioned-scanner-contract.md)、[ADR-0003](../adr/0003-untrusted-repository-default-deny.md)、[ADR-0004](../adr/0004-platform-modular-monolith.md)、[ADR-0005](../adr/0005-postgresql-business-source-of-truth.md)、[ADR-0008](../adr/0008-baseline-and-quality-gate-semantics.md)、[ADR-0009](../adr/0009-pr-revision-delta.md)、[ADR-0010](../adr/0010-agent-trust-boundary-and-model-egress.md)

## 阶段入口关卡

4A 只交付本 Spec、ADR-0010、索引和路线图同步，用一个 Docs PR 冻结阶段范围与验收语义。此时不创建阶段验收报告，不修改 Scanner Schema，不启动 Platform、Web、Gateway 或 Evals 功能开发。

只有 4A PR 合并且 Docs `main` CI 成功后，4B 才能从 `Todo` 进入 `In Progress`。4B–4H 依次遵守同一关卡：前一切片相关 PR 已合并且合并后的 `main` CI 成功，下一切片才可启动。真实模型调用还必须满足 ADR-0010 的数据处理审批、凭据、外发字段和费用关卡；未获批准时，确定性假模型可继续支持契约和 UI 开发，真实模型切片暂停。

## 问题与用户价值

阶段 3 已能确定地发现、分类和阻断新增架构问题，但用户仍需自行理解规则依据、逐项定位 Evidence，并把多个 Finding 归纳成可执行的评审说明。直接把报告交给模型会扩大源码和文档外发面，也会让提示注入、虚假引用、越权数据和模型故障污染确定性治理结果。

阶段 4 的目标是让获授权用户在 Web 中显式请求单个 Finding 的解释，或对已选择的 Finding 生成 PR 摘要和低风险建议。Platform 只把最小、已授权、版本化的事实和文档摘录交给可替换模型适配器；模型输出经过 Schema、权限、引用和业务校验后作为独立建议保存。Agent 不创建或修改 Finding，不影响基线、例外、质量门禁或 CI 退出码。

## 用户结果

1. Maintainer 可以为一个 Project 显式上传 Markdown 或纯文本文档；每次上传形成不可变版本，旧版本和引用仍可追溯。
2. 有权读取 Finding 的用户可以在 Web 中显式请求解释，并看到排队、运行、成功或明确失败状态。
3. 成功结果展示结论、规则依据、可验证引用、低风险建议、证据覆盖等级、Prompt/模型版本和 traceId。
4. Maintainer 可以从同一 PR/扫描中选择 Finding 生成摘要；摘要只覆盖所选 Finding，不扩展为全仓库判断。
5. 引用只解析到请求者有权访问的真实 Evidence 或不可变文档版本；无效、越权或无法验证的引用不作为事实展示。
6. 模型关闭、超时、不可用、输出无效、额度耗尽或引用校验失败时，用户看到稳定失败原因；扫描、基线和门禁照常工作。
7. 运维方可以按 traceId 审计请求者、Project、输入版本、模型/Prompt 版本、Token、延迟、费用和结果状态，而不记录凭据、完整 Prompt、完整源码或文档正文。

## 事实、建议与追溯边界

- Scanner Finding、Evidence、Rule 和已持久化治理结果是确定性事实来源。AgentResult 是独立、不可变、可版本追溯的建议记录。
- 每个 AgentRequest 固定关联 Project、用途、请求者、Finding/扫描版本、所选 Finding 集合、文档版本集合、Prompt 版本、输出 Schema 版本、模型提供方协议和模型版本。
- 模型只能引用 Platform 为本次请求生成的不透明候选引用 ID。Platform 在保存成功结果前把它解析回同 Project 的 Evidence 或 DocumentVersion，并重新执行授权、版本、范围和定位校验。
- 证据覆盖等级由 Platform 在引用校验后计算，不接受模型自报置信度作为事实：`COMPLETE` 表示所有事实性结论均有有效引用，`PARTIAL` 表示至少一个结论有有效引用但仍有明确未覆盖项，`INSUFFICIENT` 表示没有足够引用支撑事实性结论。
- `INSUFFICIENT` 可以形成诚实的“证据不足”结果，但不得展示无引用判断为事实。引用不实、跨 Project、版本不匹配或输出不符合 Schema 时整个请求失败关闭。
- AgentResult 不被门禁、基线、Finding 分类、PolicyException、PR 修订差异或 CI 退出码读取；任何失败都不能降级或升级既有 `PASS`、`FAIL`、`ERROR`。

## 知识来源与检索范围

- 初版唯一知识来源是 Maintainer 通过 Platform 显式上传的 UTF-8 Markdown 或纯文本文件；不接受压缩包、二进制、远程 URL、Git 凭据或仓库地址。
- 文档按 Project 隔离。每次上传创建不可变 DocumentVersion，记录内容摘要、媒体类型、字节数、上传者和时间；更新创建新版本，不覆盖旧内容。
- 初版使用 PostgreSQL 在已授权 Project 和明确 DocumentVersion 集合内做有界检索；不引入向量数据库，不由 Platform clone/fetch Git 仓库，也不访问外部搜索或模型内置工具。
- 上传内容始终是不可信数据。文档中的指令、角色声明、工具请求、数据外发请求或“忽略系统规则”等文本只作为可引用内容，不能改变 Prompt、权限、检索范围、输出 Schema 或调用策略。
- 上传时和检索时均执行大小、类型、编码、段落数量、返回条数和总字符/Token 上限；精确数值由 4C Technical Design 在不超过 ADR-0010 外发上限的前提下固定。

## 模型调用与最小外发

模型调用遵守 [ADR-0010](../adr/0010-agent-trust-boundary-and-model-egress.md)：默认关闭，由运行环境显式配置，并由 Project Maintainer 启用。首个真实协议是 OpenAI Responses API 的受限 HTTPS/JSON 子集；Platform 通过自有端口适配器编排，不把模型 SDK 引入领域层。

每次调用只允许外发以下版本化字段的最小投影：

- 请求用途、输出 Schema 版本、Prompt 版本和不含内部 ID 的请求关联标记；
- 所选 Finding 的规则 ID/版本、严重性、规范消息、受影响逻辑实体和必要位置；
- 与所选 Finding 直接关联的最小 Evidence 类型、关系、规范化位置和候选引用 ID；
- 在本次 Project 授权范围内检索出的文档片段、DocumentVersion 内容摘要和候选引用 ID；
- 生成结构化结果所需的语言/呈现参数。

不得外发 OIDC 令牌、API 密钥、Webhook secret、内部数据库 ID、成员列表、审计正文、未选择的 Finding、完整扫描报告、完整上传文档、完整仓库路径、主机路径、客户源码或无关 Project 数据。4H 的真实调用验收只使用合成 Finding、Evidence 和文档。

真实调用必须使用运行时 Secret、固定 HTTPS 目标允许列表、严格结构化输出、禁用工具、禁用会话延续、禁用后台模式并设置 `store=false`。数据处理条款必须经项目所有者批准且满足零数据保留或等效约束；若提供方、地区、模型、保留策略或价格目录无法确认，调用在外发前失败关闭。

费用硬上限为每请求最多 8,000 输入 Token、1,500 输出 Token、预估费用不超过 0.10 美元；每 Project 每 UTC 日最多 5 美元，单部署每 UTC 日最多 20 美元。运维方可以下调但不能绕过；提价或扩大外发上限必须单独评审并更新 ADR。无法取得版本化价格或预估超过任一上限时不发起调用。一个 AgentRequest 最多一次提供方尝试，重复提交返回同一请求，不通过自动重试制造重复费用。

## 功能需求

- FR-001：模型能力默认关闭；未配置、未获数据处理批准或 Project 未启用时，创建请求返回明确不可用状态且不外发数据。
- FR-002：只有 Maintainer 可以上传文档；上传必须绑定 Project，校验 UTF-8 Markdown/纯文本、大小、内容摘要和幂等键。
- FR-003：文档更新创建新的不可变 DocumentVersion；已被 AgentResult 引用的版本不能覆盖或删除。
- FR-004：检索只在请求者有权访问的 Project、明确文档版本和有界候选集合内执行；跨 Project 资源使用隐藏式未找到或明确拒绝且不泄漏存在性。
- FR-005：有 Finding 读取权限的用户必须显式创建解释请求；页面加载、扫描完成、PR Webhook 或门禁求值不得隐式触发模型。
- FR-006：解释请求固定关联一个 Finding 及其 Scan/Finding 版本；Finding 不存在、未完成或归属不一致时不创建模型调用。
- FR-007：摘要请求只接收同 Project、同 PR/扫描兼容范围内由用户明确选择的 Finding；空集合、混合 Project 或不兼容版本失败关闭。
- FR-008：Project 内相同用途、输入版本集合、Prompt/Schema/模型版本和幂等键的重复请求返回原请求；同一幂等键对应不同内容返回稳定冲突。
- FR-009：异步状态至少表达 `QUEUED`、`RUNNING`、`SUCCEEDED`、`FAILED`；失败原因至少区分关闭/未配置、授权拒绝、额度耗尽、超时、提供方不可用、输出无效、引用无效和内部错误。
- FR-010：模型原始输出先通过严格 JSON Schema，再通过 Project 授权、引用可解析性、版本、范围、建议安全等级和业务不变量校验；任何一步失败都不产生成功 AgentResult。
- FR-011：成功 AgentResult 至少包含结论、规则依据、已验证引用、低风险建议、证据覆盖等级、状态、traceId、Prompt 版本、输出 Schema 版本、模型提供方协议和模型版本。
- FR-012：建议只允许解释、人工核验步骤和低风险修改方向；不得包含自动执行状态或声称已修改 PR、源码、RuleSet、PolicyException、Finding、基线或门禁。
- FR-013：模型拒绝、超时、网络错误、非法状态、截断、非 Schema 输出、未知字段或无效引用全部转换为稳定失败，不展示未经验证的原始输出。
- FR-014：每次请求记录请求者、Project、用途、输入版本摘要、状态转换、traceId、模型/Prompt/Schema/价格目录版本、输入/输出 Token、延迟、预估/实际费用和失败类别。
- FR-015：审计与日志不得记录密钥、授权头、完整 Prompt、模型原始输出、完整源码、完整报告或完整上传文档；必要摘要使用内容 digest 和计数。
- FR-016：模型适配器故障、额度耗尽或 Agent 数据迁移失败不得阻塞 Scanner 报告接收、基线、例外、门禁、Webhook 或 CI 查询路径。

## 非功能需求

- 安全：输入和输出均不可信；每一步重新验证 Project、资源版本和授权。模型没有工具、数据库、文件系统、网络代理或写接口权限。
- 隐私：数据最小化、默认关闭、显式用户触发；真实调用只发送批准范围，验收只使用合成数据。
- 可用性：模型调用异步且有硬超时；失败可观察但不影响确定性治理路径。一个请求最多一次提供方尝试。
- 一致性：PostgreSQL 是 AgentRequest、DocumentVersion、已验证 AgentResult、额度账本和审计的业务事实来源；提供方响应不是事实来源。
- 可追溯：历史结果永久引用确切输入、文档、Prompt、Schema、模型和价格目录版本；后续配置变化不改写旧结果。
- 成本：调用前预估并预留额度，调用后记录实际用量；未知价格、超限或并发预留冲突均失败关闭。
- 兼容：Scanner Result/Rules Schema 保持 `0.1.0`；Agent Output/Request 契约由 Platform 在 4B 发布独立兼容线，不导入 Scanner 内部类。
- 性能：4B 固定异步请求和查询 SLO；Web 不同步等待模型，Scanner 和质量门禁 SLO 不因 Agent 启用而放宽。

## 验收标准

- Given 模型默认关闭或数据处理审批缺失，When 用户请求解释，Then 返回明确不可用状态且网络侧无模型请求。
- Given 一个获授权 Finding 和对应 Evidence，When 用户请求解释且模型返回合规内容，Then 结果关联确切 Finding/扫描、Prompt、Schema、模型和 traceId，并只展示可解析引用。
- Given 引用同 Project 的 Evidence 或 DocumentVersion，When 查询历史结果，Then 可解析到请求时的不可变版本，当前文档更新不改变旧引用。
- Given 模型返回未知引用、跨 Project 引用、错误版本或无引用事实，When Platform 校验，Then 请求失败或按 Schema 形成 `INSUFFICIENT`，未经验证内容不作为事实展示。
- Given 另一 Project 的用户或资源 ID，When 上传、检索、创建请求或读取结果，Then 拒绝且不泄漏资源存在性，不产生模型调用。
- Given 上传文档含“忽略规则”“调用工具”或“泄漏其他 Project”等提示注入，When 检索并生成，Then Prompt、权限、候选引用和外发字段不变化，输出仍经完整校验。
- Given 相同幂等键和相同输入，When 并发或重复请求，Then 返回同一 AgentRequest 且最多一次提供方调用；不同输入复用键返回冲突。
- Given 模型超时、不可用、拒绝、输出不合 Schema、引用不实或额度耗尽，When 请求结束，Then 显式失败并记录稳定类别、Token/延迟/费用和 traceId，不泄漏原始响应。
- Given 预估单次、Project 日额或部署日额将超限，When 请求进入调用前检查，Then 不外发数据并返回 `QUOTA_EXHAUSTED`。
- Given 原有门禁为 `PASS` 或 `FAIL`，When Agent 成功、失败、超时或不可用，Then Finding、基线、例外、GateEvaluation 和 CI 退出码逐字保持不变。
- Given 选择一组兼容 Finding，When 生成 PR 摘要，Then 输出只覆盖所选 Finding，所有事实性结论有已验证引用或明确标注证据不足。
- Given 4H 合成 Compose 旅程，When 从 Web 请求解释和摘要，Then 可追踪 Web → Platform → 模型 → 校验 → 引用展示，并核对所有相关 PR CI 与合并后 `main` CI。

## 指标

- 成功指标：合成验收中的有效请求 100% 关联版本化输入并通过引用校验；重复请求不增加提供方调用；成功结果可按 traceId 完整追溯。
- 防护指标：跨 Project 数据外发为 0；未经验证引用作为事实展示为 0；Agent 导致门禁或 CI 结果变化为 0；超预算调用为 0；真实验收中的客户源码外发为 0。
- 运行指标：按状态和失败类别统计请求数、输入/输出 Token、端到端/提供方延迟、预估/实际费用和额度拒绝，不以提高成功率为由放宽校验。

## 实施切片

| 切片 | 交付结果 | 主要仓库 |
|---|---|---|
| [4A](https://github.com/AI-ArchGuard/archguard-docs/issues/30) | Feature Spec、Agent 信任与模型数据外发 ADR、范围和验收冻结 | Docs |
| [4B](https://github.com/AI-ArchGuard/archguard-platform/issues/35) | Agent 输出、引用、请求状态和版本追溯契约；固定合成案例 | Platform、Docs、Samples |
| [4C](https://github.com/AI-ArchGuard/archguard-platform/issues/36) | Maintainer 显式上传项目 ADR/架构文档；不可变版本、Project 授权和有界检索 | Platform |
| [4D](https://github.com/AI-ArchGuard/archguard-platform/issues/37) | 按需解释单个 Finding：异步模型调用、严格校验、审计与失败回退 | Platform |
| [4E](https://github.com/AI-ArchGuard/archguard-platform/issues/38) | 基于已选 Finding 的 PR 摘要与低风险建议；不参与门禁 | Platform |
| [4F](https://github.com/AI-ArchGuard/archguard-web/issues/9) | Web 文档管理、解释与摘要展示、引用和不可用状态 | Web |
| [4G](https://github.com/AI-ArchGuard/archguard-platform/issues/39) | 注入、越权、超时、重复请求、成本上限与恢复测试；积累未来 Evals 案例 | Platform、Web、Samples |
| [4H](https://github.com/AI-ArchGuard/archguard-deploy/issues/10) | 合成数据 Compose 验收、兼容矩阵、发布及唯一阶段报告 | Deploy、Docs |

4A 只进行范围评审。4B–4H 在 Project #2 中保持 `Todo`，只有前置关卡完成后依次进入 `In Progress`。阶段 4 可以保存未来 Evals 案例，但不得启用阶段 6 的正式 Evals 运行系统。

## 明确非目标

- 不让模型创建、修改、关闭或重新分类 Finding，不改变 Evidence、基线、例外、门禁或 CI 退出码。
- 不自动修改、提交或合并 PR，不写源码、RuleSet、PolicyException 或项目文档。
- 不启用 MCP Gateway、工具调用、Shell、浏览器、外部搜索、模型内置文件检索或远程 Git 操作。
- 不由 Platform clone/fetch 仓库，不接收源码归档或 Git 凭据。
- 不引入向量数据库、Redis、Kafka、独立 Agent 微服务或新的业务事实来源。
- 不修改 Scanner Result/Rules Schema `0.1.0`，不把 Agent 字段加入 Scanner Finding。
- 不提前建设阶段 5 Gateway 或阶段 6 正式 Evals；只保留可复用的合成安全案例。
- 不在 4A 创建阶段验收报告、Technical Design、运行时代码、数据库迁移或占位 API Schema。

## 兼容、发布与回滚

兼容顺序固定为 Docs 冻结语义 → Samples/Platform 冻结 Agent 契约与合成案例 → Platform 文档版本、检索和模型编排 → Web 消费 → Deploy Compose 验收与发布 → Docs 唯一阶段报告。Scanner `v0.2.1` 及 Result/Rules Schema `0.1.0` 保持不变，除非未来独立阶段和 ADR 明确授权。

回滚先关闭 Web Agent 入口和 Project 模型开关，再关闭真实模型适配器，最后按兼容矩阵回退 Web/Platform 应用。已发布 Flyway 迁移、DocumentVersion、AgentRequest、AgentResult、额度和审计记录保留，不执行 down migration，也不改写历史解释。关闭 Agent 后扫描、报告提交、基线、例外、门禁、Webhook 和 CI 继续可用。

## 风险、依赖与开放关卡

- 真实模型提供方、地区、组织/项目级零数据保留或等效条款、密钥托管和价格目录必须由项目所有者批准；未批准时 4D/4E 只允许确定性假模型，真实调用暂停。
- OpenAI Responses API 是首个受支持协议，不等于把领域层或 Agent 契约绑定到供应商；新增协议必须实现同一最小外发、校验、费用和审计不变量。
- PostgreSQL 有界检索能否满足已声明的文档规模和延迟由 4C/4G 用合成数据验证；没有测量证据不引入向量数据库。
- 文档删除、保留期和管理员密钥轮换的产品策略在 4C Technical Design 前必须明确，但不能削弱已被历史结果引用的不可变版本。
- Project #2 的状态选项为 `Todo`、`In Progress`、`Done`、`Blocked`；4A 设为 `In Progress`，其余切片保持 `Todo`。
