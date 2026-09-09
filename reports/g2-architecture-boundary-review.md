# G2 架构边界评审记录

- 状态：Accepted
- 适用范围：D07–D10 架构边界关卡
- 所有者：ArchGuard 项目所有者
- 依赖决策：G1 产品边界、D07 系统上下文、D08 容器架构、D09 仓库边界、D10 Analyzer 架构
- 最后评审：2026-09-09
- 取代/被取代：无

## 本文解决的问题

本文记录 G2 是否接受 Platform、Scanner、Analyzer Registry、Analyzer、七仓库和运行进程之间的边界。它是进入 G3 契约与安全设计的关卡证据，不替代 D07–D10 的规范内容，也不冻结字段级公共 Schema。

## 当前事实

- G1 已接受长期产品定位、V1 Java/Spring 范围、支持状态和 V1–V5 优先级。
- 当前仍只有治理和文档能力，没有可运行 Platform、Scanner、Gateway、Analyzer、公共契约或业务数据库。
- D07–D10 已分别给出系统信任边界、容器与进程、七仓职责和 Scanner/Analyzer 结构。
- 项目所有者于 2026-09-09 确认按本组架构建议逐步完成 G2。
- G3 契约与安全、G4 V1 可开发性仍未通过。

## 评审输入

| 切片 | 规范文档 | 评审问题 | 评审结果 |
|---|---|---|---|
| D07 | [系统上下文与信任边界](../architecture/system-context.md) | 外部参与者、系统边界、数据类别和一级信任边界是否清楚？ | Accepted |
| D08 | [容器与进程架构](../architecture/container-architecture.md) | Platform、Scanner、Gateway、PostgreSQL 和进程关系是否清楚？ | Accepted |
| D09 | [七仓库职责与依赖](../architecture/repository-boundaries.md) | 七仓库事实来源、允许/禁止依赖和契约所有权是否唯一？ | Accepted |
| D10 | [Scanner 与 Analyzer 架构](../architecture/analyzer-architecture.md) | Scanner runtime、Registry、Analyzer 选择和 V1 进程边界是否清楚？ | Accepted |

## 一致性检查

| 检查项 | 结论 |
|---|---|
| 与 G1 V1 范围一致 | 只把 Java 源码、Spring 语义和 Maven 静态元数据作为 V1 必选；字节码和 Gradle 仍为增强项 |
| 当前与目标状态分离 | 所有架构选择均不构成“已支持”声明，运行时代码仍未实现 |
| Platform 模块化单体 | D08 保持单一制品与数据库，不因容器图拆分领域微服务 |
| Scanner 独立契约 | D08–D10 均禁止 Scanner 依赖 Platform 内部类、业务表或长期凭据 |
| Registry 与 Analyzer 一致 | D08、D09、D10 均把 Registry 放在 Scanner，并采用随制品发布的 V1 Analyzer |
| 数据访问最小化 | 只有 Platform 访问 PostgreSQL；Scanner 临时处理输入；Gateway 不直连业务数据库 |
| 后续版本隔离 | Gateway、PR 和 AI 仍分别属于 V2–V4，不进入 V1 最小拓扑 |
| G3 边界未被提前冻结 | 字段、状态、错误码、Rule 归属、资源阈值和安全实现均有明确后续去向 |

## 评审结论

G2 通过。D07–D10 状态统一为 Accepted，允许进入 G3 契约与安全设计。

G2 冻结逻辑所有权和进程边界，不冻结 ScanRequest/ScanResult 字段、Fact/Finding/Evidence/Diagnostic 结构、Rule Executor 归属、传输协议、隔离实现或资源数值。

## 已接受决策

### 1. 系统与信任边界

- ArchGuard 内部包含业务治理控制面和受控分析执行面；代码托管、身份、模型和外部可观测供应商位于系统边界之外。
- Repository 内容和外部载荷均为不可信输入；V1 不执行目标构建、脚本、插件、任务或任意命令。
- Platform 是业务身份、资源归属、Policy、Scan 和持久化结果的最终授权入口。

### 2. Platform 与 Scanner

- Platform 初期保持 Java/Spring 模块化单体，并通过应用边界访问唯一业务事实来源 PostgreSQL。
- Platform 与 Scanner 是独立进程和部署单元，只通过版本化 Scanner 契约交互。
- Platform 先持久化 Scan，再由后台执行器异步调用 Scanner；传输和可靠性产品留给后续设计。
- Scanner 不访问 Platform 数据库，不管理用户、Project、Policy 生命周期或业务审计事实。

### 3. Registry 与 Analyzer

- Analyzer Registry 属于 `archguard-scanner` 运行时，不是独立服务、Platform 模块或远程插件市场。
- V1 Analyzer 是随受控 Scanner 制品发布、通过显式 allowlist 注册的受信任模块，并与 Scanner runtime 同进程运行。
- Platform 只请求稳定 Capability，不指定实现类；Repository 不得提供可执行 Analyzer 或插件路径。
- 新语言、原生工具或不同信任级别出现时，可以用新 ADR 评估受控子进程，不改变 Platform/Scanner 公共边界。

### 4. 七仓库与契约所有权

- Docs 拥有跨仓库规范语义；Platform 拥有 REST 和业务状态；Scanner 拥有扫描与 Analyzer 契约制品。
- Gateway 默认通过 Platform 查询业务数据；Samples 和 Evals 只作为测试/评估依赖；Deploy 保存已验证制品组合。
- 七仓库独立版本和发布，不建立共享内部“万能模型”或要求同步版本。
- 跨仓库变化按规范/样例 → 提供方 → 消费方 → Deploy 的顺序兼容发布，回滚从消费方开始。

## 对 G1 的约束检查

- 没有扩大 V1 技术栈或产品工作流范围。
- 没有把 JVM 字节码、Gradle、PR、MCP、AI 或多技术栈能力升级为 V1 必选或当前支持。
- 没有让 LLM 产生确定性 Fact/Finding，也没有把动态插件系统作为扩展前提。
- 没有选择具体解析库、消息中间件、云厂商、模型、Kubernetes 或性能指标。

## 开放问题及去向

| 开放问题 | 后续所有者或关卡 |
|---|---|
| ScanRequest/ScanResult 字段、版本协商、状态和部分成功语义 | G3：D11 扫描契约 |
| Fact、Finding、Evidence、Diagnostic、Rule 和去重语义 | G3：D12 结果与规则模型 |
| 输入物化、路径/网络/进程限制、凭据、清理和保留 | G3：D13 不可信 Repository 安全 |
| Java/Spring/Maven 精确版本、能力深度和验收标准 | G4：D14 Feature Spec |
| 需求—架构—里程碑追踪和阶段入口同步 | G4：D15–D16 |
| Platform 内部模块名、应用接口和首个持久化模型 | M2 Technical Design |
| Scanner 传输适配器、Analyzer 代码粒度和具体技术选型 | M4/M5 Technical Design 与对应 ADR |
| Broker、子进程 Analyzer 或 Platform 拆分的触发证据 | M7 或后续独立 ADR |

这些问题均有明确后续边界，不改变 G2 对逻辑所有权和进程关系的结论。

## 非目标

- 不在本记录复制 D07–D10 的全部图表和访问矩阵。
- 不创建业务代码、Schema、SDK、数据库迁移、部署文件或动态插件系统。
- 不宣称 G3/G4、M1 或任何产品版本已经完成。
- 不用 G2 结论替代 Feature Spec、Technical Design、ADR 或自动化契约测试。

## 验收证据

- D07–D10 均包含状态、范围、当前事实、边界决策、非目标、开放问题和验收证据。
- 四份文档分别覆盖系统、容器/进程、仓库/契约和 Scanner/Analyzer，没有重复建立事实来源。
- 七仓库 README 已逐一核对，职责与依赖方向不存在冲突。
- Mermaid 图、Markdown 相对链接、文档导航、空白、YAML 和高置信 Secret 模式均纳入本地检查。
- G2 决策逐项保持 G1 范围，并把字段级契约、Rule 职责和安全实现留给 G3。

## 变更与取代规则

- D07–D10 的 Accepted 结论可以补充事实和链接，但不得原地反转 Platform/Scanner、Registry/Analyzer 或仓库所有权。
- 若未来需要 Scanner 访问业务库、Registry 独立服务、Repository 动态插件、Analyzer 独立服务或 Platform 微服务化，必须新增 ADR 和 G2 级复审说明取代关系。
- G3 可以选择契约字段、Rule 归属和安全机制，但不得通过实现细节绕过本记录的信任、数据访问和进程边界。
