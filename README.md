# ArchGuard Documentation

ArchGuard 的跨仓库产品、架构、工程规范、契约索引和阶段证据事实来源。

## 当前状态

- 最终定位：Java-first、语言无关架构、AI 增强的软件架构治理平台。
- 阶段 0 `v0.1.0-foundation` 已关闭：七仓库 Foundation PR 已合并，合并后的 `main` CI 全部成功。
- 阶段 1 `v0.2.0-scanner` 已通过[阶段验收](reports/2026-09-19-scanner-v0.2.0-acceptance.md)并关闭；Scanner `v0.2.0` Release、Result Schema `0.1.0` 和固定 Samples 已发布。
- 阶段 2 `v0.3.0-platform` 已通过[阶段验收](reports/2026-09-22-platform-v0.3.0-acceptance.md)并关闭；Scanner `v0.2.1`、Platform `v0.3.0`、Web `v0.1.0` 和 Deploy `v0.3.0` 已发布。
- 阶段 3 `v0.4.0-governance` 已通过[阶段验收](reports/2026-09-27-governance-v0.4.0-acceptance.md)并关闭；Platform `v0.4.0`、Web `v0.2.0`、Deploy `v0.4.0` 已发布，Scanner Schema 保持 `0.1.0`。PR 修复差异独立于基线门禁，见 [ADR-0009](adr/0009-pr-revision-delta.md)。
- 阶段 4 `v0.5.0-agent` 的 4A–4G 合成范围完成，4H [合成 Compose](https://github.com/AI-ArchGuard/archguard-deploy/blob/main/docs/agent-synthetic-compose-acceptance.md)和[本地回滚/恢复](https://github.com/AI-ArchGuard/archguard-deploy/blob/main/docs/agent-rollback-rehearsal.md)已验证，正式发布/退出尚未完成。[ADR-0012](adr/0012-personal-deepseek-release-scope.md)已接受个人自用版范围调整，[Feature Spec](requirements/agent-v0.5-feature-spec.md)继续要求真实适配器、双开关、单独获批的合成真实验收、制品和唯一报告。[#43](https://github.com/AI-ArchGuard/archguard-platform/issues/43)继续开放、真实调用关闭；[ADR-0010](adr/0010-agent-trust-boundary-and-model-egress.md)/[ADR-0011](adr/0011-deepseek-official-api-egress.md)协议/技术防护及企业/客户严格数据处理关卡保留。阶段 5–7 未启用。

## 唯一入口

个人所有者已批准 [Web 只写凭据管理与后端加密持久化](adr/0013-personal-write-only-credential-management.md) 的开发范围；添加/删除 Key 不触发模型、不能自动关闭阶段。真实 Key 不进入本仓库，真实外发仍须单独授权。

[ADR-0014](adr/0014-personal-token-admission-and-cost-reservation.md)保留个人Token/保守费用策略与当时的合成验收批准记录；完整请求6000字节不是输入Token证明，8000为调用后阈值。旧真实批次失败及UNKNOWN费用保留，失败终止后不复用剩余授权；新合成验收次数/预算仍待单独确认，出口关闭，阶段尚未退出。

[ADR-0015](adr/0015-approved-deepseek-1017-mapping.md)保留`DeepSeek-V4.1-Flash-1017`映射批准；现有个人启用输入`0.4.0`不等于发送授权，别名及唯一响应模型仍为`deepseek-flash`。旧确认不静默升级，实际发送前重新核对官方依据、相关PR/main CI与新鲜运行绑定。

[ADR-0016](adr/0016-personal-project-agent-use.md)落实2026-10-29已批准的个人Project日常使用设计：普通Finding/PR显式选材，独立有界授权、服务端不可变最小快照和请求/费用追溯；不要求手填合成模板/批次。生产者契约及实现待交付，日常次数/金额/有效期未批准，默认关闭。黑白工作台可独立交付，不以新UI或假HTTP替代真实验收。

| 主题 | 文档 |
|---|---|
| 产品定位和原则 | [产品愿景](product/vision.md) |
| 八仓库职责和范围 | [产品范围](product/scope.md) |
| 阶段、版本和退出条件 | [八阶段路线图](product/roadmap.md) |
| 公共概念 | [术语表](product/glossary.md) |
| 系统边界 | [系统上下文](architecture/context.md) |
| 六平面和运行组件 | [容器架构](architecture/containers.md) |
| 当前功能范围 | [Java Scanner MVP](requirements/scanner-v0.2-feature-spec.md) |
| 已发布平台范围 | [治理平台 MVP](requirements/platform-v0.3-feature-spec.md) |
| 已关闭治理范围 | [持续治理闭环](requirements/governance-v0.4-feature-spec.md) |
| 当前阶段范围 | [Java Agent 增强](requirements/agent-v0.5-feature-spec.md) |
| 工程约定 | [开发规范](development/README.md) |
| 文档治理 | [文档编写规范](development/documentation-standard.md) |
| 后续文档产物与节奏 | [文档交付计划](development/documentation-delivery-plan.md) |
| 跨仓库接口状态 | [契约索引](contracts/README.md) |
| 部署和运行原则 | [运维规范](operations/README.md) |
| 架构决策 | [ADR 索引](adr/README.md) |
| 阶段退出证据 | [报告索引](reports/README.md) |

## 目录职责

| 目录 | 只保存什么 |
|---|---|
| `product/` | 愿景、范围、路线图、公共术语 |
| `requirements/` | 当前或已发布能力的 Feature Spec |
| `architecture/` | 跨仓库系统上下文和容器边界 |
| `adr/` | 长期架构决策和替代关系 |
| `development/` | Git、代码、测试、DoD、阶段和文档规范 |
| `contracts/` | 契约所有者、版本和兼容状态索引 |
| `operations/` | 配置、部署、可观测、安全和恢复原则 |
| `reports/` | 阶段退出、发布、性能、安全和演练证据 |
| [`templates/`](templates/README.md) | Feature Spec、Technical Design、ADR、PR 和复盘模板 |

实现细节与源码一起维护：例如 Scanner S1 Technical Design 位于 `archguard-scanner/docs/technical-design/`。临时计划、任务拆分、评审对话和执行提示放在 Issue/PR，不进入长期文档库。

## 许可证

本地实现设计：[阶段四个人 Agent 可用化与黑白工作台](docs/superpowers/specs/2026-10-28-stage4-agent-workbench-design.md)。所有者已于2026-10-29批准按设计实现；新的真实调用预算与日常费用授权仍待确认。

阅读仓库内检查工具时，可从[工程检查脚本中文阅读](development/code-reading.zh-CN.md)进入；脚本已补中文说明，批准记录和历史报告不变。

本仓库采用 [Apache License 2.0](LICENSE)。
