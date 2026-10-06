# Architecture Decision Records

保存编号化架构决策。新记录从 [`../templates/adr.md`](../templates/adr.md) 创建，并维护状态和替代关系。

## 决策索引

| ADR | 决策 | 状态 |
|---|---|---|
| [ADR-0001](0001-versioned-scanner-contract.md) | Scanner 使用独立严格的版本化契约 | Accepted |
| [ADR-0002](0002-deterministic-rule-execution.md) | Scanner 统一执行确定性 Rule | Accepted |
| [ADR-0003](0003-untrusted-repository-default-deny.md) | 不可信 Repository 默认拒绝执行和外联 | Accepted |
| [ADR-0004](0004-platform-modular-monolith.md) | Platform 初期采用模块化单体 | Accepted |
| [ADR-0005](0005-postgresql-business-source-of-truth.md) | PostgreSQL 作为 Platform 业务事实来源 | Accepted |
| [ADR-0006](0006-java-first-phased-delivery.md) | Java-first、Scanner-first 的阶段化交付顺序 | Accepted |
| [ADR-0007](0007-dedicated-web-client.md) | 阶段 2 使用独立 Web 客户端仓库 | Accepted |
| [ADR-0008](0008-baseline-and-quality-gate-semantics.md) | 冻结不可变基线、Finding 分类和质量门禁语义 | Accepted |
| [ADR-0009](0009-pr-revision-delta.md) | PR 修订差异独立于基线门禁分类 | Accepted |
| [ADR-0010](0010-agent-trust-boundary-and-model-egress.md) | 冻结 Agent 信任边界与模型数据外发 | Accepted；供应商条款由 ADR-0011、个人数据处理前置条件由 ADR-0012 部分替代 |
| [ADR-0011](0011-deepseek-official-api-egress.md) | DeepSeek 官方 API 的受限接入与真实外发关卡 | Accepted；个人审批/退出条件由 ADR-0012 部分替代，协议/技术防护及企业严格审批保留 |
| [ADR-0012](0012-personal-deepseek-release-scope.md) | 个人自用 DeepSeek 接入与阶段 4 发布范围 | Accepted；仅范围调整，真实调用需单独批准 |
| [ADR-0013](0013-personal-write-only-credential-management.md) | 个人所有者的 Web 只写凭据入口与后端加密持久化 | Accepted；只批准开发，真实调用仍关闭 |
