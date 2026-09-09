# Feature Spec：V1 Java/Spring 可信治理闭环

- 切片：D14
- Issue：[archguard-docs#8](https://github.com/AI-ArchGuard/archguard-docs/issues/8)
- Owner：ArchGuard 项目所有者
- 状态：Ready
- 目标产品：V1
- 目标契约：Scanner `0.1.0`
- 依赖：G1 产品边界、G2 架构边界、G3 契约与安全
- 最后评审：2026-09-09（G4 V1 可开发性评审通过）

## 问题与用户价值

Java/Spring 团队的包、层次、组件和依赖约束常散落在文档与人工评审中。V1 要让获准用户登记一个 Repository，上传指定版本的不可变源码归档，选择确定性 Policy 发起手动 Scan，并用可重复的 Finding、最小 Evidence 和独立 Diagnostic 处置架构漂移。

当前仍没有可运行 Platform、Scanner、Analyzer、公共机器 Schema 或端到端流程。本文定义目标行为和验收边界，不把目标写成当前支持。

## 目标

- 建立 Project、Repository、Policy、手动 Scan、结果查询和审计的最小闭环。
- 对明确版本范围内的 Java 源码、Spring 语义和 Maven 静态元数据产生确定性结果。
- 用首批四条 Rule 覆盖禁止依赖、包循环、字段注入和 Maven 禁止依赖。
- 对失败、部分成功、取消、超限和不支持输入给出符合 G3 的终态与 Diagnostic。
- 让每个 V1 需求都能追踪到架构、ADR、仓库、里程碑、合成样例和自动化证据。

## 非目标

- 不支持 Java 25 源码、Spring Boot 4、Spring Framework 7、Maven 4 特有模型或其他技术栈。
- 不分析 JVM 字节码、Gradle、Kotlin、Scala、Go、TypeScript、容器或部署配置。
- 不执行 Maven/Gradle、插件、Annotation Processor、脚本、测试或目标 Repository 中的命令。
- 不下载依赖、不构建完整 classpath、不解析外部 JAR，也不承诺方法级调用图。
- 不提供远程 Git 获取、GitHub PR、MCP、AI、自动修复、自动提交或自动合并。
- 不在 G4 选择 Platform/Scanner 实现库、传输协议、数据库表、UI 框架或部署厂商。

## V1 兼容快照

以下范围是 ArchGuard 静态分析兼容目标，不等同于上游厂商的商业支持承诺，也不随上游页面自动变化。变化必须更新本文、样例和验收矩阵。

| 输入 | V1 必选范围 | 判定方式 | 超出范围的行为 |
|---|---|---|---|
| Java 源码 | 语言级别 17、21；UTF-8；`.java` | Repository 登记值与解析结果共同校验 | 受影响能力 `FAILED/PARTIAL`，返回 `java.language_level_unsupported` 或解析 Diagnostic |
| Spring Boot | 3.4.x、3.5.x | 只从归档内 POM 的 parent/BOM/依赖声明识别 | Java/Maven 能力可继续；Spring 能力返回 `spring.version_unsupported` |
| Spring Framework | 6.2.x | 只从归档内 POM 声明识别 | 同上，不访问远程仓库推断版本 |
| Maven Project Model | `modelVersion` 4.0.0 | 解析归档内 `pom.xml` | 该 Maven 模块失败并返回 `maven.model_version_unsupported` |
| 源码布局 | Maven 标准 `src/main/java`，支持归档内多模块 | 根 POM 与 `<modules>` 的规范相对路径 | 测试、生成源码和未声明目录不进入 V1 结果 |

选择依据快照日期为 2026-09-09：[Oracle Java SE 路线图](https://www.oracle.com/java/technologies/java-se-support-roadmap.html)将 17、21、25 列为 LTS；V1 为控制首版语法风险只接受 17/21。Spring Boot [3.4](https://docs.spring.io/spring-boot/3.4/system-requirements.html)和[3.5](https://docs.spring.io/spring-boot/3.5/system-requirements.html)均以 Java 17 与 Spring Framework 6.2 为基线。Maven [POM Reference](https://maven.apache.org/pom.html)记录 4.0.0 为当前 POM 模型版本。

## 输入与用户流程

V1 生产路径只启用 D11 `content-archive`。`git-commit` 和 `managed-directory` 可以作为后续或测试适配器存在，但不能标记为 V1 已支持。

1. 获准维护者创建或选择 Project，并登记 Repository 的名称、治理范围和预期 Java/Spring/Maven 版本。
2. 维护者创建版本化 Policy，选择已发布 Rule、参数和允许的 severity。
3. 维护者上传无密钥内容归档；Platform 计算 SHA-256，把 digest 作为不可变输入身份，可另存不参与 Scanner 契约的显示标签。
4. 用户选择 Repository、归档版本和 Policy，手动创建 Scan；Platform 先持久化业务 Scan，再异步调用 Scanner。
5. 用户查询 Scan 状态，可在终态前请求取消；重试、迟到结果和部分成功遵循 D11。
6. 用户查看 Finding 的 Rule、severity、subject 和最小 Evidence，并单独查看 Diagnostic。
7. 用户在 ArchGuard 外部决定修复或豁免；V1 不修改 Repository，也不把 Finding 生命周期写回 Scanner。

具体角色名称和 REST 路径由 M2/M3 Technical Design 定义，但不得削弱“维护者才能变更、获准成员才能读取、所有动作绑定 Project”的授权语义。

## 必选 Capability

| Capability ID | 必选输出 | 最小覆盖 | 明确限制 |
|---|---|---|---|
| `java.source-structure` | `java.package`、`java.type` Fact | package、class/interface/enum/record、嵌套类型、source path | 不运行 Annotation Processor，不推断生成类型 |
| `java.type-dependencies` | `java.type-dependency` Fact | import、继承/实现、注解类型、字段/record component、构造器/方法签名、可解析对象创建与类型引用 | 不承诺反射、字符串类名、动态调用或完整方法调用图 |
| `spring.component-model` | `spring.bean`、`spring.injection` Fact | 直接 stereotype、`@Configuration`/`@Bean`、构造器/字段注入、归档内可解析类型 | 不模拟容器、profile、condition、proxy、XML context 或外部依赖 Bean |
| `maven.project-model` | `maven.module`、`maven.dependency` Fact | 坐标、parent、packaging、modules、properties、dependencyManagement/dependencies、scope/optional/exclusions | 不执行插件，不读用户 settings，不解析远程 parent/BOM/transitive graph/profile activation |

所有 kind 都必须有严格、版本化 Schema。无法静态解析的表达式或外部类型产生 Diagnostic，不能猜测 Fact；只有被 Finding 引用或明确请求导出的公共 Fact 才跨 D11 边界。

## 首批 Rule

| Rule ID | 输入 | 默认 severity | 允许覆盖 | 违反条件与 Evidence |
|---|---|---|---|---|
| `archguard.forbidden-dependency` | `java.type-dependency` | `ERROR` | `WARNING/ERROR/CRITICAL` | source package/type 命中 from pattern，target 命中禁止 to pattern；Evidence 指向产生依赖的源码位置和符号 |
| `archguard.package-cycle` | `java.type-dependency` | `ERROR` | `WARNING/ERROR/CRITICAL` | 归档内主源码 package 图形成强连通分量；每个 Finding 使用规范循环身份和最小闭合边证据 |
| `spring.field-injection` | `spring.bean`、`spring.injection` | `WARNING` | `INFO/WARNING/ERROR` | Spring Bean 中字段直接使用 `@Autowired`/`@Inject`/`@Resource`；Evidence 指向字段声明 |
| `maven.forbidden-dependency` | `maven.dependency` | `ERROR` | `WARNING/ERROR/CRITICAL` | 声明坐标命中 Policy 禁止的 group/artifact pattern；Evidence 指向 POM dependency 声明 |

Rule 参数必须由 M4 发布严格 Schema；模式语法、大小写和匹配对象在 Schema 示例中唯一规定。Rule 只判定能由规范 Fact 证明的违反，不因未知输入产生 Finding。

## 功能需求

| ID | 需求 |
|---|---|
| `V1-FR-001` | 获准维护者可以创建/查询 Project，并且未授权主体不能读取或修改其资源。 |
| `V1-FR-002` | 维护者可以在 Project 内登记/停用 Repository，并声明 V1 技术栈范围。 |
| `V1-FR-003` | 维护者可以创建版本化 Policy；未知 Rule、版本、severity 或参数必须被拒绝。 |
| `V1-FR-004` | 用户可以上传 `content-archive`；系统计算/验证 digest，拒绝路径逃逸、特殊文件和超限输入。 |
| `V1-FR-005` | 用户可以对 Repository、归档 digest 和 Policy 快照手动创建幂等 Scan。 |
| `V1-FR-006` | 用户可以查询 Scan 与 Capability 状态，并请求幂等取消；失败、部分成功和迟到结果不能覆盖正确终态。 |
| `V1-FR-007` | Scanner 按兼容快照产生 Java 结构与类型依赖 Fact/Evidence。 |
| `V1-FR-008` | Scanner 按兼容快照产生 Spring Bean 与注入 Fact/Evidence，并对不完整静态语义诊断。 |
| `V1-FR-009` | Scanner 只读解析归档内 Maven POM 4.0.0，产生 module/dependency Fact/Evidence。 |
| `V1-FR-010` | Scanner 使用不可变 PolicySnapshot 执行四条首批 Rule，并产生确定排序、引用闭合的 Finding。 |
| `V1-FR-011` | 获准用户可以分页、筛选并查看 Scan、Finding、Evidence 和 Diagnostic，且状态/版本不被隐藏。 |
| `V1-FR-012` | Platform 记录 Project/Repository/Policy/Scan 的关键创建、变更、取消、结果接收和安全拒绝审计。 |
| `V1-FR-013` | 停用/删除 Repository 后禁止新 Scan；结果与审计按已配置策略处理，删除动作可追踪且不遗留 Scanner 工作区。 |

## 非功能需求

| ID | 需求与发布门禁 |
|---|---|
| `V1-NFR-001` | 相同规范输入、版本、Policy 和资源条件重复执行，移除观测字段后的结果必须与黄金向量精确一致。 |
| `V1-NFR-002` | Repository 始终不可信；目标代码执行、Analyzer 网络、凭据泄漏、根外读取和跨 Scan 访问测试必须全部阻断。 |
| `V1-NFR-003` | 所有 Project 资源读写均校验归属；验收集中的未授权/越权请求阻断率必须为 100%。 |
| `V1-NFR-004` | Platform/Scanner 只使用共同支持的 Scanner `0.1.x` 兼容线；未知字段、枚举、错误码和悬空引用失败关闭。 |
| `V1-NFR-005` | 每次执行具有有限 deadline、文件、字节、深度、内存、进程和输出上限；缺少硬上限时生产 Scanner 不得就绪。 |
| `V1-NFR-006` | 日志包含 traceId/scanId/requestId、版本、状态和安全计数，不含凭据、源码片段、完整 remote 或主机绝对路径。 |
| `V1-NFR-007` | 固定小/中型合成样例必须发布可复现耗时与资源基线；G4 不虚构延迟目标，基线回归阈值由 M4/M5 报告接受后配置。 |
| `V1-NFR-008` | Scanner 工作区正常立即清理、异常 24 小时内补偿；Platform 结果/审计保留必须是显式有限配置并支持授权删除。 |

## 验收标准

详细场景和证据位置由 [D15 验收矩阵](v1-acceptance-matrix.md)定义。V1 进入发布候选至少满足：

- 每个 `V1-FR-*` 与 `V1-NFR-*` 都有自动化或明确人工验收证据，没有空白映射。
- Java 17/21、Boot 3.4/3.5、Framework 6.2 和 Maven POM 4.0.0 的正常、违规、部分失败与不支持样例全部通过。
- 四条 Rule 的正例、反例、边界、稳定 ID/fingerprint 和排序黄金测试全部通过。
- 未授权、恶意归档、目标命令、网络、凭据、超限、取消、清理失败和引用污染测试全部通过。
- 新维护者能按文档在固定样例完成登记、上传、手动扫描和证据查看，所有步骤有可定位证据。

## 指标

| 类型 | 指标 | V1 判定 |
|---|---|---|
| 成功 | 核心旅程可完成性 | 固定任务清单 100% 完成；耗时只记录基线，不在 G4 承诺数值 |
| 成功 | 黄金结果确定性 | 全部固定样例精确一致 |
| 成功 | Finding 引用完整性 | 验收结果 100% 引用有效 Rule、Fact 和 Evidence |
| 防护 | 高风险安全失败 | 目标执行、越权、凭据/源码泄漏和根外访问为 0 |
| 防护 | 支持声明 | 没有实现、自动验收、使用与限制证据时保持“未支持” |

## 风险、依赖与开放问题

| 项目 | 处理方式或 Owner |
|---|---|
| Java 25 与 Boot 4 会增加语法/框架面 | 明确排除 V1；M4 以 parser spike 和独立样例决定 V1.x 候选，不静默扩展 |
| 静态 Spring 模型无法还原运行时容器 | 返回明确 Diagnostic，只对可证明 Fact 执行 Rule；Scanner/M4 |
| Maven parent/BOM/profile 可能依赖远程环境 | 只解析归档闭包；未解析值不猜测并诊断；Scanner/M4 |
| 具体 API、表结构、角色名和 UI 未定义 | 分别由 M2/M3 Technical Design 决定，但保持本文授权与状态语义 |
| 资源、延迟和结果/审计保留数值缺少基线 | M4/M5/M12 建立并评审；发布前 Deploy 必须提供有限配置 |
| 模块化单体与 PostgreSQL 的实现边界 | 由 ADR-0004/0005 和 M2 Technical Design 约束，不在 Feature Spec 复制实现选择 |

## 兼容、交付与回滚

规范与样例先行，Scanner 提供 `0.1.x` Schema/Rule/黄金测试，Platform 再实现消费者与 Fake adapter，最后启用真实集成并由 Deploy 固定兼容组合。回滚从 Platform 消费方回退到上一共同兼容线，再回退 Scanner；数据库迁移必须保持向后读取路径，Samples 始终固定契约版本。

当前文档没有运行时制品；回滚本切片只需撤销本分支。跨仓库实施顺序和阶段入口见 [D16 追踪与阶段计划](v1-delivery-traceability.md)。
