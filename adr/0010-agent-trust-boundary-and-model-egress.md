# ADR-0010：冻结 Agent 信任边界与模型数据外发

- 状态：Accepted
- 日期：2026-09-29
- 决策者：ArchGuard 项目所有者
- 扩展：[ADR-0003](0003-untrusted-repository-default-deny.md)、[ADR-0004](0004-platform-modular-monolith.md)、[ADR-0005](0005-postgresql-business-source-of-truth.md)、[ADR-0006](0006-java-first-phased-delivery.md)、[ADR-0008](0008-baseline-and-quality-gate-semantics.md)
- 替代：无

## 背景

阶段 3 已把 Scanner Finding、Evidence、基线、PR 修订差异和质量门禁建立为可重放的确定性事实。阶段 4 要在 Web 中按需提供解释、引用、PR 摘要和低风险建议，但模型、上传文档、检索片段和模型输出全部是不可信输入。若直接把扫描报告或文档交给外部模型，系统可能外发无关 Project 数据、客户源码或凭据，并接受提示注入、虚假引用和越权结果。

Agent 还可能被误解为新的事实或门禁判定器。模型故障、价格变化、提供方保留策略或输出格式变化都不能改变 Finding、基线、例外、门禁和 CI 行为。阶段 4 因此必须先冻结编排所有权、外发协议、数据最小化、凭据、数据处理、费用和失败语义。

## 决策驱动因素

- Scanner Finding 和 Evidence 必须继续作为事实来源；模型只解释和建议。
- 用户必须显式发起请求，且每个输入、输出和引用都能追溯到 Project 与不可变版本。
- 上传文档可以包含提示注入，不能改变权限、Prompt、工具或外发范围。
- 外部模型会处理 Project 数据；默认关闭、最小外发和可证明的数据处理约束优先于便利性。
- 模型输出即使符合 JSON Schema，也可能语义错误、引用不实或越权，必须由 Platform 再校验。
- 费用、Token 和延迟必须有调用前硬上限；重复请求和超时不能造成无限重试或重复计费。
- Platform 初期仍是模块化单体；没有独立团队、扩缩或隔离证据，不创建 Agent 微服务。
- 阶段 5 Gateway 和阶段 6 Evals 不能因 Agent 实现而提前启用。

## 选择

### 所有权与隔离

- Agent 是 Platform 模块化单体中的独立应用编排模块，通过公开应用接口读取获授权的 Finding、Evidence、文档版本和 PR/扫描上下文。它不直接读取其他模块的表。
- 领域层只依赖模型端口和版本化 Agent 契约，不依赖 Spring Web、数据库驱动或外部模型 SDK。模型 SDK/HTTP 客户端仅存在于基础设施适配器。
- AgentRequest、DocumentVersion、经校验的 AgentResult、额度账本和审计以 PostgreSQL 已提交状态为准；模型提供方响应不是业务事实来源。
- AgentResult 与 Finding、Evidence、BaselineVersion、GateEvaluation、PolicyException 和 PR 修订差异分表、分类型并单向引用。确定性路径不得读取 AgentResult 决定任何状态或退出码。
- 模型没有 Platform API、数据库、文件系统、Shell、网络代理、Git、Web、MCP 或其他工具权限。阶段 4 不注册任何模型工具。

### 显式请求与授权快照

- 页面加载、扫描完成、报告提交、Webhook、门禁求值或文档上传不得隐式触发模型。用户必须在 Web 中显式请求解释或摘要。
- 创建请求时先验证请求者对 Project、Finding/PR、扫描和文档版本的读取权限；文档上传仅限 Maintainer。
- 请求固定记录 Project、用途、请求者、Finding/扫描或 PR 版本、所选 Finding 集合、DocumentVersion 集合、Prompt 版本、输出 Schema 版本、模型协议/版本和输入 digest。
- 调用前再次校验授权和版本归属；调用后保存结果前第三次校验引用目标仍属于原 Project 和原版本集合。跨 Project 资源失败关闭，不向模型发送存在性信息。
- 已完成结果不可变。权限撤销后读取仍按当前授权判断，但历史结果和审计不被改写。

### 文档和提示注入边界

- 初版只接受 Maintainer 显式上传的 UTF-8 Markdown/纯文本。每次上传创建不可变 DocumentVersion；不接受 URL、仓库地址、压缩包、二进制、远程文件或 Git 凭据。
- 检索限定在一个 Project 和明确 DocumentVersion 集合，使用 PostgreSQL 的有界全文/关键词能力。输入大小、片段数量、单片段长度和总 Token 均有限；阶段 4 不引入向量数据库。
- 文档、Finding 消息、Evidence 文本和用户可控名称统一作为带来源标签的数据块，不拼接为系统/开发者指令。内容中的角色、工具、外联、越权或忽略规则请求永远不具有控制权。
- Prompt 由 Platform 拥有并版本化；运行时用户不能覆盖系统约束、输出 Schema、模型设置、引用候选、费用或网络策略。

### 引用和输出信任

- Platform 为本次调用允许的 Evidence 和文档片段生成不透明、请求内唯一的候选引用 ID。模型只能返回这些 ID，不能返回数据库 ID、任意 URL、文件路径或自创引用。
- 返回先通过严格 Agent Output JSON Schema 和未知字段拒绝，再验证引用存在、Project、资源类型、不可变版本、范围与可显示位置；失败不保存为成功结果。
- 每个事实性结论必须关联至少一个已验证引用，或明确标记证据不足。未经验证的原始模型输出不返回 Web、不进入审计正文，也不作为重试 Prompt。
- Platform 基于通过校验的引用计算证据覆盖等级 `COMPLETE`、`PARTIAL`、`INSUFFICIENT`。模型自报置信度、概率或权威措辞不具事实地位。
- 低风险建议仅包含解释、人工核验步骤和可选修改方向。任何声称已修改 PR、源码、RuleSet、例外、Finding、基线或门禁的输出都违反业务 Schema。

### 首个真实模型协议

- 首个受支持协议是 OpenAI Responses API `POST /v1/responses` 的受限 HTTPS/JSON 子集。选择它是因为该协议支持通过 `text.format` 使用严格 JSON Schema 输出；[官方 Structured Outputs 文档](https://developers.openai.com/api/docs/guides/structured-outputs)仍不能替代 Platform 的权限、引用和业务校验。
- 请求只允许配置固定 allowlist 中的 HTTPS base URL 和显式模型 ID，并发送 `model`、版本化 `instructions`、结构化文本 `input`、`text.format` 严格 JSON Schema、`max_output_tokens`、`store=false`、`background=false`、禁用自动截断所需设置和不含内部资源 ID 的关联元数据。
- 不发送 `previous_response_id` 或 conversation，不启用流式输出、后台模式、Web/file search、code interpreter、computer use、函数或其他内置工具，不上传文件。一个 AgentRequest 只对应一次无会话调用。
- 模型 ID 和提供方返回的确切模型/响应标识作为追溯元数据保存；领域契约不使用供应商响应对象。未来新增协议必须走新的适配器并满足本 ADR 全部不变量，不能把 OpenAI SDK 类型带入领域或公共 Agent Schema。

### 最小外发字段

允许外发的上限是：用途、Prompt/输出 Schema 版本、无内部 ID 的请求关联标记；所选 Finding 的规则 ID/版本、严重性、规范消息、受影响逻辑实体和必要位置；直接关联的最小 Evidence 类型、关系、规范化位置与候选引用 ID；本次获授权检索出的文档片段、DocumentVersion 内容摘要与候选引用 ID；以及语言/呈现参数。

禁止外发 OIDC/会话令牌、模型密钥、Webhook secret、内部数据库 ID、成员和权限列表、审计正文、未选择的 Finding、完整扫描报告、完整上传文档、完整仓库/主机绝对路径、客户源码、无关 Project 数据和任何运行时 Secret。Scanner Evidence `0.1.0` 不含源码片段的现有边界保持不变。阶段 4 真实模型验收只使用合成 Finding、Evidence 和文档。

### 凭据、网络和数据处理

- 模型功能默认关闭。真实适配器只有在部署运维显式启用、Project Maintainer 显式启用且项目所有者批准提供方/地区/模型/数据处理条款后才可调用。
- API key 由部署 Secret 注入模型适配器，不由用户上传，不保存在业务表、AgentRequest、日志、错误或审计正文中；请求只通过 `Authorization: Bearer` 发送到固定 allowlist 主机。
- 只允许校验证书的 HTTPS，拒绝明文、任意重定向、用户提供 base URL、私网/环回/链路本地目标和代理继承。出站防火墙只开放已批准提供方主机。
- 即使提供方支持服务端状态，请求也固定 `store=false`。项目所有者必须确认组织/项目已获零数据保留或等效数据处理约束；官方说明默认 API 可能保留滥用监控内容，而 Zero Data Retention 需要批准，见[数据控制文档](https://developers.openai.com/api/docs/guides/your-data)。未获批准、状态无法核验或条款变化时，真实调用在外发前暂停。
- Prompt/响应正文不写入通用日志或审计；Platform 只持久化业务需要的最小输入引用、经校验结构化结果、digest、Token、延迟、费用和提供方响应标识。供应商调试日志必须关闭正文记录。

### 费用、Token、超时和重复请求

- 硬上限为：每次最多 8,000 输入 Token、1,500 输出 Token、调用前预估费用最多 0.10 美元；每 Project 每 UTC 日最多 5 美元，单部署每 UTC 日最多 20 美元。
- 价格使用版本化 allowlist 目录。调用前在同一数据库事务中按最坏情况预估并预留额度；价格未知、目录过期、并发预留冲突或任一上限不足时不外发数据。调用后记录提供方实际 Token/费用并结算，不能用事后告警代替硬上限。
- 运维方可以下调上限；上调单请求 Token/费用、Project 日额或部署日额需要更新本 ADR 或由后续 ADR 取代，并重新完成数据处理与容量评审。
- 提供方硬超时 30 秒。一个 AgentRequest 最多一次提供方尝试；网络中断或超时后不自动重试未知结果。用户显式重试创建新的、可审计请求并重新占用额度。
- Project 内幂等键加输入 digest 约束重复请求：相同键和相同输入返回原请求，不再次调用；相同键不同输入返回冲突。

### 状态、失败与审计

- AgentRequest 至少经历 `QUEUED`、`RUNNING`、`SUCCEEDED` 或 `FAILED`。4B 契约固定合法转换和错误结构，不允许失败伪装为成功或空解释。
- 稳定失败类别至少包括 `MODEL_DISABLED`、`FORBIDDEN`、`QUOTA_EXHAUSTED`、`MODEL_TIMEOUT`、`MODEL_UNAVAILABLE`、`OUTPUT_INVALID`、`CITATION_INVALID` 和 `INTERNAL_ERROR`。
- 每次请求按 traceId 记录请求者、Project、用途、输入版本摘要、状态转换、Prompt/Schema/协议/模型/价格目录版本、输入/输出 Token、提供方与端到端延迟、预估/实际费用和失败类别；不记录 Secret、完整 Prompt、原始输出、完整源码或文档正文。
- 模型、Agent worker、额度或文档检索故障不得阻断报告接收、Scanner、基线、例外、门禁、Webhook 或 CI 查询。Agent 不可用时这些路径的既有 `PASS`、`FAIL`、`ERROR` 和退出码保持不变。

## 备选方案

- 让模型直接读取完整报告、源码或全部文档：实现简单但违反最小外发和 Project 隔离，拒绝。
- 让模型自由生成文件路径、URL 或数据库 ID 作为引用：无法证明来源真实、获授权和版本一致，拒绝。
- 仅依赖提供方 Structured Outputs：只能约束部分结构，不能证明授权、引用或业务语义，拒绝。
- 在浏览器直接调用模型：会暴露凭据并绕过 Platform 授权、审计、额度和引用校验，拒绝。
- 在阶段 4 引入向量数据库：当前 Markdown/文本规模和 PostgreSQL 有界检索尚无瓶颈证据，拒绝。
- 把 Agent 拆为微服务：当前没有独立扩缩、团队、合规或发布边界证据，拒绝。
- 使用自动重试提高成功率：超时后的提供方结果未知，会重复费用和结果，初版拒绝。
- 提前使用 MCP Gateway 或模型内置工具：扩大攻击面并越过阶段 5 关卡，拒绝。
- 以模型自报置信度替代证据覆盖：不可验证且容易误导，拒绝。

## 正面影响

- 用户获得可追溯解释和建议，同时确定性 Finding 与门禁语义保持不变。
- 外发数据、凭据、网络和费用都有调用前硬边界；真实模型未获批准时可以安全停用。
- 引用从模型自由文本变为 Platform 提供并重新验证的能力句柄，降低幻觉和越权展示风险。
- 协议适配器可替换，Platform 领域与公共 Agent 契约不绑定供应商 SDK。
- PostgreSQL 复用现有业务事实、事务和审计能力，不提前引入新基础设施。

## 负面影响与风险

- 严格最小外发和 8,000 Token 上限可能导致上下文不足；系统必须诚实返回 `PARTIAL` 或 `INSUFFICIENT`，不能静默扩大发送范围。
- 一次尝试策略会降低瞬时故障下的成功率，但避免未知结果自动重试造成重复费用；后续只有在提供方幂等证据充分时重新评审。
- 零数据保留或等效条款可能不可用或需商务审批，从而暂停真实模型切片；确定性假模型仍可验证契约和 UI。
- PostgreSQL 关键词检索对同义表达和大型文档集合的召回有限；只有 4G 的规模和质量证据证明不足时才评审向量检索。
- 不保存原始模型响应会降低事后调试粒度；以合成可复现案例、digest、版本和稳定失败类别补偿。

## 验证方式

- 默认关闭、未获数据处理批准、未配置 Secret、未知价格或额度不足时，网络侧没有模型请求。
- 出站测试证明只允许固定 HTTPS 主机，拒绝重定向、私网地址、用户 base URL 和代理继承。
- 合成请求抓取并断言外发字段 allowlist；不存在 Token、凭据、客户源码、完整报告、完整文档或跨 Project 数据。
- 注入文档不能改变 Prompt 版本、输出 Schema、引用候选、工具列表、网络目标或费用设置。
- 无效 Schema、未知字段、拒绝、截断、错误状态、跨 Project/未知/错误版本引用均失败关闭，原始输出不展示。
- 相同幂等请求并发提交只触发一次假模型/真实模型适配器调用；超时不自动重试。
- 单请求、Project 日额和部署日额边界分别通过并发测试；Token、延迟、费用和 traceId 可审计。
- Agent 成功、失败、超时和额度耗尽前后，原有 Finding、BaselineVersion、GateEvaluation 和 CI `0/2/64/70` 保持不变。
- 真实协议只以合成 Finding、Evidence 和文档完成 Compose 验收，并核对提供方数据处理审批和 `store=false`。

## 何时重新评估

- 需要第二模型协议、区域化部署或客户自有密钥，并能保持同等数据、费用和引用边界时。
- 真实规模证明 PostgreSQL 有界检索无法满足明确的召回或延迟目标时。
- 提供方能给出可验证的幂等请求语义，需要在超时后安全重试时。
- 单体内 Agent 出现可测量的独立扩缩、故障隔离、合规或团队发布需求时。
- 产品需要模型调用工具、自动修改代码或参与门禁时；这些改变必须另立阶段、Spec 和 ADR，不能隐式扩大本决策。
