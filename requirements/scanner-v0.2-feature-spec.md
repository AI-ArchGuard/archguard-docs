# Feature Spec：Java Scanner MVP `v0.2.0-scanner`

- 状态：In Progress（S1 已完成，S2 下一步）
- 阶段：1
- 主要仓库：`archguard-scanner`、`archguard-samples`、`archguard-docs`
- 前置：[阶段 0 退出关卡](../product/roadmap.md#阶段-0v010-foundation)
- 架构决策：[ADR-0001](../adr/0001-versioned-scanner-contract.md)、[ADR-0002](../adr/0002-deterministic-rule-execution.md)、[ADR-0003](../adr/0003-untrusted-repository-default-deny.md)、[ADR-0006](../adr/0006-java-first-phased-delivery.md)

## 用户结果

开发者可以在本地对 Java 项目执行：

```text
archguard scan ./my-java-project --rules rules/default.yaml --output report.json
```

命令在不依赖 Platform、数据库、网络、模型或目标项目构建的情况下，输出确定、版本化、机器可校验的架构结果。每个 Finding 都能追溯到 Rule、位置和 Evidence。

## 范围

### 必选能力

- 发现 Maven 标准布局下的 Java 主源码和模块边界。
- 提取 Artifact、Component 和 Dependency，并计算必要 Metric。
- 执行八类首批确定性规则。
- 产生稳定 ID、排序、Finding、Evidence、Metric 和 Diagnostic。
- 严格校验 YAML 规则配置和 JSON 输出 Schema。
- 在输入、文件、深度、时间和输出上使用有限上限。
- 通过至少三个合成 Java 项目和黄金结果验证重复性。

### 非目标

- 不提供 Platform API、数据库、用户、权限、任务历史或网页。
- 不克隆远程 Git，不执行 Maven/Gradle、插件、脚本、测试或目标代码。
- 不承诺完整类型求解、运行时 Spring 容器、反射、动态代理或完整调用图。
- 不使用 LLM 产生 Fact、Finding 或 severity。
- 不实现 Go、Python、JavaScript 解析器；只保证模型和 SPI 不阻止它们接入。
- 不建立远程动态插件市场；阶段 1 扫描器模块随受控制品发布。

## 模块边界

```text
archguard-scanner/
├── scanner-domain
├── scanner-parser-java
├── scanner-rule-engine
├── scanner-report
└── scanner-cli
```

| 模块 | 责任 | 禁止依赖 |
|---|---|---|
| `scanner-domain` | 语言无关模型、Rule/Analyzer 端口、结果不变量 | Java parser、Spring、数据库、Web、模型 SDK、Platform |
| `scanner-parser-java` | Java 文件发现、语法解析、语言特有结构到统一模型的映射 | Platform、数据库、CLI |
| `scanner-rule-engine` | 规则配置校验、依赖图、确定性规则、稳定排序 | Platform、网络、模型 SDK |
| `scanner-report` | JSON Schema 校验、规范序列化和报告写入 | Java AST、Platform DTO |
| `scanner-cli` | 参数、退出码、组合和用户错误输出 | 规则实现细节、Platform |

模块通过 Maven 聚合构建。具体 Java 解析库必须在 Technical Design 中比较能力、许可证、维护状态和替代方案后选择，本规范不提前冻结依赖。

## 语言无关统一模型

```text
Project
 └── Artifact
      └── Component
           ├── Dependency
           ├── Metric
           ├── Finding
           └── Evidence
```

公共对象不得包含 Java AST 节点、解析库类名、`Class<?>`、Spring Bean 实例或 Platform 数据库实体。语言特有信息只能进入带命名空间且经过 Schema 限制的属性，例如 `java.modifiers`；核心字段保持通用。

### 最小结果外形

```json
{
  "schemaVersion": "0.1.0",
  "project": "order-service",
  "language": "java",
  "artifacts": [],
  "components": [],
  "dependencies": [],
  "findings": [],
  "metrics": {},
  "diagnostics": []
}
```

最低字段语义：

| 对象 | 必需内容 |
|---|---|
| Artifact | 稳定 ID、kind、名称、相对根路径、语言 |
| Component | 稳定 ID、artifactId、kind、规范名称、可选位置 |
| Dependency | 稳定 ID、sourceId、targetId、kind、Evidence 引用 |
| Metric | scopeId、metric key、数值、阈值是否由 Rule 判定 |
| Rule | ID、版本、参数 Schema、默认与允许 severity |
| Finding | ID/fingerprint、Rule 引用、severity、subject、位置和 Evidence 引用 |
| Evidence | ID、kind、规范相对路径、1-based 位置、符号/关系摘要 |
| Diagnostic | code、level、scope、可安全定位的信息；不得伪装成 Finding |

输出路径使用 `/` 分隔的项目相对路径；集合稳定排序；ID 输入不包含时间、耗时或绝对路径。`schemaVersion` 是 Scanner 契约版本，不等于七仓库发布版本。

## 首批规则

| Rule ID | 目标 | 最小验证 |
|---|---|---|
| `archguard.illegal-package-dependency` | 包之间的非法依赖 | 允许边、禁止边、边界匹配 |
| `archguard.layered-architecture` | 分层架构方向违规 | 合规流向、反向依赖、跨层跳跃配置 |
| `archguard.dependency-cycle` | 包或模块循环依赖 | 两点循环、多点循环、自环、无环 |
| `spring.controller-repository-access` | Controller 直接访问 Repository | 直接依赖、经 Service 间接访问、同名非 Spring 类型 |
| `archguard.internal-module-access` | 跨模块调用内部类 | public API 允许、internal 禁止、模块边界缺失诊断 |
| `archguard.forbidden-component` | 禁止依赖指定组件 | 类型、包和 Maven 坐标匹配；未知对象不猜测 |
| `archguard.complexity-threshold` | 类、方法或模块复杂度告警 | 阈值边界、忽略生成代码、确定计数 |
| `archguard.required-annotation` | 缺少必要架构注解 | 适用范围、存在/缺失、无法解析诊断 |

每条 Rule 都必须有严格参数 Schema、默认 severity、允许覆盖范围、正例、反例、边界例和稳定 Evidence。复杂度算法、模块识别、内部可见性和“架构注解”的精确定义必须在实现前由 Technical Design 冻结。

## CLI 和退出码

| 情况 | 退出码类别 |
|---|---|
| 扫描完成且无阻断 Finding | `0` |
| 扫描完成但存在达到门槛的 Finding | 独立的规则违规退出码 |
| 参数、规则或输入无效 | 独立的用户输入退出码 |
| 解析/执行/资源/内部失败 | 独立的扫描失败退出码 |

具体整数值由 CLI Technical Design 冻结；规则违规与扫描失败绝不能共用同一语义。

## 合成样例

至少交付：

1. `java-clean-layered`：合规分层、构造器注入、无循环。
2. `java-architecture-violations`：非法包依赖、Controller→Repository、内部类跨模块、缺少注解和复杂度超限。
3. `java-dependency-cycle`：稳定的两点/多点循环。
4. 最小失败夹具：无法解析、未知 Rule、路径/资源超限。

样例必须是合成、可公开、固定版本的输入；每个样例 README 记录预期 Finding、Diagnostic、契约版本和验证命令。

## 测试与退出标准

- `scanner-domain` 架构测试证明与 Java parser、Spring、数据库、模型 SDK 和 Platform 解耦。
- 每条 Rule 有单元、参数 Schema、黄金和失败测试。
- 至少三份项目样例重复扫描三次，规范化 JSON 逐字节一致。
- 每个 Finding 的 Rule、位置、Evidence 引用闭合，没有悬空 ID。
- 未知字段、枚举、Rule、参数和无效引用失败关闭。
- 解析失败返回稳定 Diagnostic；日志和结果不含凭据、完整源码或主机绝对路径。
- `mvn verify`、CLI smoke test、Schema 校验、Secret/路径检查全部通过。
- README 明确支持范围、限制、构建、执行和退出码。

达到以上条件后才能发布 `v0.2.0-scanner`，并允许 Platform 进入阶段 2 的 Scanner 消费方设计。

## 实施切片

1. S1：聚合构建、五模块骨架和架构规则测试。
2. S2：`0.1.0` JSON Schema、统一模型、规范 ID/排序和有效/无效契约测试。
3. S3：Java 文件发现、语法解析、Component/Dependency/Evidence 提取。
4. S4：依赖图和前三条结构规则。
5. S5：Spring/模块/组件/复杂度/注解规则。
6. S6：CLI、YAML 校验、退出码和报告写入。
7. S7：Samples、黄金/失败/重复性测试、性能基线和发布文档。

每个切片单独评审和验证，不在 S1 一次创建全部占位实现。
