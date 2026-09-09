# `v0.1.0-foundation` 阶段 0 验收报告

- 状态：Closed
- 验收日期：2026-09-10
- 许可证决策：Apache License 2.0
- 下一阶段：阶段 1 `v0.2.0-scanner`，S2 统一模型与 JSON Schema

## 结论

阶段 0 的产品边界、仓库治理、工程规范、许可证和基础 CI 退出条件已经满足。七仓库正式进入统一 Apache-2.0 许可证线；阶段 0 关闭，Scanner/Samples/Docs 成为阶段 1 功能主线。现有 Platform 继续作为阶段 2 预实现资产冻结功能扩展。

本报告关闭治理阶段，不声称已经创建远端 Git Tag 或 Release。标签只能在对应工作树提交、托管 CI 通过且七仓库版本组合确认后发布。

## 七仓库验收矩阵

| 仓库 | README | LICENSE | CONTRIBUTING | Issue/PR 模板 | 基础 CI | 阶段职责 |
|---|---|---|---|---|---|---|
| `archguard-platform` | 通过 | Apache-2.0 | 通过 | 通过 | 治理 + Java 构建 | 阶段 2 预实现资产，阶段 1 冻结 |
| `archguard-scanner` | 通过 | Apache-2.0 | 通过 | 通过 | 治理 + Java 构建 | 阶段 1 当前主线 |
| `archguard-mcp-gateway` | 通过 | Apache-2.0 | 通过 | 通过 | 治理 | 阶段 5 启用 |
| `archguard-evals` | 通过 | Apache-2.0 | 通过 | 通过 | 治理 | 阶段 6 启用 |
| `archguard-samples` | 通过 | Apache-2.0 | 通过 | 通过 | 治理 | 阶段 1 当前主线 |
| `archguard-deploy` | 通过 | Apache-2.0 | 通过 | 通过 | 治理 | 阶段 2 起启用 |
| `archguard-docs` | 通过 | Apache-2.0 | 通过 | 通过 | 文档治理 | 全阶段事实来源 |

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
| 七仓库必需治理文件 | 通过 |
| 七仓库 Apache-2.0 SHA-256 | 通过；七份一致 |
| 七仓库 CI 包含许可证校验和门禁 | 通过 |
| 七份 GitHub Actions Workflow YAML 解析 | 通过 |
| Platform 完整构建 | 通过；33 tests，0 failures/errors/skipped |
| Scanner S1 完整构建 | 通过；父工程和五模块成功，缓存齐全后的离线复验也通过 |
| Scanner S1 架构测试 | 通过；3 tests，0 failures/errors/skipped |
| Markdown 相对文件链接 | 通过 |
| 差异空白和常见密钥模式 | 通过 |

## 发布、兼容与回滚

正常提交顺序为 Docs 治理证据 → 六个实现/样例仓库许可证和门禁；这些变更不修改 API、数据、制品格式或运行时行为，可独立合入。为保持阶段证据一致，建议同一发布窗口完成。

若法律策略改变，必须由项目所有者作出新决定，同时更新七份 LICENSE、README、贡献说明、CI 校验和和本报告；不得只修改单个仓库。Scanner S1 的构建变更与许可证变更可分别回滚，不影响现有 Platform 数据库和运行时。

## 阶段 1 入口

Scanner S1 已完成：Java 21/Maven Wrapper、父工程、五模块、Enforcer 和模块依赖测试均可运行。下一切片严格进入 S2：先冻结语言无关统一模型、`0.1.0` JSON Schema、稳定 ID/排序和契约失败规则，再开始 Java parser。
