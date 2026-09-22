# Feature Spec：治理平台 MVP `v0.3.0-platform`

- 状态：Accepted / Closed
- 阶段：2
- 主要仓库：`archguard-platform`、`archguard-scanner`、`archguard-web`、`archguard-deploy`、`archguard-docs`
- 前置：[Scanner `v0.2.0` 阶段验收](../reports/2026-09-19-scanner-v0.2.0-acceptance.md)
- 架构决策：[ADR-0001](../adr/0001-versioned-scanner-contract.md)、[ADR-0003](../adr/0003-untrusted-repository-default-deny.md)、[ADR-0004](../adr/0004-platform-modular-monolith.md)、[ADR-0005](../adr/0005-postgresql-business-source-of-truth.md)、[ADR-0007](../adr/0007-dedicated-web-client.md)
- 验收：[Platform `v0.3.0` 阶段验收](../reports/2026-09-22-platform-v0.3.0-acceptance.md)

## 用户结果

开发者在本地 Compose 环境通过 OIDC 登录后，可以创建 Project，注册一个受控挂载目录中的 Java Repository，保存版本化 RuleSet，提交和取消 ScanJob，查看扫描历史、Finding 与 Evidence，并把单次扫描中的 Finding 标记为误报或风险接受。

## 范围

### 必选能力

- Project/OIDC、成员角色、统一错误、traceId 和审计沿用 Platform 预实现资产。
- Repository 使用部署者预先挂载的只读源码根，只保存规范化相对路径。
- RuleSet 以不可变版本保存 Scanner `0.1.0` YAML、摘要、创建者和兼容版本。
- ScanJob 使用 PostgreSQL 状态、幂等键、租约、attempt token、取消和有限重试。
- Scanner 作为独立进程运行；Platform 只消费公开 CLI 与 Result Schema `0.1.0`。
- 合法 Result 经过 Schema、版本、身份、大小、唯一 ID 和引用闭合双重校验后持久化。
- Finding 支持 `OPEN`、`FALSE_POSITIVE`、`RISK_ACCEPTED`，每次变化都记录原因、版本、操作者和审计。
- 独立 Web 客户端覆盖登录、Project、Repository、RuleSet、ScanJob、Result 和 Finding 处置主流程。
- 本地 Compose 包含 Web、Platform、PostgreSQL、Keycloak 和无网络 Scanner Runner。

### 非目标

- 不上传归档、不克隆 Git、不接入 Webhook、PR 或 CI 门禁。
- 不实现基线、新旧问题分类、趋势、通知、处置到期或跨扫描自动继承。
- 不启动 Agent、Gateway、Evals、Kafka、Redis、对象存储或 Kubernetes。
- 不把 Scanner 代码、Java DTO、目标源码或数据库访问嵌入 Web。
- 不在首版 Web 提供成员管理、Identity 管理或全局管理后台。

## 用户流程

1. 用户从 Web 经本地 Keycloak 完成 Authorization Code + PKCE 登录。
2. 用户创建 Project，并在 Project 下注册受控输入根中的相对 Repository 路径。
3. 用户以 Web 表单中的 YAML 编辑器创建 RuleSet；Platform 通过固定 Scanner 版本验证后保存版本。
4. 用户选择 Repository 和 RuleSetVersion，以 `Idempotency-Key` 提交 ScanJob。
5. Platform 持久化 `QUEUED` 后认领任务，通过文件邮箱交给无网络 Runner。
6. Runner 执行 Scanner CLI，返回退出码、受限 Diagnostic 和可选报告。
7. Platform 校验并保存结果；Web 轮询任务并展示结果或安全失败原因。
8. Maintainer 对 Finding 提交误报或风险接受；Viewer 可以查看但不能修改。

## 功能需求

- FR-001：Project 成员可以分页查看 Project；只有 Maintainer 可以创建阶段 2 子资源。
- FR-002：Repository 路径必须是受控输入根下的规范化相对路径，拒绝绝对路径、遍历、链接逃逸和特殊文件。
- FR-003：Scanner project identity 固定为 `platform:<projectId>:<repositoryId>`。
- FR-004：RuleSetVersion 创建后不可修改；新内容形成新版本并保存 SHA-256。
- FR-005：无效 RuleSet 不得进入数据库，错误不得包含凭据、绝对路径或源码。
- FR-006：ScanJob 状态为 `QUEUED`、`RUNNING`、`CANCEL_REQUESTED`、`SUCCEEDED`、`FAILED`、`CANCELLED`。
- FR-007：相同 Project 内相同幂等键和相同请求返回原任务；不同请求返回冲突。
- FR-008：Scanner 退出码 `0/2` 分别形成 `PASS/VIOLATION` 成功结果，`64/70` 形成失败任务。
- FR-009：Scanner `70` 的合法部分报告只作为失败附件，不产生可处置 Finding。
- FR-010：旧 attempt 或已取消任务的迟到结果不得覆盖当前任务状态。
- FR-011：成功结果支持原始报告下载、Finding/Evidence 分页和扫描历史查询。
- FR-012：处置必须包含原因和期望版本；每次转换追加不可变历史和审计。
- FR-013：Project 存在 Repository、RuleSet 或 ScanJob 时删除返回 `409 project.not_empty`。
- FR-014：Web 必须通过发布的 Platform OpenAPI 生成客户端类型，不手写重复接口模型。

## 非功能需求

- 安全：Runner 无网络、无凭据、非 root、只读根文件系统，源码根只读；Web Token 不进入 `localStorage` 或日志。
- 隐私：Platform 不保存源码；日志、错误、审计和 Result 不出现宿主绝对路径或完整源码。
- 一致性：PostgreSQL 是 Project、RuleSet、ScanJob、Finding 和处置的唯一业务事实来源。
- 兼容：Scanner Result/Rules Schema 保持 `0.1.0`；Platform 不导入 Scanner 内部类。
- 恢复：运行中任务通过租约回收；任务目录成功、失败或取消后清理，失败隔离并在 24 小时内补偿。
- 可观测：请求、任务、Runner attempt 和审计通过 traceId/jobId 关联，结构化日志只输出 allow-list 字段。

## 验收标准

- Given 干净环境，When 执行一条 Compose 启动命令，Then Web、Platform、PostgreSQL、Keycloak 和 Runner 健康。
- Given 合法用户，When 完成登录并创建 Project，Then 只有其成员可以查看资源。
- Given 合规和违规的固定 Samples，When 分别扫描，Then 任务得到 `PASS` 与 `VIOLATION`，报告通过 `0.1.0` Schema。
- Given 重复的幂等请求，When 请求内容相同或不同，Then 分别返回原任务或稳定冲突。
- Given 运行中任务，When 用户取消或 Runner 重启，Then 状态不会被迟到结果覆盖且工作区最终清理。
- Given Finding，When Maintainer 处置，Then当前状态、历史和审计一致；Viewer 写入被拒绝。
- Given 路径穿越、链接逃逸、未知字段、悬空引用或身份不匹配，When 输入系统，Then 失败关闭且不泄漏宿主细节。

## 实施切片

1. 2A：阶段入口、Feature Spec、独立 Web ADR 和八仓库边界。
2. 2B：Platform 预实现纳入及 Web 工程治理基线。
3. 2C：Scanner `validate-rules` 与 `v0.2.1`。
4. 2D：Repository、RuleSet、迁移和 API。
5. 2E：ScanJob、Runner、Result 消费和历史。
6. 2F：Finding/Evidence 查询与处置。
7. 2G：独立 Web MVP。
8. 2H：Compose、跨仓库验收和发布。

## 退出标准

- 所有功能和非功能验收均有自动化或可复现证据。
- Scanner、Platform、Web 和 Deploy 的 PR CI 与合并后 `main` CI 成功。
- Scanner `v0.2.1`、Platform `v0.3.0`、Web `v0.1.0` 和固定 Deploy 组合可追踪。
- 空库及上一已发布数据库版本升级通过，已发布迁移未改写。
- 一份阶段 2 验收报告记录版本、摘要、命令、限制和回滚顺序。
