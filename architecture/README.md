# Architecture

系统上下文、容器图、仓库边界、跨仓库契约和总体架构说明。

## 当前切片

| ID | 文档 | 只解决的问题 | 状态 |
|---|---|---|---|
| D07 | [系统上下文与信任边界](system-context.md) | 谁与 ArchGuard 交互，系统边界和外部信任边界在哪里 | Accepted |
| D08 | [容器与进程架构](container-architecture.md) | Platform、Scanner、Gateway、数据库和运行进程如何分工 | Accepted |
| D09 | [七仓库职责与依赖](repository-boundaries.md) | 七仓库的事实来源、允许依赖、禁止依赖和契约所有权 | Accepted |
| D10 | [Scanner 与 Analyzer 架构](analyzer-architecture.md) | Scanner runtime、Analyzer Registry、Analyzer 和进程边界如何协作 | Accepted |
| D11 | [Scanner 版本化契约](scan-contract.md) | 请求、结果、状态、版本协商、幂等和部分成功如何跨进程表达 | Accepted |
| D12 | [结果与 Rule 模型](result-rule-model.md) | Fact、Finding、Evidence、Diagnostic、Policy 和 Rule 的字段与职责 | Accepted |
| D13 | [不可信 Repository 安全](untrusted-repository-security.md) | 输入获取、文件、进程、网络、凭据、清理和保留采用什么默认值 | Accepted |

D07–D10 已于 2026-09-09 通过 [G2 架构边界评审](../reports/g2-architecture-boundary-review.md)，D11–D13 又于同日通过 [G3 契约与安全评审](../reports/g3-contract-security-review.md)，D14–D16 已通过 [G4 V1 可开发性评审](../reports/g4-v1-readiness-review.md)。G4 允许开始 M2 设计，不表示任何机器 Schema 或运行时能力已经交付。
