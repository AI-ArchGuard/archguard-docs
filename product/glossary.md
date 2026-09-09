# ArchGuard 术语表

- 状态：Accepted
- 适用范围：产品、需求、架构、契约、代码和用户界面
- 最后更新：2026-09-10

| 术语 | 规范含义 | 不表示什么 |
|---|---|---|
| ArchGuard | Java-first、语言无关架构、AI 增强的软件架构治理平台 | 当前已经支持多语言 |
| Project | ArchGuard 中的治理边界，聚合成员、代码来源、规则和结果 | Git 托管平台中的单个仓库 |
| Artifact | 一个可独立识别的分析单元，例如 Maven module、Go module 或 Python package | Platform 数据库实体 |
| Component | Artifact 内可被依赖、度量或应用规则的结构 | 只等同于 Java class |
| Dependency | 两个 Component 或 Artifact 之间的规范化有向关系 | 对关系是否合规的判断 |
| Metric | 对明确作用域计算的确定性数值 | Rule 的阈值结论 |
| Rule | 对统一模型进行确定性求值的版本化架构约束 | LLM 建议或运行错误 |
| Finding | Rule 求值形成的治理问题，必须引用规则、位置和证据 | 解析失败或 Agent 建议 |
| Evidence | 支撑 Dependency、Metric 或 Finding 的最小可验证依据 | 默认保存完整源码 |
| Diagnostic | 输入、配置、解析或执行异常的结构化诊断 | Rule 违规 |
| Scan | 对确定输入、规则和资源限制执行的一次分析 | 任意构建或无限制代码执行 |
| Scanner | 语言前端、统一模型、确定性规则和报告组成的分析平面 | Platform 的任务状态机 |
| RuleSet | Platform 管理的规则选择、版本、参数和严重性配置 | Rule 执行实现 |
| Baseline | 用于区分历史问题与新增问题的版本化参照 | 删除或隐藏既有问题 |
| Agent Suggestion | 模型基于扫描证据生成的解释或建议 | 确定性事实或自动决策 |
| Contract | 由生产者拥有、版本化且可机器校验的跨仓库边界 | 共享内部类或共享数据库 |
| ADR | 对重要架构选择、替代方案和影响的不可变记录 | 临时计划或会议纪要 |

规范表达只有“已实现”“进行中”“目标”“未启用”四类。只有代码和自动化证据存在时才能写“已实现”；路线图中出现不等于已支持。
