# Git 约定

## 分支

- `main` 始终保持可构建、可发布；禁止直接推送。
- 短分支格式：`feat/<issue>-<topic>`、`fix/<issue>-<topic>`、`docs/<issue>-<topic>`、`refactor/<issue>-<topic>`。
- 一个分支和 PR 只解决一个明确问题；跨仓库工作拆成独立分支和 PR，并通过同一变更计划关联。
- 默认 Squash Merge；合并前必须通过仓库声明的质量门禁。

## Commit

采用 Conventional Commits：

```text
feat(scanner): add language-neutral component model
fix(platform): reject stale project version
test(scanner): cover three-node dependency cycle
docs(roadmap): adopt scanner-first delivery
build(deploy): add local compose validation
```

提交不得包含密钥、Token、密码、真实客户源码、个人数据、生成缓存或本地环境文件。

## Pull Request

PR 必须关联 Issue，并说明：目标与非目标、修改范围、架构影响、测试结果、兼容性、风险、发布顺序和回滚方式。数据库、跨仓库契约、安全边界或部署变化必须附相应设计或 ADR。

## 版本

- 仓库使用语义化版本，开发期为 `0.x.y`，标签为 `vMAJOR.MINOR.PATCH`；阶段展示名可以使用 `v0.2.0-scanner` 等预发布/路线标识。
- 七仓库独立版本，不要求同一标签。
- Scanner Schema、Rule、Platform REST、MCP Tool 和 Agent 输出各自独立版本；不得用仓库版本代替契约版本。
- Deploy 记录可运行的 Platform/Scanner/Gateway/Schema 组合。
