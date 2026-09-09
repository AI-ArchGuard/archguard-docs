# V1 验收矩阵

- 切片：D15
- Issue：[archguard-docs#9](https://github.com/AI-ArchGuard/archguard-docs/issues/9)
- Owner：ArchGuard 项目所有者
- 状态：Accepted
- 适用范围：D14 中全部 V1 功能与非功能需求的验证场景、证据和所有者
- 依赖：D14 Feature Spec、D11–D13、统一质量门禁
- 最后评审：2026-09-09（G4 V1 可开发性评审通过）

## 本文解决的问题

本文把每个 V1 需求绑定到可执行场景、合成样例、测试层、责任仓库和退出证据。表中“计划”表示尚无实现和测试；只有证据清单指向已运行结果后才能改为“通过”。

## 验收原则

- 所有输入均为合成、可公开、固定版本的数据，不复制真实客户源码。
- 正常、违规、不支持、恶意、超限、取消和恢复路径均进入自动化验收。
- Finding 期望使用 Rule、fingerprint、Fact/Evidence 引用表达，不以易变 message 或行号作为唯一断言。
- 确定性用 D11 规范投影比较；安全零容忍场景不能靠人工目测放行。
- 每次证据记录仓库提交、制品版本、契约版本、样例 digest、Policy 版本、环境和命令。
- 尚无基线的耗时/资源只记录测量值；不得在实现后反向修改用例来制造通过。

## 测试层与证据位置

| 层级 | 主要所有者 | 证据要求 |
|---|---|---|
| Schema/契约 | `archguard-scanner`、`archguard-platform` | 有效/无效 JSON、消费者/提供方兼容报告、黄金向量 |
| 领域/模块 | Platform 或 Scanner 对应仓库 | 单元/模块测试结果、架构边界测试、迁移测试 |
| 样例/黄金 | `archguard-samples`、`archguard-scanner` | 固定样例 digest、预期 Fact/Finding/Diagnostic、重复执行结果 |
| 集成/端到端 | Platform、Scanner、Samples、Deploy | 版本组合、启动证据、用户旅程和故障路径报告 |
| 安全 | Scanner、Platform、Deploy | 越权/路径/网络/执行/泄漏/清理负例与零容忍结果 |
| 基线 | Scanner、Platform、Deploy | 固定环境、输入规模、耗时和资源原始结果及摘要 |
| 文档/人工 | Docs 与产品所有者 | 使用步骤、限制说明、十分钟阅读和核心任务清单 |

具体报告文件由对应里程碑创建；D16 定义路径约定和阶段完成规则。

## 合成样例目录

以下是必须创建的稳定 fixture ID，不预先规定目录实现。每个样例 README 必须记录许可证、契约版本、digest、支持版本和期望结果。

| Fixture ID | 内容 | 主要期望 |
|---|---|---|
| `v1-java17-clean` | Java 17 单模块、合规层次 | 无 Finding，Java capabilities `COMPLETED` |
| `v1-java21-records` | Java 21 record/sealed 类型与依赖 | 结构和依赖 Fact 稳定，无误解析 |
| `v1-java-forbidden-dependency` | application 包依赖 adapter 禁止目标 | 1 个 `archguard.forbidden-dependency` |
| `v1-java-package-cycle` | 三个 package 构成最小循环 | 规范循环 Finding 和闭合边 Evidence |
| `v1-spring34-clean` | Boot 3.4、Framework 6.2、构造器注入 | Bean/injection Fact，字段注入 Finding 为 0 |
| `v1-spring35-field-injection` | Boot 3.5、字段注入 | 1 个 `spring.field-injection` |
| `v1-spring-dynamic-partial` | condition/profile/外部 Bean 无法静态解析 | Spring capability `PARTIAL` 与稳定 Diagnostic，无猜测 Finding |
| `v1-maven-multimodule` | 本地 parent、properties、dependencyManagement、modules | module/dependency Fact 完整且排序稳定 |
| `v1-maven-forbidden-dependency` | 命中禁止坐标 | 1 个 `maven.forbidden-dependency` |
| `v1-maven-unresolved` | 远程 parent/profile/未解析 property | 明确 Diagnostic，禁止网络和猜测值 |
| `v1-unsupported-versions` | Java 25、Boot 4、POM 非 4.0.0 | 对应能力失败/部分成功，其他独立能力按 D11 保留 |
| `v1-malicious-archive` | Zip Slip、链接、特殊文件、碰撞和压缩炸弹变体 | 全部失败关闭，无根外写入/读取 |
| `v1-resource-limit` | 文件、字节、深度、时间、输出各超限变体 | 稳定超限 Diagnostic、正确终态和清理 |

## 功能需求验收

| 需求 | 场景 ID | Given / When / Then | 层级与所有者 | 状态 |
|---|---|---|---|---|
| `V1-FR-001` | `AC-AUTH-001` | Given 两个 Project 的维护者/查看者，When 创建、读取、修改跨 Project 资源，Then 只允许授权范围且拒绝有审计 | Platform 模块/集成 | 计划 |
| `V1-FR-002` | `AC-REPO-001` | Given 已授权 Project，When 登记、查询、停用 Repository，Then 归属/版本范围可见且停用后拒绝新 Scan | Platform 模块/API | 计划 |
| `V1-FR-003` | `AC-POLICY-001` | Given 四条已发布 Rule，When 创建有效与含未知 Rule/version/severity/parameter 的 Policy，Then 有效版本化保存、无效原子拒绝 | Platform + Scanner Schema | 计划 |
| `V1-FR-004` | `AC-INPUT-001` | Given 正常与 `v1-malicious-archive`，When 上传并物化，Then digest 可复算，恶意/超限输入失败且根外无副作用 | Platform/Scanner 安全集成 | 计划 |
| `V1-FR-005` | `AC-SCAN-001` | Given 相同 Repository/digest/Policy 和幂等键，When 重复创建，Then 返回同一业务 Scan；新执行 attempt 身份符合 D11 | Platform 状态机/契约 | 计划 |
| `V1-FR-006` | `AC-SCAN-002` | Given 排队/运行/已终态 Scan，When 查询、取消、重复取消、重试并接收迟到结果，Then 终态和副作用符合 D11 | Platform + Fake/真实 Scanner | 计划 |
| `V1-FR-007` | `AC-JAVA-001` | Given `v1-java17-clean` 与 `v1-java21-records`，When 扫描，Then Java Fact/Evidence 与黄金结果精确一致 | Scanner 黄金 | 计划 |
| `V1-FR-008` | `AC-SPRING-001` | Given Spring 3.4/3.5 正常与动态样例，When 扫描，Then Bean/injection Fact 正确，未知语义只产生 Diagnostic | Scanner 黄金 | 计划 |
| `V1-FR-009` | `AC-MAVEN-001` | Given多模块与未解析样例，When 静态解析 POM，Then 本地闭包 Fact 正确且没有构建、插件或网络执行 | Scanner 黄金/安全 | 计划 |
| `V1-FR-010` | `AC-RULE-001` | Given 四组正反例与固定 Policy，When 执行 Rule，Then Finding 数量、ID/fingerprint、severity、排序和引用精确一致 | Scanner Rule 黄金 | 计划 |
| `V1-FR-011` | `AC-RESULT-001` | Given SUCCEEDED/PARTIAL/FAILED/CANCELLED 结果，When 分页筛选查询，Then 状态、版本、Finding/Evidence/Diagnostic 完整且越权拒绝 | Platform API/集成 | 计划 |
| `V1-FR-012` | `AC-AUDIT-001` | Given关键创建/变更/取消/结果/安全拒绝，When 查询审计，Then actor、范围、trace、版本和结果关联完整且无源码/凭据 | Platform 模块/安全 | 计划 |
| `V1-FR-013` | `AC-DELETE-001` | Given 有历史 Scan 的 Repository，When 停用/授权删除，Then 新 Scan 被拒、业务保留策略执行、Scanner 工作区无残留且动作可审计 | Platform/Scanner/Deploy 集成 | 计划 |

## 非功能需求验收

| 需求 | 场景 ID | 验收断言 | 层级与所有者 | 状态 |
|---|---|---|---|---|
| `V1-NFR-001` | `AC-DET-001` | 所有黄金样例至少重复执行 3 次；规范投影、ID 和排序逐字节一致 | Scanner 黄金 | 计划 |
| `V1-NFR-002` | `AC-SEC-001` | hooks/filter/LFS/submodule/目标命令/SSRF/链接/特殊文件/跨任务读取/源码或凭据泄漏全部为 0 | Scanner + Deploy 安全 | 计划 |
| `V1-NFR-003` | `AC-AUTH-002` | Project/Repository/Policy/Scan/Result/Audit 的未授权和跨 Project 矩阵拒绝率 100% | Platform 权限集成 | 计划 |
| `V1-NFR-004` | `AC-CONTRACT-001` | `0.1.x` 有效组合通过；未知字段/枚举/错误码、身份冲突、悬空引用和无共同兼容线全部拒绝 | 双边契约 | 计划 |
| `V1-NFR-005` | `AC-LIMIT-001` | 每类资源上限均有单独超限用例；无硬上限配置时生产 profile readiness 失败 | Scanner + Deploy | 计划 |
| `V1-NFR-006` | `AC-OBS-001` | 成功/失败/取消链路可按 traceId 关联；日志/指标扫描不含凭据、源码、完整 remote 或主机绝对路径 | Platform/Scanner/Deploy | 计划 |
| `V1-NFR-007` | `AC-BASELINE-001` | 固定小/中样例记录环境、版本、输入规模、p50/p95、CPU/内存/磁盘/输出；结果可重复且不冒充 SLO | Scanner/Platform 基线 | 计划 |
| `V1-NFR-008` | `AC-RETENTION-001` | 正常立即清理、异常 24 小时补偿、超期 worker 隔离均经演练；业务保留配置有限且删除可验证 | Scanner/Platform/Deploy | 计划 |

## 关键组合与失败矩阵

| 条件 | 期望总体状态 | 必须保留 | 必须为空或拒绝 |
|---|---|---|---|
| 所有请求 Capability 完成、无 error/截断 | `SUCCEEDED` | 验证通过且引用闭合的结果 | 无 |
| Spring 动态语义不完整，Java/Maven 完成 | `PARTIAL` | 独立完整能力结果、Diagnostic | 依赖未知 Spring Fact 的 Finding |
| 不支持 Boot 版本，Java/Maven 仍完整 | `PARTIAL` | Java/Maven 结果、版本 Diagnostic | Spring 推测结果 |
| 契约/身份/摘要/路径/输出引用无效 | `FAILED` | 最小 Diagnostic | facts/findings/evidence |
| 用户取消且提交点未完成 | `CANCELLED` | 能力状态与取消 Diagnostic | facts/findings/evidence |
| 输出截断 | `PARTIAL` | 返回计数、原始计数、超限 Diagnostic | `SUCCEEDED` 状态 |
| 清理失败但结果可验证 | `PARTIAL` | 业务结果与清理 Diagnostic | 完全成功声明 |
| 清理/污染使结果不可证明 | `FAILED` | 最小 Diagnostic 与安全审计 | 业务结果 |

## 证据清单

每次阶段或发布验收生成机器可读清单或等价报告，至少包含：

| 字段 | 要求 |
|---|---|
| `requirementIds` / `scenarioIds` | 本次覆盖的稳定 ID，去重排序 |
| `repositoryCommits` | 每个受影响仓库的完整提交 SHA |
| `artifactVersions` | Platform、Scanner、Analyzer、Schema、Rule 和 Deploy 版本 |
| `fixtureDigests` | 使用的 Samples commit 与内容 SHA-256 |
| `environment` | OS/JDK/容器/CPU/内存及关键有限配置，不含 Secret |
| `commands` | 可复现命令与退出码 |
| `result` | PASS/FAIL/BLOCKED；失败不能省略 |
| `evidenceLinks` | CI、报告、日志摘要和限制文档的稳定位置 |

## 阶段门禁

- M2/M3 可以使用 Fake Scanner 验证 Platform 领域和流程，但不能把 `AC-JAVA-*`、`AC-SPRING-*`、`AC-MAVEN-*` 或真实安全场景标为通过。
- M4 必须通过 Scanner Schema、黄金、Rule、确定性和输入安全的独立验收，才能进入真实集成。
- M5 必须通过双边契约、端到端、取消/重试/清理、权限和结果查询场景，才能称 V1 功能闭环完成。
- M11/M12/M13 分别补足可部署/回滚、性能基线和最终证据审计；M6–M10 的 V2–V4 功能不是 V1 发布依赖。

## 开放问题

- 每个场景的实际命令和报告路径由对应 Technical Design 在实现前补齐。
- 小/中型样例的规模定义和回归预算由 M4/M5 首次可复现基线决定。
- 人工核心旅程的参与者与任务耗时只记录基线；没有用户研究前不设置体验 SLO。
- 当前所有场景均为计划状态；本文合并不代表任何 V1 验收已经运行。
