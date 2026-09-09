# Architecture

系统上下文、容器图、仓库边界、跨仓库契约和总体架构说明。

## 当前切片

| ID | 文档 | 只解决的问题 | 状态 |
|---|---|---|---|
| D07 | [系统上下文与信任边界](system-context.md) | 谁与 ArchGuard 交互，系统边界和外部信任边界在哪里 | Accepted |
| D08 | [容器与进程架构](container-architecture.md) | Platform、Scanner、Gateway、数据库和运行进程如何分工 | Accepted |
| D09 | [七仓库职责与依赖](repository-boundaries.md) | 七仓库的事实来源、允许依赖、禁止依赖和契约所有权 | Accepted |
| D10 | [Scanner 与 Analyzer 架构](analyzer-architecture.md) | Scanner runtime、Analyzer Registry、Analyzer 和进程边界如何协作 | Accepted |

D07–D10 已于 2026-09-09 通过 [G2 架构边界评审](../reports/g2-architecture-boundary-review.md)。下一步可以进入 G3 契约与安全；G2 不冻结字段级公共 Schema，也不表示任何运行时能力已经交付。
