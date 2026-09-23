# Contracts

机器可执行契约由生产者仓库拥有，本目录只汇总版本、消费者和兼容状态。

| 契约 | 生产者 | 消费者 | 当前状态 |
|---|---|---|---|
| Scanner Result Schema `0.1.x` | `archguard-scanner` | Platform、Evals | `0.1.0` 随 Scanner [`v0.2.0`](https://github.com/AI-ArchGuard/archguard-scanner/releases/tag/v0.2.0) 发布并通过[阶段验收](../reports/2026-09-19-scanner-v0.2.0-acceptance.md)；Schema 仍由 Scanner 仓库唯一拥有 |
| Platform REST/OpenAPI v1 | `archguard-platform` | `archguard-web`、CI、Gateway | 阶段 2 已发布 Project、Repository、RuleSet、ScanJob、Result 和 Finding 处置边界；3B 的[治理扩展 OpenAPI](https://github.com/AI-ArchGuard/archguard-platform/blob/main/openapi/governance-v1.json)已冻结，运行时端点待 3C–3E 实现 |
| Platform Finding 指纹 `platform-finding-v1` | `archguard-platform` | Platform 基线/门禁、Web | 3B 的[算法设计](https://github.com/AI-ArchGuard/archguard-platform/blob/main/docs/technical-design/v0.4-governance-3b-contracts.md)和[固定 Samples 向量](https://github.com/AI-ArchGuard/archguard-samples/tree/main/governance)覆盖现有 15 个 Finding；Scanner Schema 保持 `0.1.0` |
| MCP Tool Schema | `archguard-mcp-gateway` | Agent/MCP 客户端 | 阶段 5 未启用 |
| Agent Output Schema | `archguard-platform` | UI、Evals | 阶段 4 未启用 |

## 兼容规则

- 生产者发布 Schema、示例和提供方测试，消费者不得导入生产者内部类。
- 开发期契约使用独立 `0.MINOR.PATCH`；破坏性变化提升 MINOR，并保留并行迁移窗口。
- 正常顺序为 Spec/ADR → Samples → 生产者 → 消费者 → Deploy 兼容组合。
- 服务不共享数据库；无共同兼容线、未知字段或无效引用失败关闭。
- 契约字段定义只在生产者机器制品中维护，本索引不复制 Schema。
