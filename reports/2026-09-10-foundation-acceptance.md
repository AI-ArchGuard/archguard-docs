# `v0.1.0-foundation` 阶段 0 验收报告

- 状态：Closed
- 验收日期：2026-09-10
- 许可证决策：Apache License 2.0
- 下一阶段：阶段 1 `v0.2.0-scanner`；先验收 S1 构建与模块边界

> 本报告是阶段 0 关闭时的历史快照，不随后续切片状态改写。当前执行状态以[产品路线图](../product/roadmap.md)为准。

## 结论

阶段 0 的产品边界、仓库治理、工程规范、许可证和基础 CI 退出条件已经满足。七个 Foundation PR 均已 Squash Merge，合并后的七条 `main` CI 全部成功；阶段 0 正式关闭，Scanner/Samples/Docs 进入阶段 1。现有 Platform 继续作为阶段 2 预实现资产冻结功能扩展。

本报告关闭治理阶段，不声称已经创建远端 Git Tag 或 Release。标签和 Release 只在对应仓库明确执行发布流程时创建，不影响本阶段基于 `main` 提交与 CI 证据的关闭结论。

## 七仓库验收矩阵

| 仓库 | README | LICENSE | CONTRIBUTING | Issue/PR 模板 | 基础 CI | 阶段职责 |
|---|---|---|---|---|---|---|
| `archguard-platform` | 通过 | Apache-2.0，`main` | 通过 | 通过 | 合并后 CI 成功 | 阶段 2 预实现资产，阶段 1 冻结 |
| `archguard-scanner` | 通过 | Apache-2.0，`main` | 通过 | 通过 | 合并后 CI 成功 | 阶段 1 当前主线 |
| `archguard-mcp-gateway` | 通过 | Apache-2.0，`main` | 通过 | 通过 | 合并后 CI 成功 | 阶段 5 启用 |
| `archguard-evals` | 通过 | Apache-2.0，`main` | 通过 | 通过 | 合并后 CI 成功 | 阶段 6 启用 |
| `archguard-samples` | 通过 | Apache-2.0，`main` | 通过 | 通过 | 合并后 CI 成功 | 阶段 1 当前主线 |
| `archguard-deploy` | 通过 | Apache-2.0，`main` | 通过 | 通过 | 合并后 CI 成功 | 阶段 2 起启用 |
| `archguard-docs` | 通过 | Apache-2.0，`main` | 通过 | 通过 | 合并后 CI 成功 | 全阶段事实来源 |

## 许可证门禁

- 七份 `LICENSE` 使用相同 Apache License 2.0 标准文本。
- 标准文件 SHA-256：`c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`。
- 每个仓库 CI 同时验证 `LICENSE` 存在和上述校验和；许可证文本被意外替换或截断时失败关闭。
- 每个 README 指向本地 `LICENSE`，每个贡献指南声明默认贡献许可。
- 当前没有需要汇总到 `NOTICE` 的项目自有归属声明；引入带 NOTICE 要求的可再分发制品时必须重新评审。

## 工程和架构关卡

- 产品愿景、范围、八阶段路线和六平面架构有唯一入口。
- 七仓库职责无运行时重叠，跨仓库契约遵循生产者所有、Docs 汇总、Deploy 记录组合。
- Git、Commit、测试、DoD、安全、数据库、日志/trace、版本和兼容策略已有规范。
- Platform 保持模块化单体；Scanner 契约独立；Gateway 不拥有业务数据；Evals 不进入线上强依赖。
- 基础 CI 验证治理文件、许可证和空白错误；有运行时工程的仓库额外执行自身构建。

## 验证证据

| 检查 | 结果 |
|---|---|
| 七仓库必需治理文件 | 通过；已合入 `main` |
| 七仓库 Apache-2.0 SHA-256 | 通过；七份一致并由 CI 校验 |
| 七仓库 CI 包含许可证校验和门禁 | 通过；已合入 `main` |
| 七份 Foundation PR 与合并后 `main` CI | 通过 |
| Platform 完整构建 | 通过；33 tests，0 failures/errors/skipped |
| Scanner S1 完整构建 | 本地通过；父工程和五模块成功，作为阶段 1 首个待验收切片 |
| Scanner S1 架构测试 | 通过；3 tests，0 failures/errors/skipped |
| Markdown 相对文件链接 | 通过 |
| 差异空白和常见密钥模式 | 通过 |

### 远端关闭证据

| 仓库 | Foundation PR | `main` 合并提交 | 合并后 CI |
|---|---|---|---|
| Docs | [#13](https://github.com/AI-ArchGuard/archguard-docs/pull/13) | `b8a0b190` | [success](https://github.com/AI-ArchGuard/archguard-docs/actions/runs/34471351044) |
| Scanner | [#5](https://github.com/AI-ArchGuard/archguard-scanner/pull/5) | `c36083fd` | [success](https://github.com/AI-ArchGuard/archguard-scanner/actions/runs/34471651858) |
| Platform | [#10](https://github.com/AI-ArchGuard/archguard-platform/pull/10) | `7eb2e78f` | [success](https://github.com/AI-ArchGuard/archguard-platform/actions/runs/34471767348) |
| Samples | [#2](https://github.com/AI-ArchGuard/archguard-samples/pull/2) | `23b86809` | [success](https://github.com/AI-ArchGuard/archguard-samples/actions/runs/34471989247) |
| Deploy | [#2](https://github.com/AI-ArchGuard/archguard-deploy/pull/2) | `cfb50c07` | [success](https://github.com/AI-ArchGuard/archguard-deploy/actions/runs/34472088146) |
| Gateway | [#3](https://github.com/AI-ArchGuard/archguard-mcp-gateway/pull/3) | `27a5fa11` | [success](https://github.com/AI-ArchGuard/archguard-mcp-gateway/actions/runs/34472214986) |
| Evals | [#3](https://github.com/AI-ArchGuard/archguard-evals/pull/3) | `265f840f` | [success](https://github.com/AI-ArchGuard/archguard-evals/actions/runs/34472315485) |

## 发布、兼容与回滚

实际合并顺序为 Docs → Scanner → Platform → Samples → Deploy → Gateway → Evals。Foundation 变更没有修改 API、数据、制品格式或运行时行为；回滚时可在对应仓库单独 revert Foundation 合并提交，不要求跨仓库同步回滚。

若法律策略改变，必须由项目所有者作出新决定，同时更新七份 LICENSE、README、贡献说明、CI 校验和和本报告；不得只修改单个仓库。Scanner S1 的构建变更与许可证变更可分别回滚，不影响现有 Platform 数据库和运行时。

## 阶段 1 入口

Scanner S1 的本地实现已验证：Java 21/Maven Wrapper、父工程、五模块、Enforcer 和模块依赖测试均可运行。阶段 1 的下一步是单独提交并由托管 CI 验收 S1；通过后再进入 S2，并冻结语言无关统一模型、`0.1.0` JSON Schema、稳定 ID/排序和契约失败规则。
