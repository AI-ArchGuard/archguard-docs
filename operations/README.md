# Operations

本目录维护跨仓库部署和运行原则。阶段 2 才首次交付本地 Compose；阶段 7 完成生产化。

## 当前边界

- 当前没有完整多容器部署，不得把 Platform 的数据库测试描述为产品可部署。
- 数据库、Redis 和内部服务端口不得暴露公网。
- Secret 与配置分离；仓库只保存无敏感值示例。
- 日志、指标和链路使用 traceId 关联，不记录凭据或完整源码。
- 数据库迁移只追加；回滚应用不回写已发布迁移。
- 发布必须记录 Platform、Scanner、Schema、Gateway 和数据库的兼容组合。

## 分阶段交付

1. 阶段 2：Docker Compose、本地配置、健康检查和一条命令启动。
2. 阶段 3–6：按真实能力补充 CI、Webhook、模型和 Gateway 可观测性。
3. 阶段 7：HTTPS、Secret 管理、备份恢复、优雅停机、OpenTelemetry、告警和自动发布。
4. Kubernetes 只有在单机或 Compose 出现可测量的容量、隔离或恢复问题并接受 ADR 后引入。

具体运行手册在对应能力实际可运行时加入本目录；不为空计划创建占位文件。
