# ArchGuard Documentation

ArchGuard 的产品、需求、架构、ADR、工程规范、运行手册和交付报告的事实来源。

## 当前状态

M0 仓库治理基线、G1 产品边界和 G2 架构边界已经完成；下一步进入 G3 契约与安全。当前仍没有已支持的业务或分析能力，公共 Schema 和运行时实现尚未冻结。

## 职责

- 维护产品范围、需求和术语。
- 记录跨仓库架构、契约和架构决策。
- 发布工程规范、质量门禁、发布流程和运行手册。
- 保存可验证的安全、性能和交付报告。

## 非职责

- 不承载 Platform、Scanner、MCP Gateway 等服务的实现代码。
- 不保存密钥、真实客户源码、生产数据或未经脱敏的事故材料。
- 不替代各代码仓库内与实现紧密相关的使用说明和测试文档。

## 依赖与契约

- 本仓库不依赖其他 ArchGuard 仓库的内部实现。
- 其他仓库通过稳定链接引用这里的跨仓库规范、契约说明和 ADR；实现细节仍由对应代码仓库维护。
- 跨仓库契约变化必须在这里记录版本、兼容顺序、发布顺序和回滚方案。

## 入口

- [项目治理](engineering/governance.md)
- [开发流程](engineering/development-workflow.md)
- [工程规范](engineering/engineering-standards.md)
- [质量门禁](engineering/quality-gates.md)
- [安全与可观测性](engineering/security-and-observability.md)
- [发布与运行](engineering/release-and-operations.md)
- [分阶段开发提示词](engineering/prompts.md)
- [文档模板](templates/)
- [M0 仓库基线验收报告](reports/m0-repository-baseline.md)

## 目录

| 目录 | 内容 |
|---|---|
| `product/` | 产品章程、范围与路线图 |
| `requirements/` | Feature Spec 与验收标准 |
| `architecture/` | C4、跨仓库边界与契约 |
| `adr/` | 架构决策记录 |
| `engineering/` | 统一工程规范 |
| `runbooks/` | 部署、运维与故障处置手册 |
| `reports/` | 评估、性能、安全和发布证据 |
| `templates/` | 需求、设计、ADR、PR 和复盘模板 |

## 本地验证

当前基线可执行空白、Markdown 相对链接、YAML 结构和常见 Secret 模式检查。仓库尚无提交，因此 GitHub Actions 只完成了配置审查，不能声称远程 CI 已运行。
