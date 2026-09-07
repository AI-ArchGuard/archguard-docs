# 标准开发流程

## 1. 需求进入

创建Issue并写清：问题、目标用户、价值、范围、非目标、验收标准、指标和风险。需求不清楚不得编码。

## 2. 设计

- 小改动：在Issue写实现说明。
- 中型改动：Technical Design。
- 影响边界、协议、数据或部署：补充ADR。
- 画必要的C4、时序或数据流图。

设计评审检查：是否可测试、是否向后兼容、失败如何处理、如何观测、如何回滚、是否存在更简单方案。

## 3. 计划

拆分为每个0.5至2天可完成的任务，每项有独立验收结果。先做端到端最小切片，再扩展异常路径和非功能能力。

## 4. 开发

推荐短分支：

```text
feat/123-create-project
fix/245-webhook-replay
docs/031-update-adr
refactor/087-isolate-analysis-module
```

实现顺序：契约/测试 → 领域逻辑 → 适配器 → API → 可观测 → 文档。

## 5. 本地验证

- 格式化和静态检查；
- 单元测试；
- 相关集成测试；
- 数据库迁移测试；
- Docker启动与健康检查；
- 涉及并发时执行竞争、压力或故障测试。

## 6. Pull Request

PR应小于约500行有效业务变更；更大时说明不可拆原因。PR必须关联Issue，填写风险、测试、截图/API样例、迁移和回滚。

## 7. 合并

默认Squash Merge；提交标题遵循Conventional Commits。禁止直接推送主分支，禁止在CI失败时合并。

## 8. 发布与复盘

生成变更日志、打标签、部署测试环境、执行Smoke Test。严重故障在48小时内完成无责复盘，形成具体改进Issue。

## 提交约定

```text
feat(platform): add project registration
fix(scanner): detect nested cycle correctly
test(gateway): cover authorization denial
docs(adr): record event delivery strategy
refactor(platform): isolate audit port
build(deploy): add image scanning
```
