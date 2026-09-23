# Feature Spec：持续治理闭环 `v0.4.0-governance`

- 状态：Accepted；3A 已完成，3B 契约冻结，后续切片按顺序关卡执行
- 阶段：3
- Issue：[AI-ArchGuard/archguard-docs#25](https://github.com/AI-ArchGuard/archguard-docs/issues/25)
- 主要仓库：`archguard-platform`、`archguard-web`、`archguard-deploy`、`archguard-samples`、`archguard-docs`
- 条件参与：`archguard-scanner` 仅在 3B 证明现有 Finding 数据不足以形成稳定逻辑指纹时重新评审；默认不修改
- 前置：[Platform `v0.3.0` 阶段验收](../reports/2026-09-22-platform-v0.3.0-acceptance.md)
- 架构决策：[ADR-0001](../adr/0001-versioned-scanner-contract.md)、[ADR-0003](../adr/0003-untrusted-repository-default-deny.md)、[ADR-0004](../adr/0004-platform-modular-monolith.md)、[ADR-0005](../adr/0005-postgresql-business-source-of-truth.md)、[ADR-0008](../adr/0008-baseline-and-quality-gate-semantics.md)

## 阶段入口关卡

本 Spec、ADR-0008、索引和路线图构成 3A 的完整交付。3A Docs PR #26 已合并，合并后的 `main` CI 已成功，3B 因而获准冻结跨仓库契约。3B 的 [Platform 设计与 OpenAPI](https://github.com/AI-ArchGuard/archguard-platform/blob/main/docs/technical-design/v0.4-governance-3b-contracts.md)及 [Samples 固定向量](https://github.com/AI-ArchGuard/archguard-samples/tree/main/governance)提供消费方证据；3C 仍须等待全部 3B PR 合并后的相关 `main` CI 成功。本阶段入口不创建验收报告；阶段验收报告只在 3H 形成。

## 问题与用户价值

阶段 2 已能在受控本地目录上手动扫描并查看、处置单次结果，但尚不能把 Git 提交、PR、CI、历史基线和跨扫描例外连接成持续治理闭环。Maintainer 无法稳定判断一次变更新增、保留或解决了哪些问题，也无法让新增高风险问题可靠阻断 CI。

阶段 3 的目标是让团队在不向 Platform 交付 Git 凭据或源码的前提下，把本地 Scanner 的确定性报告提交给 Platform，与不可变基线比较，得到可审计、可重复的质量门禁结果，并在 Web 查看 PR、趋势和有期限例外。

## 用户结果

1. Maintainer 为 Project、Repository、目标分支和 RuleSetVersion 选择一个成功扫描作为不可变基线。
2. PR 在自己的 CI 工作区运行 Scanner，并向 Platform 提交报告和 Git 元数据。
3. Platform 使用稳定逻辑指纹把候选问题分类为 `NEW`、`EXISTING`、`RESOLVED`。
4. 默认策略只让未被有效例外覆盖的新增 `high` 或 `critical` Finding 产生 `FAIL`，CI 退出 `2`。
5. Maintainer 可以创建有范围、有原因、有创建者和到期时间的 `PolicyException`；历史扫描不被改写。
6. 修复违规后重新扫描，问题分类为 `RESOLVED`，门禁返回 `PASS`。
7. Web 展示 PR 门禁、新增/存量/已解决问题、趋势和例外状态。

## 范围

### Git 与报告提交

- 内部领域模型保持 Git Provider 无关；阶段 3 只实现 GitHub Adapter。
- CI 在其已有工作区运行固定版本 Scanner，并向 Platform 提交未经改写的报告、报告摘要、Repository 身份、commit SHA、目标分支、PR 元数据和 RuleSetVersion。
- Platform 不保存 Git 凭据，不远程 clone 或 fetch 源码，不接收源码归档。
- 报告提交使用 Project 内幂等键和内容摘要；相同提交返回同一结果，不产生重复任务或 Finding。
- Platform 先按已发布 Scanner Result Schema `0.1.0` 校验报告，再校验 Git 元数据、Project/Repository/RuleSetVersion 归属和提交顺序。

### 基线与差异分类

- 基线按 `Project + Repository + 目标分支 + RuleSetVersion` 隔离；每个基线版本绑定成功扫描、commit SHA、报告摘要、创建者和创建时间。
- 基线版本不可修改或删除；提升新扫描创建新版本，重新提升只能切换活动版本并追加审计，不改写已有版本。
- 初版“增量”只指完整报告之间的 Finding 差异分类，不进行部分文件或增量 AST 扫描。
- Platform 依据稳定逻辑指纹关联 Finding。指纹不得只依赖 Scanner Finding ID、行号、列号、输入顺序、消息文本或时间戳。
- 比较结果固定为 `NEW`、`EXISTING`、`RESOLVED`；相同输入集合在任意顺序下得到相同分类。
- RuleSetVersion 不同的扫描不得静默复用基线；缺失或不兼容基线必须得到显式状态或 `ERROR`。

### 例外与质量门禁

- 跨扫描例外建模为独立 `PolicyException`，至少包含 Project、Repository、目标分支、规则或指纹范围、原因、创建者、生效时间、到期时间和版本。
- 例外只影响当前门禁求值，不修改历史报告、Finding、分类或既有门禁结果。
- 门禁结果固定为 `PASS`、`FAIL`、`ERROR`。
- 默认策略仅由未被有效例外覆盖的 `NEW` 且严重性为 `high` 或 `critical` 的 Finding 产生 `FAIL`；`EXISTING` 默认不阻断。
- 报告无效、契约不兼容、必要元数据缺失或求值失败产生 `ERROR`，不得降级为 `PASS`。
- CI 退出码固定为：`0` 表示通过，`2` 表示治理违规，`64` 表示配置错误，`70` 表示执行或契约错误。

### GitHub、Webhook 与 Web

- GitHub Webhook 必须验证签名和事件类型，限制时间窗口并防重放，以 delivery ID 幂等处理。
- 同一 PR 的重复、乱序和迟到事件不得覆盖较新 commit 的权威门禁结果；旧 commit 结果可以保留审计，但不能成为当前 PR 状态。
- GitHub 状态发布只消费 Platform 已持久化的门禁事实；失败重试不得重复创建业务结果。
- Web 通过 Platform OpenAPI 展示 PR、基线、趋势、`NEW`/`EXISTING`/`RESOLVED`、例外和门禁；不直连 GitHub 或数据库。

## 功能需求

- FR-001：Maintainer 可以在同一 Project 内注册 Git Provider 无关的 Repository 身份和 GitHub 连接元数据；Platform 不接收 Git 凭据。
- FR-002：报告提交必须绑定 Project、Repository、commit SHA、目标分支和 RuleSetVersion，并以 Project 内幂等键和报告摘要去重。
- FR-003：相同报告和元数据重复提交返回原结果；同一幂等键对应不同内容返回稳定冲突。
- FR-004：只有成功且归属一致的扫描可以被提升为基线；基线版本不可变。
- FR-005：Platform 使用版本化指纹算法关联 Finding，并保存算法版本和输入摘要。
- FR-006：每次比较完整产生 `NEW`、`EXISTING`、`RESOLVED` 集合，分类不依赖报告数组顺序或源码行号漂移。
- FR-007：门禁保存策略版本、基线版本、候选扫描、三类计数、命中例外和 `PASS`/`FAIL`/`ERROR` 结果。
- FR-008：Maintainer 可以创建有期限的 `PolicyException`；Viewer 和跨 Project 主体不得写入。
- FR-009：Webhook 对错误签名、重放、未知事件、乱序和迟到事件安全失败或显式忽略。
- FR-010：CI 可以轮询或读取最终门禁，并稳定映射到退出码 `0/2/64/70`。
- FR-011：Web 可以按 PR 和扫描查看门禁、分类、趋势、基线和例外的当前状态与历史。
- FR-012：报告提交、基线提升、门禁求值、例外生命周期和 Webhook 处理全部写入审计并关联 traceId。

## 非功能需求

- 安全：所有读取和写入都验证 Project 边界；Webhook secret、CI 凭据和报告正文不进入日志、错误或审计正文。
- 确定性：相同基线、候选报告、策略和求值时间产生相同分类与门禁；集合排序只影响呈现，不影响结果。
- 一致性：PostgreSQL 是基线、分类、例外、门禁和事件幂等事实来源；外部 GitHub 状态不是业务事实来源。
- 可恢复：重复投递、进程重启和发布重试不会重复创建业务实体；失败可从已持久化状态安全重试。
- 兼容：Scanner Result/Rules Schema 默认保持 `0.1.0`；阶段 3 不导入 Scanner 内部类。
- 隐私：Platform 不保存源码，只保存最小 Git 元数据、原始 Scanner 报告和治理事实。

## 验收标准

- Given 相同报告和 Git 元数据，When 重复提交，Then 不产生重复任务、Finding、分类或门禁结果。
- Given 已创建的基线版本，When Maintainer 再次提升扫描，Then 创建新版本或切换活动版本，既有版本内容不变。
- Given 相同基线和候选 Finding 集合，When 任意调整输入顺序，Then `NEW`、`EXISTING`、`RESOLVED` 分类完全一致。
- Given 仅源码行号变化的同一逻辑违规，When 与基线比较，Then 不被错误分类为 `NEW`。
- Given 不同 RuleSetVersion，When 请求比较，Then 不静默复用不兼容基线。
- Given 新增 `high` 或 `critical` Finding，When 无例外、例外有效或例外已到期，Then 分别得到 `FAIL`、`PASS`、`FAIL`。
- Given 错误签名、重放、乱序或迟到 Webhook，When Platform 处理，Then 安全失败或显式忽略，较新 commit 状态不被覆盖。
- Given 非成员或另一 Project 的成员，When 读取、提交、提升基线或创建例外，Then 使用隐藏式未找到或明确拒绝，且不泄漏资源存在性。
- Given PR 引入非法依赖后又修复，When CI 运行两次，Then 首次分类为 `NEW`、门禁 `FAIL`、退出 `2`，第二次分类为 `RESOLVED`、门禁 `PASS`、退出 `0`。
- Given 任一治理写操作，When 成功、拒绝或失败，Then 审计记录主体、Project、动作、目标、结果、时间和 traceId，不记录凭据或源码。
- Given 各切片完成，When 执行 PR CI、合并后 `main` CI 和最终 Compose 验收，Then 全部成功且证据可追踪。

## 实施切片

1. 3A：Docs 完成 Feature Spec、ADR-0008、范围冻结和阶段入口；只进行评审。
2. 3B：Platform、Docs、Samples 冻结 Git 修订、报告提交、门禁结果和 Finding 指纹契约。
3. 3C：Platform 实现不可变基线和 `NEW`、`EXISTING`、`RESOLVED` 分类。
4. 3D：Platform 实现质量门禁、跨扫描例外、到期与审计。
5. 3E：Platform、Deploy 实现 GitHub Webhook、CI 报告提交和退出码闭环。
6. 3F：Web 实现 PR、基线、趋势、例外和门禁页面。
7. 3G：全部已启用仓库完成安全、幂等、乱序事件、恢复和固定 Samples 加固。
8. 3H：Deploy、Docs 完成 Compose 验收、版本发布、兼容矩阵和阶段报告。

切片按顺序进入 `Current`。只有前一切片合并后的相关 `main` CI 成功，下一切片才能从 `Next` 进入 `Current`。

## 明确非目标

- 不启动 Agent、MCP Gateway 或正式 Evals。
- 不使用 LLM 解释、判定或自动修复治理问题。
- 不实现 GitLab、Bitbucket 或第二个 Git Provider。
- 不由 Platform clone、fetch 或持有 Git 凭据。
- 不实现部分文件扫描或增量 AST 解析。
- 不引入 Kafka、Redis、Kubernetes、远程容器 Registry 或供应链签名。
- 不自动修改 PR、源码或 RuleSet。
- 不在 3A 创建阶段验收报告或修改任何运行时代码。
- 不修改现有 Scanner Schema；只有 3B 的可复现实验证明现有数据无法形成稳定逻辑指纹时，才单独提出兼容方案和评审。

## 兼容、发布与回滚

目标兼容顺序为 Docs 范围与 ADR → 3B 契约与固定 Samples → Platform 领域和 API → GitHub/CI Adapter → Web → Deploy → Docs 阶段报告。Scanner 默认沿用 `v0.2.1` 和 Result/Rules Schema `0.1.0`。

回滚先停止 GitHub 状态发布和 CI 门禁入口，再回退 Web 与 Platform 应用；已发布的 Flyway 迁移不回写。不可变基线、历史分类、例外、门禁和审计保留。若指纹算法需要升级，使用新算法版本并重新计算新的比较结果，不改写既有结果。

## 风险与待验证项

- 3B 已用阶段 2 的三份固定报告和 15 个 Finding 验证当前 Schema 可覆盖依赖、组件、复杂度和循环类逻辑身份；Scanner Schema 保持 `0.1.0`。
- GitHub commit ancestry 在 Platform 不持有 Git 凭据且不 clone 的条件下只能依赖经过认证的事件和 CI 元数据；3B/3E 必须明确可信边界和迟到判断。
- 例外范围过宽会掩盖新增风险；3D 应默认选择最小规则/指纹范围并限制到期时间。
- Project #2 的状态选项为 `Todo`、`In Progress`、`Done`、`Blocked`；切片只有通过前置 `main` CI 后才从 `Todo` 进入 `In Progress`。
