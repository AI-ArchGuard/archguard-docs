# 文档库后续交付计划

- 状态：Ready
- 生效日期：2026-09-10
- 适用范围：阶段 1–7
- 阶段来源：[产品路线图](../product/roadmap.md)
- 编写规则：[文档编写与生命周期规范](documentation-standard.md)

## 目标

本计划把阶段 1–7 的产品交付转换为最小、可维护的文档产物。它不创建新的里程碑体系，不替代产品路线图，也不提前为尚未启用的能力编写占位设计。

文档库始终满足以下结果：

1. 新成员从根 README 能在三次跳转内找到当前范围、架构、契约或退出证据。
2. 每个事实只有一个权威位置；实现细节与源码同仓，跨仓库结论留在本库。
3. 当前事实、目标状态和历史证据明确分开。
4. 每进入一个阶段，只增加该阶段确实需要的文档；阶段结束后删除临时材料。
5. 机器契约由生产者仓库发布，本库只维护版本、所有者、消费者和兼容状态。

## 当前基线

- 阶段 0 正在远端收口；Docs 已发布，另外六个仓库待提交并通过托管 CI，当前验收状态记录在 `reports/`。
- 阶段 1 尚未正式进入；Scanner S1 已在本地通过，S2 必须等待阶段 0 关卡关闭。
- Platform 成果作为阶段 2 预实现资产保留，正式功能扩展冻结。
- 阶段 3–7 未启用，不创建其 Feature Spec、Technical Design 或验收报告占位文件。
- 历史 M、D、G、V 编号体系已从本地文档库删除；远端历史 Issue/PR 不再作为当前事实来源。

## 判断一份材料应该放在哪里

| 问题 | 放置位置 | 不应放置的位置 |
|---|---|---|
| 它定义产品结果、范围或退出条件吗？ | `product/` 或当前阶段 `requirements/` | Issue 评论、实现仓库设计文档 |
| 它影响三个以上组件或多个仓库边界吗？ | `architecture/`，必要时新增 ADR | 单个模块 README |
| 它是长期且代价较高的技术决策吗？ | `adr/` | 路线图正文、验收报告 |
| 它是 JSON Schema、OpenAPI 或工具 Schema 吗？ | 生产者仓库；`contracts/` 建索引 | 在本库复制一份 Schema |
| 它解释模块、类、算法或适配器实现吗？ | 对应仓库 `docs/technical-design/` | 本库 `architecture/` |
| 它是本次任务计划、评审意见或测试日志吗？ | Issue/PR/CI | 新建长期 Markdown |
| 它是阶段退出、正式发布或专项演练证据吗？ | `reports/` | Feature Spec、README |
| 它是部署、备份、恢复或告警操作吗？ | 能力实现并演练后进入 `operations/` | 未启用阶段的占位 runbook |

无法通过上表确定归属时，默认不新建文件，先在 Issue/PR 中完成讨论。

## 阶段化交付矩阵

| 阶段 | 进入时允许新增 | 实施中维护 | 退出时必须形成 | 暂不创建 |
|---|---|---|---|---|
| 1 Java Scanner | 当前 Scanner Feature Spec；必要的统一模型 ADR | Scanner 契约索引、Feature Spec 状态、术语 | Scanner 发布说明与一份阶段退出报告 | Platform、Agent、MCP、Evals 详细设计 |
| 2 Platform MVP | Platform Feature Spec；Scanner→Platform 集成 ADR（若现有 ADR 不足） | 容器架构、REST/OpenAPI 和 Scanner 契约索引、运维入口 | Platform 阶段退出报告、可运行部署说明 | 微服务拆分、Kafka、高可用设计 |
| 3 持续治理 | Governance Feature Spec；基线/质量门禁语义 ADR | Webhook、CI 退出码、规则和基线版本契约索引 | CI 闭环演示和阶段退出报告 | Agent、MCP 或模型评估文档 |
| 4 Java Agent | Agent Feature Spec；安全边界和输出可信度 ADR | Agent Output Schema 索引、模型/Prompt/知识库版本规则 | Agent 回退、费用和可追溯性证据 | 自动改代码、自动合并、任意 Shell 能力 |
| 5 Go MCP | MCP Gateway Feature Spec；工具所有权和权限 ADR | 工具 Schema 索引、鉴权/限流/超时/取消运维说明 | 工具审计和故障隔离证据 | 在 Gateway 复制 Platform 业务说明 |
| 6 Python Evals | Evals Feature Spec；质量阈值和数据集版本策略 | 数据集、评估输出和候选/基线契约索引 | 回归与安全质量门禁报告 | 将 Evals 写成线上强依赖 |
| 7 生产化与多语言 | 生产化 Feature Spec；新语言接入 ADR（有真实需求时） | 部署、备份、恢复、告警、发布和语言适配契约索引 | `v1.0.0` 发布证据和演练记录 | 无容量证据的 Kubernetes/高可用方案 |

每一行的“进入时允许新增”都是上限，不是必须创建的文件清单。现有文档能够表达清楚时，只更新现有文档。

## 阶段 1 当前执行计划

### S2：统一模型与 Schema

- 本库不再创建第二份 Scanner 需求；继续维护 `requirements/scanner-v0.2-feature-spec.md`。
- `archguard-scanner` 拥有 `0.1.0` JSON Schema、有效/无效样例和契约测试。
- Schema 合并后更新 `contracts/README.md`：记录准确制品路径、版本、状态和消费者。
- 只有当稳定 ID、扩展字段或兼容规则改变现有长期决策时才新增 ADR。
- S2 测试输出留在 Scanner PR/CI，不创建 S2 验收报告。

### S3–S6：解析、规则与 CLI

- Java parser、规则算法、资源上限和 CLI 组合设计留在 Scanner 的 `docs/technical-design/`。
- 用户可观察行为发生变化时，同步当前 Feature Spec、Scanner README 和契约示例。
- 新术语必须先确认是否跨仓库复用；只有跨仓库概念才进入本库术语表。
- 每个切片的完成证据留在对应 PR；本库只在阶段状态或公共边界变化时修改。

### S7：样例、重复性和发布

- `archguard-samples` 为每个样例维护输入目的、预期 Finding/Diagnostic 和验证命令。
- Scanner 发布前冻结 Schema `0.1.x` 兼容线、CLI 退出码和支持矩阵。
- 阶段 1 退出时只新增一份正式报告，报告引用 CI、Schema、样例和性能证据，不复制完整日志。
- 退出报告通过后，路线图、根 README、Feature Spec、契约索引和 Changelog 在同一 PR 中切换状态。

## 后续文件按需创建规则

以下名称仅定义未来命名，不提前创建空文件：

| 触发条件 | 建议文件 |
|---|---|
| 阶段 2 正式进入 | `requirements/platform-v0.3-feature-spec.md` |
| 阶段 3 正式进入 | `requirements/governance-v0.4-feature-spec.md` |
| 阶段 4 正式进入 | `requirements/agent-v0.5-feature-spec.md` |
| 阶段 5 正式进入 | `requirements/mcp-gateway-v0.6-feature-spec.md` |
| 阶段 6 正式进入 | `requirements/evals-v0.7-feature-spec.md` |
| 阶段 7 正式进入 | `requirements/production-v1.0-feature-spec.md` |
| 部署能力已实现并完成演练 | `operations/deployment.md`、`backup-restore.md`、`incident-response.md` 等具体文档 |
| 一个阶段达到全部退出条件 | `reports/YYYY-MM-DD-<stage>-acceptance.md` |

新增文件必须同时加入所在目录 README；属于长期基线的文件还必须进入 Docs CI 必备清单。

## 文档变更节奏

### 每个 PR

- PR 描述回答“是否影响产品范围、架构、契约、运维或用户行为”。
- 有影响时更新唯一事实源；无影响时不得为了留痕新增说明文件。
- 自动检查本地链接、旧编号、必备文件、空白、许可证和敏感信息。

### 每个实现切片

- 开始前确认 Feature Spec 已经覆盖用户结果和验收，不创建切片级需求副本。
- 合并前由生产者验证契约和示例；消费者变更遵守兼容顺序。
- 完成状态只写入当前 Feature Spec/路线图，具体测试留在 PR/CI。

### 每个阶段入口

- 确认上一阶段退出报告为 Passed/Closed。
- 将本阶段 Feature Spec 从 Draft 调整为 Ready，并确认仓库、契约和安全所有者。
- 只创建本阶段所需文档，未来阶段继续保持未启用。

### 每个阶段出口

- 创建一份阶段退出报告；报告只引用可复现证据。
- 同步路线图、Feature Spec、契约索引、根 README 和 Changelog。
- 删除临时迁移说明、重复检查表和已经被权威文档吸收的草稿。

### 每季度或重大路线变更后

- 检查当前事实与代码、发布制品和远端任务是否一致。
- 检查孤立文档、断链、重复术语、过期状态和未声明消费者。
- 路线变更先新增 ADR，再更新路线图和阶段关卡；不复活旧编号体系。

## 远端历史记录治理

- 已关闭 Issue/PR 是历史审计记录，不改写正文；其中的旧编号不再具有规范效力。
- 开放 Issue/PR 若仍用于开发，先增加“已由阶段 0–7 路线取代”的迁移说明，再把范围映射到当前阶段或关闭为 superseded。
- 未到阶段的 Gateway、Evals 和 Platform 后续项应保持 deferred，不得因旧 Issue 存在而提前启用。
- Wiki 当前未启用；未来若启用，只做导航和阅读入口，不复制本仓库内容。
- 任何远端描述与本仓库冲突时，以已接受 ADR、产品路线图和当前 Feature Spec 为准。

## 所有权与审查

| 变更 | 必需审查视角 |
|---|---|
| 产品范围、阶段状态 | 产品所有者 + 对应实现仓库所有者 |
| 跨仓库架构和 ADR | 总体架构所有者 + 受影响仓库所有者 |
| 契约索引 | 生产者 + 至少一个消费者 |
| 安全边界 | 安全审查者 + 能力所有者 |
| 运维说明 | 部署所有者 + 实际演练执行者 |
| 阶段退出报告 | 验证执行者 + 阶段所有者 |

同一人可以承担多个角色，但审查意见必须覆盖这些视角。

## 计划完成定义

- 本阶段所需文档能从根 README 导航，且没有提前创建未来阶段占位文档。
- 权威事实、生产者制品和消费者引用一致。
- 所有状态有证据，所有报告可复现，所有链接有效。
- 远端开放任务已映射到阶段 0–7 或明确标记为 superseded/deferred。
- 文档数量增长能够对应真实产品能力、契约、决策或正式证据。
