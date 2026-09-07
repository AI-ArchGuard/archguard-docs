# 阶段 3：仓库登记与扫描任务

## 阶段目标

在 `archguard-platform` 内实现仓库登记和扫描任务状态机，通过 Port 与 Fake Scanner 完成项目到扫描结果的最小业务闭环。

## 输入与范围

- 必需：Feature Spec、测试计划。
- 视风险需要：Technical Design；状态和契约决策需要 ADR。
- 允许修改：Platform 及对应 OpenAPI、需求和架构文档。
- 非目标：真实 Git 克隆、真实 Scanner、消息中间件、GitHub Webhook 和 AI 解释。

## 开始前检查

1. 验证阶段 2 的构建、迁移和模块规则确实通过。
2. 阅读 project、repository、analysis、audit 模块现状。
3. 明确身份、组织、项目和仓库的资源归属规则。
4. 定义 RepositoryRegistration、ScanJob、ScanResult 的术语和生命周期。
5. 先画状态机和请求时序，再写实现。

## 执行流程

### 3A：契约与不变量

1. 定义登记仓库、创建扫描和查询结果的 API DTO。
2. 明确仓库唯一性、规范化 URL、启用/禁用和删除语义。
3. 定义 ScanJob 状态，例如 QUEUED、RUNNING、SUCCEEDED、FAILED、CANCELLED。
4. 列出每个合法转换、禁止转换和终态行为。
5. 定义幂等键作用域、重复请求响应和并发冲突策略。
6. 定义统一错误码及审计事件。

### 3B：测试优先实现

1. 先覆盖重复仓库、非法 URL、越权访问、非法状态转换和幂等重放。
2. 实现领域模型及状态不变量。
3. 实现应用服务和事务边界，禁止跨模块直接访问表。
4. 定义 Scanner Port 和版本化内部 DTO。
5. 使用 Fake Adapter 返回固定违规，不连接真实 Git。
6. 实现 API、持久化适配器、错误映射和审计记录。

### 3C：可观测与文档

1. 日志包含 traceId、actorId、projectId、repositoryId 和 scanJobId。
2. 增加任务创建、状态、失败原因和耗时指标。
3. 更新 OpenAPI、状态机图、数据库模型和运行说明。
4. 记录未来真实 Scanner 适配器需要满足的契约。

## 交付物

- Feature Spec、状态机和必要设计文档。
- RepositoryRegistration、ScanJob 和相关迁移。
- Scanner Port、Fake Adapter、API 与审计事件。
- 单元、集成和最小端到端测试。

## 验证

1. 领域状态转换的表驱动或参数化测试。
2. 重复仓库、重复扫描、并发创建和权限错误测试。
3. 空库和上一阶段数据库升级测试。
4. 创建项目 → 登记仓库 → 发起扫描 → 查询固定结果的集成测试。
5. OpenAPI 响应、错误结构、分页和幂等语义检查。
6. 完整 Maven、架构规则和 Secret 扫描。

## 停止条件

状态语义、资源归属、幂等范围或 Scanner 契约存在歧义时停止；不得用控制器条件分支临时绕过领域设计。

## 退出条件

最小扫描业务链路可重复运行，非法路径被测试覆盖，数据库和 API 文档同步，并且真实 Scanner 可通过 Port 替换 Fake。
