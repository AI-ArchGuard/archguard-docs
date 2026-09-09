# V1 交付追踪与阶段入口

- 切片：D16
- Issue：[archguard-docs#10](https://github.com/AI-ArchGuard/archguard-docs/issues/10)
- Owner：ArchGuard 项目所有者
- 状态：Accepted
- 适用范围：D14 需求到架构、ADR、仓库、工程里程碑和 D15 验收证据的双向追踪
- 依赖：D14 Feature Spec、D15 验收矩阵、G1–G3、M0–M13 路线图
- 最后评审：2026-09-09（G4 V1 可开发性评审通过）

## 本文解决的问题

本文规定 V1 的实现应从哪里开始、每个阶段能声称什么完成、跨仓库按什么顺序兼容交付，以及如何证明没有需求、架构或测试脱节。G4 已通过，但当前所有实现项均未开始；本文合并不授权跳过 M2–M5 各自的 Issue、Technical Design 和退出门禁。

## 事实来源

| 信息 | 唯一事实来源 |
|---|---|
| 用户价值、V1 范围和稳定需求 ID | [D14 Feature Spec](v1-java-spring-feature-spec.md) |
| 验收场景、样例和证据字段 | [D15 验收矩阵](v1-acceptance-matrix.md) |
| 产品版本与工程里程碑关系 | [产品路线图](../product/roadmap.md) |
| Platform/Scanner/仓库边界 | [D07–D10](../architecture/README.md)与 G2 评审 |
| Scanner 契约、结果、Rule 和安全 | [D11–D13](../architecture/README.md)与 G3 评审 |
| 实现阶段操作约束 | [分阶段开发提示词](../engineering/prompts.md) |
| 当前是否“已支持” | [支持矩阵](../product/support-matrix.md)及可定位发布证据 |

Issue、PR 和项目看板只跟踪工作状态，不得复制或悄悄改变以上规范语义。

## 需求追踪矩阵

| 需求 | 主要架构/ADR | 主要仓库 | 工程阶段 | 验收场景 |
|---|---|---|---|---|
| `V1-FR-001` Project 与授权 | D08 Platform 模块化单体、D09 仓库边界 | Platform | M2 | `AC-AUTH-001` |
| `V1-FR-002` Repository 治理 | D07 信任边界、D08、D09 | Platform | M3 | `AC-REPO-001` |
| `V1-FR-003` Policy | D08、D12、ADR-0002 | Platform、Scanner | M3/M4 | `AC-POLICY-001` |
| `V1-FR-004` 内容归档 | D11、D13、ADR-0003 | Platform、Scanner、Samples | M4/M5 | `AC-INPUT-001` |
| `V1-FR-005` 手动 Scan | D08、D11、ADR-0001 | Platform | M3/M5 | `AC-SCAN-001` |
| `V1-FR-006` 状态/取消/重试 | D08、D11 | Platform、Scanner | M3/M5 | `AC-SCAN-002` |
| `V1-FR-007` Java Fact | D10–D12、ADR-0002 | Scanner、Samples | M4 | `AC-JAVA-001` |
| `V1-FR-008` Spring Fact | D10–D12、ADR-0002 | Scanner、Samples | M4 | `AC-SPRING-001` |
| `V1-FR-009` Maven Fact | D10–D13、ADR-0003 | Scanner、Samples | M4 | `AC-MAVEN-001` |
| `V1-FR-010` 四条 Rule | D12、ADR-0002 | Scanner、Samples | M4 | `AC-RULE-001` |
| `V1-FR-011` 结果查询 | D08、D11–D12 | Platform、Scanner | M3/M5 | `AC-RESULT-001` |
| `V1-FR-012` 审计 | D07–D08、D13 | Platform、Deploy | M2/M3/M5 | `AC-AUDIT-001` |
| `V1-FR-013` 停用/删除 | D07–D08、D13 | Platform、Scanner、Deploy | M3/M5/M11 | `AC-DELETE-001` |
| `V1-NFR-001` 确定性 | D11–D12、ADR-0002 | Scanner、Samples | M4/M5 | `AC-DET-001` |
| `V1-NFR-002` 不可信输入 | D07、D13、ADR-0003 | Scanner、Deploy、Samples | M4/M5/M11 | `AC-SEC-001` |
| `V1-NFR-003` 资源授权 | D07–D09 | Platform | M2/M3/M5 | `AC-AUTH-002` |
| `V1-NFR-004` 契约兼容 | D09、D11–D12、ADR-0001 | Scanner、Platform、Samples、Deploy | M4/M5/M11 | `AC-CONTRACT-001` |
| `V1-NFR-005` 有限资源 | D11、D13、ADR-0003 | Scanner、Deploy | M4/M5/M11 | `AC-LIMIT-001` |
| `V1-NFR-006` 可观测/最小化 | D07–D08、D13 | Platform、Scanner、Deploy | M2–M5/M11 | `AC-OBS-001` |
| `V1-NFR-007` 性能基线 | D11、质量门禁 | Scanner、Platform、Deploy | M4/M5/M12 | `AC-BASELINE-001` |
| `V1-NFR-008` 保留与清理 | D07、D13、ADR-0003 | Scanner、Platform、Deploy | M5/M11 | `AC-RETENTION-001` |

新增、拆分或删除需求时必须在同一变更中更新 D14、D15 和本表。没有验收场景或责任仓库的需求不能进入 Ready。

## G4 入口与退出

### 进入 G4

- G1、G2、G3 均已 Accepted，且当前事实和支持状态没有冲突。
- D14 可以保持 Draft、D15–D16 可以保持 Proposed，用于评审和收敛。
- 不要求任何 V1 业务代码、Schema 或样例已经存在。

### G4 通过条件

- D14 的目标、非目标、用户流程、版本范围、Capability、Fact、Rule 和需求 ID 无阻断歧义。
- D15 覆盖每个需求，正常/失败/安全/确定性/兼容场景具有所有者和计划证据。
- 本文将每个需求映射到架构、仓库、阶段和验收，M2–M5 的入口/退出可独立判断。
- 七仓库 README/AGENTS 与规范没有职责或支持声明冲突。
- 所有开放问题都有 Owner 和最迟决策阶段；会改变 M2 架构或数据边界的问题必须在 G4 前关闭。
- G4 评审记录接受 D14–D16 后，D14 改为 Ready、D15–D16 改为 Accepted，并允许开始 M2。

## V1 开发阶段同步

### M2：Platform 骨架与 Project 垂直切片

入口：G4 Accepted；D14 为 Ready、D15–D16 为 Accepted；M2 Issue 与 Technical Design 已评审；模块化单体/PostgreSQL 决策入口明确；Platform 工作树与基线干净。

必须交付：

- 可复现的 Java/Spring Boot 构建、模块化单体边界、Flyway 空库迁移和健康检查。
- `V1-FR-001` 的最小 Project 创建/查询与 `V1-NFR-003` 授权骨架。
- 统一错误、traceId、审计端口和不依赖 Web/数据库的领域层架构测试。

退出：M2 提示词的构建/迁移/架构/集成检查通过；只允许声称 Platform 骨架与 Project 最小切片完成，不能声称 Scan 或分析已支持。

### M3：Repository、Policy、Scan 与 Fake Scanner

入口：M2 退出证据通过；M3 Feature/Technical Design 已关联 D14；Fake adapter 明确实现 D11 语义而不复制 Scanner 内部类。

必须交付：

- Repository 登记/停用、Policy 生命周期、Scan 状态机、幂等/取消/重试和结果查询持久化。
- Fake Scanner 正常、部分、失败、取消和迟到结果场景；权限、审计和迁移测试。
- `V1-FR-002/003/005/006/011/012/013` 的 Platform 侧证据。

退出：核心控制面流程可用 Fake 复现；不能把 Fake 输出当作 Java/Spring/Maven 能力已支持。

### M4：Scanner `0.1.x` 与确定性分析

入口：D11–D14 不再有 Scanner 语义阻断；M4 Technical Design 冻结 parser、Schema 文件组织、Rule/Fact 接口、初始资源值和许可；Samples 计划已评审。

必须交付：

- Scanner `0.1.0` Schema、有效/无效示例、提供方测试和 ID 黄金向量。
- D14 四个 Capability、七类公共 Fact/Evidence 和四条 Rule 的最小实现。
- D15 Java/Spring/Maven/Rule/确定性/契约/恶意输入/资源超限样例与报告。
- 非 root、无目标执行、分析期无网络、有限资源和工作区清理的本地/CI 证据。

退出：Scanner 独立验证通过并发布可定位 `0.1.x` 制品；仍不能声称 Platform 真实扫描闭环完成。

### M5：真实异步扫描集成

入口：M3 Platform 消费方和 M4 Scanner 提供方分别通过；共同 `0.1.x` 兼容线与回滚组合已记录；输入/传输/隔离 Technical Design 已评审。

必须交付：

- Platform、Scanner、Samples 的真实 content-archive 异步主路径。
- 双边 Schema、幂等、取消、重试、迟到结果、部分成功、权限、审计、清理和补偿测试。
- D15 核心用户旅程和小/中样例集成基线，使用说明与限制说明。

退出：D14 功能闭环在固定版本组合上可重复完成，失败可定位并可回滚；支持矩阵仍须等待发布级证据才能升级为“已支持”。

## 发布级证据

M6–M10 分别服务 V2–V4，不是 V1 功能闭环依赖。以下跨版本阶段仍为 V1 对外升级“已支持”所需证据：

| 阶段 | V1 所需结果 | 不要求 |
|---|---|---|
| M11 | 可重复启动、有限配置、制品兼容矩阵、备份/恢复/回滚和清理 Runbook 演练 | 不要求 Kubernetes 或公网数据库 |
| M12 | 固定环境性能/资源基线和回归预算；有证据的优化结论 | 不要求引入 Kubernetes，也不虚构 SLO |
| M13 | D14–D16 双向追踪 100%、P0 关闭、演示可复现、声明与限制一致 | 不新增大型功能 |

只有 D15 全部发布门禁通过、使用/限制文档齐备且支持矩阵附上实现和证据链接后，V1 目标才能升级为“已支持”。

## 工作拆分与状态规则

- 每个 Issue 只交付一个 0.5–2 天的可验证切片，标题包含主要 requirement/scenario ID。
- 跨仓库工作拆成规范/样例、提供方、消费方、部署四类 Issue；一个仓库一个分支和 PR。
- Feature Spec 状态：`Draft` 表示评审中，`Ready` 表示 G4 已通过，`Developing` 表示首个 M2 实现开始，`Done` 表示 D15 全部发布证据通过；D15/D16 使用 `Proposed/Accepted`。
- 单个需求可在追踪工具中标记 planned/developing/verified，但不得回写改变规范含义。
- CI 失败、证据缺失或仅手工演示时不能标记 verified；Blocked 必须记录原因和 Owner。

## 跨仓库兼容顺序

1. Docs 接受需求/架构/ADR 变化并声明契约兼容影响。
2. Samples 增加固定输入、digest 和预期输出，不依赖未发布实现。
3. Scanner 发布兼容 Schema/Rule/Analyzer 制品和提供方证据。
4. Platform 更新消费者测试、Fake adapter 和业务持久化，再启用真实适配器。
5. Deploy 记录 Platform/Scanner/Schema/Samples 组合、有限配置和回滚步骤。
6. Evals 只引用已发布结果做后续评估；Gateway 不进入 V1 主路径。

破坏性契约变化先并行发布新 `0.MINOR`；回滚顺序为 Platform 消费线 → Deploy 组合 → Scanner 制品。数据库迁移不得原地修改，样例预期不得为适配错误实现而降低断言。

## G4 前置缺口

| 缺口 | 是否阻断 G4 通过 | 最迟处理 |
|---|---:|---|
| D14–D16 GitHub Issue | 已解决 | Docs #8、#9、#10 已创建并回填 |
| 模块化单体与 PostgreSQL 独立 ADR | 已解决 | ADR-0004、ADR-0005 已由 G4 同组接受 |
| Platform README 的 Maven Wrapper M1/M2 错位 | 已解决 | Platform `docs/align-m2-platform-skeleton` 分支已修正，待独立提交/PR |
| M2/M3/M4/M5 Technical Design 尚不存在 | 否，不阻断 G4；阻断各自阶段入口 | 对应里程碑开始前 |
| 具体资源、性能和业务保留数值无基线 | 否，不虚构；阻断 M4/M5/M11/M12 对应退出 | 对应报告接受前 |
| Java 25、Boot 4、远程 Git 未纳入 V1 | 非缺口，是明确非目标 | 有独立需求证据时进入 V1.x/后续评审 |

## 验收与变更规则

- 从任一 `V1-*` ID 可以定位 D14 定义、D15 场景、本表责任和最终 CI/报告；反向也能从证据定位需求。
- G4 评审要逐行确认映射完整，不以“后续实现再说”接受改变架构或数据边界的空项。
- Accepted/Ready 后若目标用户、V1 输入、版本、Capability、Rule、信任边界或发布门禁发生实质变化，必须重新进行 G4 级评审；架构变化同时新增或取代 ADR。
- 当前回滚只需撤销本分支，不触及其他仓库、数据库或运行环境。
