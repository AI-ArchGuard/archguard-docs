# 阶段 2：Java Platform 骨架

## 阶段目标

只修改 `archguard-platform` 及必要文档，建立可启动、可迁移、可测试的 Java/Spring Boot 模块化单体，并完成健康检查和最小项目创建/查询垂直切片。

## 输入与范围

- Feature Spec：`<related-spec>`
- Technical Design：`<related-design>`
- ADR：模块化单体、PostgreSQL。
- 非目标：Kafka、Redis、微服务、真实 Scanner、GitHub App、LLM 功能。

## 开始前检查

1. 检查仓库状态、README、AGENTS 和现有构建文件。
2. 从官方来源确认受支持的 LTS JDK、Spring Boot、Spring Modulith 和 Testcontainers 兼容版本。
3. 对每个新依赖记录用途、许可证、维护状态和替代方案。
4. 明确模块包名、数据库名、端口和本地环境变量，禁止使用真实凭据。
5. 先写最小 Technical Design 和测试矩阵。

## 执行流程

### 2A：构建与模块骨架

1. 初始化 Maven Wrapper 并固定 Java、插件和依赖版本。
2. 建立 identity、project、repository、architecture、analysis、audit 模块。
3. 每个模块按 `api/application/domain/infrastructure` 组织；不存在内容的层不要创建占位类。
4. 使用 Spring Modulith 或等价架构测试声明允许依赖。
5. 领域层不得依赖 Spring Web、数据库驱动或外部模型 SDK。

### 2B：运行基础设施

1. 配置 PostgreSQL 和本地测试环境，不引入 Redis。
2. 使用 Flyway 创建首个不可变迁移；验证空库启动。
3. 配置 Actuator 健康、就绪和存活检查。
4. 定义统一错误响应 `code/message/traceId/details`。
5. 建立结构化日志和 traceId 传播，禁止记录凭据和源码。

### 2C：最小垂直切片

1. 先定义项目创建/查询 DTO、用例和测试。
2. 在领域模型中实现不变量，不使用贫血实体承载所有逻辑。
3. 事务边界放在应用层，控制器只做协议转换。
4. 数据库实体不得直接作为 API 响应。
5. 实现创建和查询 API、幂等或冲突语义、权限占位边界及审计事件。

## 交付物

- Maven 工程、Wrapper 和固定版本配置。
- 模块结构与架构规则测试。
- Flyway 迁移、健康检查、错误协议和日志配置。
- 项目创建/查询代码、OpenAPI 和测试。
- README 本地启动和验证说明。

## 验证

1. 格式化、静态检查和完整 Maven 验证。
2. 单元测试：项目领域不变量和错误路径。
3. 架构测试：模块及领域层依赖限制。
4. Testcontainers 集成测试：空库迁移、创建、重复创建、查询和不存在场景。
5. 启动应用并验证健康、就绪和 API 请求。
6. 扫描依赖和 Secret；检查日志不包含敏感数据。

## 停止条件

版本兼容性无法确认、数据库迁移策略未决定、模块边界与现有 ADR 冲突或需要引入非目标基础设施时停止。

## 退出条件

干净环境中可用 Wrapper 完成构建；空库可启动；架构规则、集成测试和健康检查通过；失败项有真实证据。
