# Contracts

机器可执行契约由生产者仓库拥有，本目录只汇总版本、消费者和兼容状态。

| 契约 | 生产者 | 消费者 | 当前状态 |
|---|---|---|---|
| Scanner Result Schema `0.1.x` | `archguard-scanner` | Platform、Evals | `0.1.0` 随 Scanner [`v0.2.0`](https://github.com/AI-ArchGuard/archguard-scanner/releases/tag/v0.2.0) 发布并通过[阶段验收](../reports/2026-09-19-scanner-v0.2.0-acceptance.md)；Schema 仍由 Scanner 仓库唯一拥有 |
| Platform REST/OpenAPI v1 | `archguard-platform` | `archguard-web`、CI、Gateway | Platform [`v0.4.0`](https://github.com/AI-ArchGuard/archguard-platform/releases/tag/v0.4.0) 已实现并发布[治理扩展 OpenAPI](https://github.com/AI-ArchGuard/archguard-platform/blob/v0.4.0/openapi/governance-v1.json)；Gateway 仍未启用 |
| Platform Finding 指纹 `platform-finding-v1` | `archguard-platform` | Platform 基线/门禁、Web | 3B 的[算法设计](https://github.com/AI-ArchGuard/archguard-platform/blob/main/docs/technical-design/v0.4-governance-3b-contracts.md)和[固定 Samples 向量](https://github.com/AI-ArchGuard/archguard-samples/tree/main/governance)覆盖现有 15 个 Finding；Scanner Schema 保持 `0.1.0` |
| PR 修订差异只读 API `0.2.0` | `archguard-platform` | `archguard-web`、Deploy 验收 | [ADR-0009](../adr/0009-pr-revision-delta.md) 已接受；[Platform 固定读取契约](https://github.com/AI-ArchGuard/archguard-platform/blob/v0.4.0/openapi/governance-read-v1.json)与 Web `v0.2.0` 已通过 Compose 闭环；PR `RESOLVED` 不计入基线门禁 |
| MCP Tool Schema | `archguard-mcp-gateway` | Agent/MCP 客户端 | 阶段 5 未启用 |
| [Agent API 0.1.0](https://github.com/AI-ArchGuard/archguard-platform/blob/main/openapi/agent-v1.json) 与 [模型输出 Schema 0.1.0](https://github.com/AI-ArchGuard/archguard-platform/blob/main/src/main/resources/contracts/agent-model-output-0.1.0.schema.json) | `archguard-platform` | Web、[Samples 合成向量](https://github.com/AI-ArchGuard/archguard-samples/tree/main/agent)；未来 Evals | 4C–4G 合成运行时/Web 消费已验证；4H 未正式发布。[ADR-0012](../adr/0012-personal-deepseek-release-scope.md)只调整个人范围，不改变契约或取消 Project/引用校验；真实外发仍关闭 |

## 兼容规则

个人凭据管理API由Platform唯一拥有，Web消费固定快照；边界见[ADR-0013](../adr/0013-personal-write-only-credential-management.md)。现有加密只写入口不触发模型，不改变Agent Output或Scanner Schema，也不表示真实模型已启用。

[ADR-0015](../adr/0015-approved-deepseek-1017-mapping.md)冻结的个人启用输入`0.4.0`已有生产者和消费者，映射`DeepSeek-V4.1-Flash-1017`、别名/单元素响应模型`deepseek-flash`与价格`deepseek-flash-context-peak-usd-2026-10-15`保持现有兼容线。实际发送前须重新核对官方依据、相关PR/main CI与运行绑定；旧确认、失败批次和剩余次数不升级或复用，历史读取/撤销/结算保留。

[ADR-0016](../adr/0016-personal-project-agent-use.md)的日常Project授权/请求由Platform另立版本化机器契约，当前待交付；Web后续消费固定快照。它绑定普通资源选择、不可变最小输入、当前所有者/Project/凭据/运行版本及独立次数/预算/有效期，不能复用合成`SYNTHETIC_ACCEPTANCE`模板或批准。原输出Schema、合成API与历史保持兼容，迁移只追加；日常与合成批准分开追溯，共享Project/部署技术额度。本索引不复制DTO或创建占位Schema，合入顺序仍为Docs/main CI→生产者/main CI→消费者/main CI→Deploy固定候选。

- 生产者发布 Schema、示例和提供方测试，消费者不得导入生产者内部类。
- 开发期契约使用独立 `0.MINOR.PATCH`；破坏性变化提升 MINOR，并保留并行迁移窗口。
- 正常顺序为 Spec/ADR → Samples → 生产者 → 消费者 → Deploy 兼容组合。
- 服务不共享数据库；无共同兼容线、未知字段或无效引用失败关闭。
- 契约字段定义只在生产者机器制品中维护，本索引不复制 Schema。
