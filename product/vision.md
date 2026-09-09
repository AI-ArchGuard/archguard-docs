# ArchGuard 产品愿景

- 状态：Accepted
- 生效日期：2026-09-09
- 决策依据：[ADR-0006](../adr/0006-java-first-phased-delivery.md)

## 最终定位

> 一个 Java-first、语言无关架构、AI 增强的软件架构治理平台。

Java-first 表示第一条深度治理链覆盖 Java 项目，不表示平台模型绑定 Java。ArchGuard 的长期治理对象是软件系统；Go、Python、JavaScript 及跨语言 API、消息和数据库关系通过独立扫描前端逐步接入统一架构模型。

## 核心价值

- 用 Scanner 提供可重复、可定位、可验证的架构事实。
- 用 Platform 管理项目、规则、任务、权限、结果、基线和审计。
- 用 CI 和 PR 门禁阻止新增架构债务，而不只生成一次性报告。
- 用 Agent 解释事实、关联文档并给出低风险建议，由用户作最终决定。
- 用 Gateway 控制 Agent 的工具访问，用 Evals 证明 Agent 的质量与安全。
- 用 Deploy 提供可运行、可观察、可恢复的完整交付。

## 不变量

1. 扫描结果是事实，Agent 建议不是事实。
2. 每个 Finding 必须包含 Rule、位置和 Evidence。
3. Scanner 契约版本化，且不依赖 Platform 内部类。
4. 统一模型不暴露语言 AST、编译器对象或 Java 专属类型。
5. Platform 初期保持模块化单体，没有真实证据不拆微服务。
6. Gateway 不复制 Platform 业务逻辑，也不直连其数据库。
7. Evals 不成为线上核心请求的强依赖。
8. LLM 输出必须经过 Schema、权限和业务校验。
9. 新技术必须对应明确问题并记录 ADR。
10. 每个阶段独立演示、发布和回滚。

## 成功形态

开发者能够在本地或 CI 中确定地发现架构问题；团队能够在 Platform 中管理规则、基线、例外和历史；Agent 能引用真实证据解释问题；所有工具调用与治理动作可授权、可审计；平台能够在不改变控制面核心模型的前提下接入新的语言扫描器。
