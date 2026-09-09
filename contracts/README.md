# Contracts

机器可执行契约由生产者仓库拥有，本目录只汇总版本、消费者和兼容状态。

| 契约 | 生产者 | 消费者 | 当前状态 |
|---|---|---|---|
| Scanner Result Schema `0.1.x` | `archguard-scanner` | Platform、Evals | S2 目标，尚未发布 |
| Platform REST/OpenAPI | `archguard-platform` | UI、CI、Gateway | 阶段 2 预实现资产，正式消费边界未冻结 |
| MCP Tool Schema | `archguard-mcp-gateway` | Agent/MCP 客户端 | 阶段 5 未启用 |
| Agent Output Schema | `archguard-platform` | UI、Evals | 阶段 4 未启用 |

## 兼容规则

- 生产者发布 Schema、示例和提供方测试，消费者不得导入生产者内部类。
- 开发期契约使用独立 `0.MINOR.PATCH`；破坏性变化提升 MINOR，并保留并行迁移窗口。
- 正常顺序为 Spec/ADR → Samples → 生产者 → 消费者 → Deploy 兼容组合。
- 服务不共享数据库；无共同兼容线、未知字段或无效引用失败关闭。
- 契约字段定义只在生产者机器制品中维护，本索引不复制 Schema。
