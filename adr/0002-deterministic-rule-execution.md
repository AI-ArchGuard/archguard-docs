# ADR-0002：Scanner 统一执行确定性 Rule

- 状态：Accepted
- 日期：2026-09-09
- 决策者：ArchGuard 项目所有者
- 替代：无

## 背景

Platform 拥有 Policy，Analyzer 理解语言和框架，Scanner runtime 负责执行编排。若三者都能形成 Finding，Rule 版本、错误处理、资源预算和结果身份将出现多套事实来源。

## 决策驱动因素

- Finding 必须由确定性、可重复和可版本化的 Rule 形成。
- Platform 领域层不能依赖解析器或 Analyzer 实现。
- Analyzer 需要提供能力特定 Fact 和 Rule，但不能绕过统一资源与结果校验。
- LLM 输出是不可信建议，不能决定确定性违规。

## 选择

- Scanner runtime 拥有统一 Rule Executor，负责 PolicySnapshot 校验、执行计划、预算、统计、排序和最终 Finding Schema 校验。
- Analyzer 能力模块拥有 Fact 抽取器及语言/框架特定 Rule 实现，并通过 Registry 显式注册 Rule 描述。
- Platform 只拥有 Policy 生命周期、作用域、参数和 severity 配置；每次 Scan 发送不可变快照。
- Rule 只读取声明的规范 Fact，不访问 Platform、网络、凭据或 Analyzer 私有对象。
- LLM 只能解释已验证结果，不能注册/执行 Rule、生成 Fact 或改变 severity。

## 备选方案

- Platform 执行全部 Rule：会复制分析模型并耦合 Scanner 内部语义，拒绝。
- Analyzer 各自完整生成 Finding：实现简单但难以统一预算、版本、身份和失败语义，拒绝。
- LLM 直接判断违规：不可重复、不可审计且会放大提示注入，拒绝。
- 独立 Rule 微服务：当前没有规模或隔离证据，暂不采用。

## 正面影响

- Rule 生命周期、资源控制和 Finding 结构只有一个执行边界。
- Analyzer 仍可拥有领域知识，Platform 保持语言无关。
- 黄金测试可以固定 Fact、Rule、Policy 和 Finding 的完整因果链。

## 负面影响与风险

- Scanner runtime 需要稳定的内部 Fact/Rule 接口和跨能力依赖计划。
- 能力模块若泄漏私有对象，会形成隐式耦合，必须用架构测试限制。
- 通用与能力特定 Rule 的归属需要清晰代码所有权。

## 验证方式

- 固定 Fact/Policy 重复执行得到相同 Finding ID、fingerprint 和排序。
- 未知 Rule/参数、部分 Fact、超时和 Analyzer 失败均有黄金测试。
- 架构测试证明 Platform 不依赖 Rule 实现，Rule 不访问网络和 Platform。

## 何时重新评估

- 第二个技术栈证明规范 Fact 接口无法承载真实 Rule 需求时。
- Rule 数量或执行成本出现可复现的独立扩缩/隔离需求时。
- 确定性框架无法表达获准需求时，先补证据和新 ADR，不转交 LLM。
