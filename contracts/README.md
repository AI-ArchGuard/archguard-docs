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

个人凭据管理的增量 API 由 Platform 唯一拥有，Web 消费固定快照；开发边界见 [ADR-0013](../adr/0013-personal-write-only-credential-management.md)。当前待实现，不复制 DTO/Schema、不改变 Agent Output 或 Scanner Schema，也不表示真实模型已启用。

[ADR-0015](../adr/0015-approved-deepseek-1017-mapping.md)冻结的最小跟进目标是 Platform 生产者拥有的个人启用输入 Schema `0.4.0`：本次映射为 `DeepSeek-V4.1-Flash-1017`，别名和单元素响应模型集合仍为 `deepseek-flash`，上下文价格版本仍为 `deepseek-flash-context-peak-usd-2026-10-15`，其余限制/有效期/来源/批准引用/凭据要求不变。该版本尚待生产者交付；Web 随后消费生成契约并只提交新确认。旧 Schema/确认、费用历史和迁移保留；旧映射不得用于新真实发送，历史读取、撤销和结算继续支持。本索引不复制 DTO；Docs/main CI → Platform 契约/测试/main CI → Web 消费/测试/main CI → Deploy 显式候选/测试/main CI → 新鲜运行绑定的顺序不可由版本号替代。

- 生产者发布 Schema、示例和提供方测试，消费者不得导入生产者内部类。
- 开发期契约使用独立 `0.MINOR.PATCH`；破坏性变化提升 MINOR，并保留并行迁移窗口。
- 正常顺序为 Spec/ADR → Samples → 生产者 → 消费者 → Deploy 兼容组合。
- 服务不共享数据库；无共同兼容线、未知字段或无效引用失败关闭。
- 契约字段定义只在生产者机器制品中维护，本索引不复制 Schema。
