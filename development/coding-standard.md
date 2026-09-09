# 代码约定

本文件规定七仓库共同遵守且不能被阶段实现削弱的代码边界。仓库专属规则写入对应 `AGENTS.md`，不在中央文档复制。

## Java

- 使用构造器注入；禁止字段注入和全局可变状态。
- 领域层不依赖 Spring Web、数据库驱动、Scanner 实现或模型 SDK。
- 公共边界使用明确 DTO；数据库行/实体不作为 API 响应。
- 事务边界在应用层；模块不直接访问其他模块内部类或表。
- Scanner 的 `scanner-domain` 保持语言无关，语言前端只负责映射到统一模型。
- 外部输入失败必须显式返回 Diagnostic 或错误，禁止吞异常。

## Go

- `gofmt`、`go vet` 和适用的 race test 进入 CI。
- 所有外部调用接受 `context.Context`，支持超时与取消。
- 错误显式处理并用 `%w` 保留 cause；Goroutine 有所有者、停止和回收路径。
- Gateway 只处理通信与访问控制，不复制 Platform 业务逻辑。

## Python

- Evals 数据集、评分器、Prompt 和基线全部版本化。
- 运行器对模型/Agent 框架可替换；确定性评分优先。
- 不收集真实客户源码、个人数据、凭据或未经脱敏的生产记录。
- 测试失败不能通过删除样例、放宽阈值或隐藏波动解决。

## API、数据与日志

- API 错误统一为 `code/message/traceId/details`；列表分页；创建类操作有明确幂等策略。
- Scanner、REST、Tool 和 Agent 输出使用严格版本化 Schema；未知内容按契约失败关闭。
- 数据库变化只追加 Flyway 迁移；已发布迁移不得修改。
- 结构化日志包含 traceId 和必要资源标识，不记录凭据、完整源码或隐藏推理。
