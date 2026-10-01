# Contracts

机器可执行契约由生产者仓库拥有，本目录只汇总版本、消费者和兼容状态。

| 契约 | 生产者 | 消费者 | 当前状态 |
|---|---|---|---|
| Scanner Result Schema `0.1.x` | `archguard-scanner` | Platform、Evals | `0.1.0` 随 Scanner [`v0.2.0`](https://github.com/AI-ArchGuard/archguard-scanner/releases/tag/v0.2.0) 发布并通过[阶段验收](../reports/2026-09-19-scanner-v0.2.0-acceptance.md)；Schema 仍由 Scanner 仓库唯一拥有 |
| Platform REST/OpenAPI v1 | `archguard-platform` | `archguard-web`、CI、Gateway | Platform [`v0.4.0`](https://github.com/AI-ArchGuard/archguard-platform/releases/tag/v0.4.0) 已实现并发布[治理扩展 OpenAPI](https://github.com/AI-ArchGuard/archguard-platform/blob/v0.4.0/openapi/governance-v1.json)；Gateway 仍未启用 |
| Platform Finding 指纹 `platform-finding-v1` | `archguard-platform` | Platform 基线/门禁、Web | 3B 的[算法设计](https://github.com/AI-ArchGuard/archguard-platform/blob/main/docs/technical-design/v0.4-governance-3b-contracts.md)和[固定 Samples 向量](https://github.com/AI-ArchGuard/archguard-samples/tree/main/governance)覆盖现有 15 个 Finding；Scanner Schema 保持 `0.1.0` |
| PR 修订差异只读 API `0.2.0` | `archguard-platform` | `archguard-web`、Deploy 验收 | [ADR-0009](../adr/0009-pr-revision-delta.md) 已接受；[Platform 固定读取契约](https://github.com/AI-ArchGuard/archguard-platform/blob/v0.4.0/openapi/governance-read-v1.json)与 Web `v0.2.0` 已通过 Compose 闭环；PR `RESOLVED` 不计入基线门禁 |
| MCP Tool Schema | `archguard-mcp-gateway` | Agent/MCP 客户端 | 阶段 5 未启用 |
| [Agent API 0.1.0](https://github.com/AI-ArchGuard/archguard-platform/blob/main/openapi/agent-v1.json) 与 [模型输出 Schema 0.1.0](https://github.com/AI-ArchGuard/archguard-platform/blob/main/src/main/resources/contracts/agent-model-output-0.1.0.schema.json) | `archguard-platform` | Web、[Samples 合成向量](https://github.com/AI-ArchGuard/archguard-samples/tree/main/agent)；未来 Evals | 4C–4G 已实现并验证合成运行时和 Web 消费；4H 候选组合验收中，未正式发布。引用须经 Project 授权和服务端验证；真实外发仍关闭 |

## 兼容规则

- 生产者发布 Schema、示例和提供方测试，消费者不得导入生产者内部类。
- 开发期契约使用独立 `0.MINOR.PATCH`；破坏性变化提升 MINOR，并保留并行迁移窗口。
- 正常顺序为 Spec/ADR → Samples → 生产者 → 消费者 → Deploy 兼容组合。
- 服务不共享数据库；无共同兼容线、未知字段或无效引用失败关闭。
- 契约字段定义只在生产者机器制品中维护，本索引不复制 Schema。
