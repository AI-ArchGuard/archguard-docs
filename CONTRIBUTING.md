# Contributing

## 开始之前

1. 阅读 `README.md`、`AGENTS.md` 和 [`development/`](development/README.md) 下的相关规范。
2. 创建或关联 Issue，明确范围、非目标、验收标准、风险和验证方式。
3. 检查工作树，不覆盖或混入无关修改。
4. 普通功能使用 Feature Spec；中高风险设计和架构决策分别补充 Technical Design 与 ADR。

## 文档约定

- 遵循[文档编写与生命周期规范](development/documentation-standard.md)，不创建临时阶段编号文档。
- 使用清晰、可验证的表述，区分当前事实、目标状态、建议和开放问题。
- 新入口必须从 `README.md` 可导航；链接优先使用相对路径。
- 不提交密钥、真实客户源码、个人数据或未经脱敏的生产与事故材料。
- 跨仓库契约变化必须记录版本、兼容顺序、发布顺序和回滚方案。
- 提交消息遵循 Conventional Commits，例如 `docs(adr): record scanner contract strategy`。

## 验证与 Pull Request

- 运行空白、Markdown 链接、YAML 和 Secret 模式检查。
- PR 关联 Issue，并说明修改、影响、验证证据、兼容性、风险和回滚。
- 未运行的检查必须明确标注；默认使用 Squash Merge，不绕过失败的 CI。

## 许可证

除非另有明确书面声明，提交到本仓库的贡献按 [Apache License 2.0](LICENSE) 提供。
