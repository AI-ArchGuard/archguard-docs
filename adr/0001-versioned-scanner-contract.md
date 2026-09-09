# ADR-0001：Scanner 使用独立严格的版本化契约

- 状态：Accepted
- 日期：2026-09-09
- 决策者：ArchGuard 项目所有者
- 替代：无

## 背景

Platform 与 Scanner 是独立进程和仓库。若共享 Platform DTO、Java 内部类或无版本 JSON，双方将无法独立发布，也无法可靠表达部分成功、兼容窗口和安全校验。

## 决策驱动因素

- Scanner 不得依赖 Platform 内部实现或业务数据库。
- 契约必须可机器校验、跨语言消费并支持提供方/消费方测试。
- 当前处于 `0.x` 开发期，需要明确而保守的破坏性变化规则。
- 不可信输出必须在 Scanner 和 Platform 两侧校验。

## 选择

- ScanRequest、ScanResult 和 ContractError 使用独立 JSON Schema Draft 2020-12 发布，首个版本为 `0.1.0`。
- `archguard-scanner` 拥有 Schema/示例制品，`archguard-docs` 拥有规范语义，Platform 只消费公开契约。
- `0.MINOR` 是兼容线；字段、枚举或语义变化使用新 MINOR 并与旧线并行迁移，PATCH 不改变结构。
- 对象默认拒绝未知字段；无共同兼容线、未知枚举或无效引用均失败关闭。
- transport adapter 可以替换，但不得改变已发布契约的身份、幂等、状态和部分成功语义。

## 备选方案

- 共享 Java DTO：类型安全但绑定语言、构建和内部发布节奏，拒绝。
- 复用 Platform REST/数据库模型：泄漏业务所有权和持久化细节，拒绝。
- 宽松无版本 JSON：前期简单，但无法证明兼容和拒绝恶意字段，拒绝。
- Protobuf/gRPC：机器契约强，但会提前绑定 transport/toolchain；当前不选择。

## 正面影响

- Platform、Scanner 和 Evals 可以独立生成契约测试。
- 版本不兼容、未知内容和输出污染有明确失败边界。
- 未来可以在不改变语义的前提下替换 HTTP、命令或消息适配器。

## 负面影响与风险

- 严格兼容线会增加并行 Schema、示例和消费方测试维护成本。
- JSON Schema 不能独自表达全部跨引用不变量，需要实现级校验器。
- PATCH 不允许结构扩展，早期迭代需要更频繁提升 MINOR。

## 验证方式

- 提供方/消费方分别运行有效、无效、未知字段、未知枚举和跨引用测试。
- 同一规范请求重复执行，移除时间/耗时观测字段后比较 RFC 8785 确定性投影。
- 在 Deploy 中验证 Platform 与 Scanner 至少共享一个兼容线。

## 何时重新评估

- JSON 消息成为可测量的性能瓶颈，或多语言 SDK 需要更强代码生成时。
- 出现多个独立 Scanner 提供方，需要独立 Schema Registry 或标准化协议时。
- 新 transport 无法保持已发布契约语义时，必须以新 ADR 取代而非绕过。
