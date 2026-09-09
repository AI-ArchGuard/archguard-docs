# ArchGuard 分阶段开发提示词

本目录把 ArchGuard 建设拆成可独立执行、验证和回滚的阶段。每次只选择一个阶段文件，不要一次要求 Codex 生成整个系统。

## 使用方式

1. 先填写执行参数。
2. 把本文件的“统一执行约束”和一个阶段文件一起交给 Codex。
3. 阶段较大时，只执行阶段文件中的一个子阶段。
4. 阶段完成后保存测试、兼容和交付证据，再进入下一阶段。

## 执行参数

```text
<workspace-path>        七仓库工作区绝对路径
<issue-number>          当前 Issue 编号和链接
<target-version>        本次目标版本；开发期使用 0.x.y
<baseline-commit>       开始工作前各受影响仓库的提交
<target-environment>    Local / CI / Staging / Production
<related-spec>          Feature Spec 路径
<related-design>        Technical Design 路径；不适用时写 N/A
<related-adr>           ADR 路径；不适用时写 N/A
```

缺少的信息如果不会改变方案，可明确记录合理假设后继续；如果会改变范围、契约、安全边界、数据处理或外部写操作，必须停止并请求确认。

## 统一执行约束

执行任何阶段时必须遵守以下规则：

### 开始前

1. 阅读工作区 `AGENTS.md`、目标仓库 `README.md` 和仓库级 `AGENTS.md`。
2. 阅读相关 Feature Spec、Technical Design、ADR，以及：
   - [治理规范](governance.md)
   - [开发流程](development-workflow.md)
   - [工程规范](engineering-standards.md)
   - [质量门禁](quality-gates.md)
   - [安全与可观测性](security-and-observability.md)
   - [发布与运行](release-and-operations.md)
3. 检查所有受影响仓库的工作树、当前分支、远程地址和现有测试，不覆盖或混入用户已有修改。
4. 先报告实施计划、影响范围、风险、依赖、验证方式和回滚方案，再开始修改。
5. 新增依赖前说明用途、许可证、维护状态、现有替代方案和替换成本。

### 实施中

1. 一次只处理一个明确问题，优先完成端到端最小切片。
2. 实现顺序原则上为：契约与测试 → 领域逻辑 → 适配器 → API → 可观测性 → 文档。
3. 缺陷修复必须先增加能够复现问题的测试。
4. 不得删除测试、降低断言、吞掉异常或绕过质量门禁。
5. 不执行超出任务授权的提交、推送、发布、外部写操作或破坏性操作。
6. 不提交密钥、Token、密码、真实客户源码、个人数据或未经脱敏的生产记录。

### 完成前

1. 运行最小相关测试，再运行目标仓库声明的完整质量检查。
2. 检查安全、权限、错误处理、日志、指标、审计、兼容性和回滚。
3. 跨仓库变化必须记录契约版本、兼容矩阵、发布顺序和回滚顺序。
4. 明确区分已通过、失败、未运行和因环境受阻的验证。
5. 最终报告必须包含：
   - 完成了什么；
   - 修改了哪些文件；
   - 关键架构选择；
   - 执行了哪些测试及结果；
   - 已知限制和下一步。

## 阶段顺序

```text
仓库基线
→ 产品与架构文档
→ Platform 骨架
→ 仓库与扫描任务
→ Scanner MVP
→ 真实扫描集成
→ GitHub PR 集成
→ 消息与可靠性
→ MCP Gateway
→ Evals 基线
→ AI 架构评审
→ 部署与 CI/CD
→ 性能与 Kubernetes
→ 求职交付审计
```

MCP Gateway 和 Evals 被放在 AI 评审之前，使工具边界、安全策略和评估基线先于模型功能建立。

V1 的阶段 2–5 必须遵循 [D14 Feature Spec](../requirements/v1-java-spring-feature-spec.md)、[D15 验收矩阵](../requirements/v1-acceptance-matrix.md)和[D16 交付追踪与阶段入口](../requirements/v1-delivery-traceability.md)。G4 已于 2026-09-09 通过，允许开始阶段 2；仍须逐阶段填写并评审 Issue、Technical Design、版本和基线参数，不能把 G4 当作后续实现的通用授权。

## 阶段索引

| 阶段 | 文件 | 主要结果 |
|---|---|---|
| 0 | [仓库基线](prompts/00-repository-baseline.md) | 七仓库治理、模板和基础 CI |
| 1 | [产品与架构文档](prompts/01-product-and-architecture.md) | 产品范围、C4、边界和 ADR |
| 2 | [Java Platform 骨架](prompts/02-platform-skeleton.md) | 模块化单体和最小垂直切片 |
| 3 | [仓库与扫描任务](prompts/03-scan-workflow.md) | 登记、任务状态机和模拟扫描 |
| 4 | [Java Scanner MVP](prompts/04-scanner-mvp.md) | 版本化契约和确定性规则分析 |
| 5 | [真实扫描集成](prompts/05-real-scan-integration.md) | 异步扫描、重试、清理和端到端测试 |
| 6 | [GitHub PR 集成](prompts/06-github-pr-integration.md) | 安全 Webhook 和只读 PR 反馈 |
| 7 | [消息与可靠性演进](prompts/07-messaging-reliability.md) | 基于证据的队列决策与故障恢复 |
| 8 | [Go MCP Gateway](prompts/08-mcp-gateway.md) | 只读工具、授权、审计和限流 |
| 9 | [Evals 基线与安全中心](prompts/09-evals-baseline.md) | 数据集、评分器、基线和安全门禁 |
| 10 | [AI 架构评审](prompts/10-ai-review.md) | 证据化解释、严格 Schema 和评估 |
| 11 | [部署与 CI/CD](prompts/11-deployment-cicd.md) | Compose、制品晋级、备份和回滚 |
| 12 | [性能与 Kubernetes](prompts/12-performance-kubernetes.md) | 性能证据和有条件的 K8s 引入 |
| 13 | [求职交付审计](prompts/13-delivery-audit.md) | 可复现证据、差距清单和发布准备 |

## 阶段拆分原则

以下阶段默认分批执行：

- 阶段 1：产品文档 → 总体架构 → ADR。
- 阶段 6：安全设计 → Webhook 接入 → PR Check 与评论。
- 阶段 10：评估样例 → AI 实现 → 安全与成本验证。
- 阶段 11：本地部署 → CI → Staging/Production。
- 阶段 12：性能基线 → 优化 → Kubernetes 决策与实施。
- 阶段 13：只读审计 → P0 修复 → 最终发布审查。

每个子阶段应有独立验收结果。未达到当前阶段退出条件时，不进入后续阶段。
