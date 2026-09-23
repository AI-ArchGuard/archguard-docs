# ArchGuard Documentation

ArchGuard 的跨仓库产品、架构、工程规范、契约索引和阶段证据事实来源。

## 当前状态

- 最终定位：Java-first、语言无关架构、AI 增强的软件架构治理平台。
- 阶段 0 `v0.1.0-foundation` 已关闭：七仓库 Foundation PR 已合并，合并后的 `main` CI 全部成功。
- 阶段 1 `v0.2.0-scanner` 已通过[阶段验收](reports/2026-09-19-scanner-v0.2.0-acceptance.md)并关闭；Scanner `v0.2.0` Release、Result Schema `0.1.0` 和固定 Samples 已发布。
- 阶段 2 `v0.3.0-platform` 已通过[阶段验收](reports/2026-09-22-platform-v0.3.0-acceptance.md)并关闭；Scanner `v0.2.1`、Platform `v0.3.0`、Web `v0.1.0` 和 Deploy `v0.3.0` 已发布。
- 阶段 3 `v0.4.0-governance` 的 3A 范围评审已完成；3B 冻结 Git 修订、报告提交、门禁结果和 Finding 指纹契约。后续切片仍按合并后 `main` CI 逐个放行。

## 唯一入口

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
| 当前阶段范围 | [持续治理闭环](requirements/governance-v0.4-feature-spec.md) |
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

本仓库采用 [Apache License 2.0](LICENSE)。
