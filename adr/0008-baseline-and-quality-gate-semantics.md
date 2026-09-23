# ADR-0008：冻结不可变基线、Finding 分类和质量门禁语义

- 状态：Accepted
- 日期：2026-09-22
- 决策者：ArchGuard 项目所有者
- 扩展：[ADR-0001](0001-versioned-scanner-contract.md)、[ADR-0004](0004-platform-modular-monolith.md)、[ADR-0005](0005-postgresql-business-source-of-truth.md)、[ADR-0006](0006-java-first-phased-delivery.md)

## 背景

阶段 2 保存每次扫描的 Result、Finding、Evidence 和单次扫描处置，但没有跨扫描身份、基线、差异分类或 CI 门禁。直接以 Scanner Finding ID 或源码行号关联，会在报告重排、行号漂移或重扫时制造假新增问题；修改历史 Finding 来表达例外，又会破坏审计和重现。

阶段 3 还需要接入 GitHub PR 与 CI，但 Platform 的安全边界不允许持有 Git 凭据或远程克隆源码。必须先冻结与 Git Provider 无关的领域语义，再把 GitHub 作为首个外部 Adapter 实现。

## 决策驱动因素

- 相同报告集合必须得到与数组顺序无关的相同分类和门禁。
- 仅移动代码行不能把同一逻辑违规误判为新问题。
- 基线、策略、例外和门禁必须可重放、可审计且不能改写历史。
- RuleSetVersion 的变化不能静默继承语义不兼容的基线。
- Scanner 保持独立、稳定和版本化；Platform 只消费公开报告契约。
- GitHub 集成失败或迟到不能覆盖 Platform 已持久化的权威治理事实。

## 选择

### Git 与执行边界

- 领域模型使用 Provider 无关的 Repository、GitRevision、PullRequestRef、ReportSubmission 和 GateEvaluation；阶段 3 只实现 GitHub Adapter。
- CI 在自己的检出工作区运行固定 Scanner，把原始报告及最小 Git 元数据提交给 Platform。
- Platform 不接收 Git 凭据，不执行远程 clone/fetch，不接收源码归档，也不根据 Webhook 下载源码。
- “增量扫描”在阶段 3 仅表示两个完整扫描结果之间的 Finding 差异；Scanner 仍执行完整确定性扫描。

### 不可变基线

- 基线比较空间由 `Project + Repository + 目标分支 + RuleSetVersion` 唯一确定。不同空间不得共享活动基线。
- BaselineVersion 绑定一个已成功、归属校验通过的 ScanResult，并记录 commit SHA、报告摘要、创建者、创建时间和版本号。
- BaselineVersion 创建后不可修改或删除。提升另一个扫描创建新版本；重新选择既有版本只改变版本化的活动指针，并追加审计。
- 活动指针不是历史内容的一部分。历史 GateEvaluation 永远引用求值时的确切 BaselineVersion，不随活动指针变化。

### 稳定逻辑指纹

- Platform 为每个 Finding 计算版本化逻辑指纹，用于集合关联；不把 Scanner Finding ID 直接当作跨扫描身份。
- 指纹输入由 3B 的公开消费方契约固定，至少包含 Rule 身份、规范化受影响实体身份、违规类型和规则所需的稳定区分字段。
- 指纹明确排除行号、列号、数组顺序、展示消息、时间戳和随机/运行期 ID。路径只有在它是规范化逻辑实体身份的一部分时才能参与。
- 环、无序集合或多实体关系必须先使用契约规定的规范形式再哈希，不能依赖遍历顺序。
- 指纹记录算法版本。检测到同一指纹对应不同规范载荷时必须失败为 `ERROR`，不得静默合并。
- 默认沿用 Scanner Result Schema `0.1.0`。只有 3B 通过固定报告证明现有字段不足，才能另提兼容性决策；本 ADR 不授权修改 Scanner Schema。

### 三类差异

设基线指纹集合为 `B`，候选指纹集合为 `C`：

- `NEW = C - B`
- `EXISTING = C ∩ B`
- `RESOLVED = B - C`

分类以集合语义计算并保存确定排序后的结果。输入顺序、展示排序和行号漂移不影响集合成员。RuleSetVersion 不同意味着比较空间不同，Platform 不自动跨版本迁移基线。

### 独立例外

- 跨扫描例外是独立 `PolicyException`，不修改 ScanResult、Finding、BaselineVersion 或既有 GateEvaluation。
- 例外至少记录 Project、Repository、目标分支、规则或指纹范围、原因、创建者、生效时间、到期时间、版本和撤销信息。
- GateEvaluation 使用明确的求值时间判断例外是否有效，并记录命中的例外版本；到期后新求值重新阻断，历史求值不变化。
- 例外默认使用最小范围；跨 Project 或隐式全局例外不允许。

### 质量门禁

- 结果枚举固定为 `PASS`、`FAIL`、`ERROR`。
- 默认策略只检查 `NEW` 中未被有效例外覆盖的 `high` 和 `critical` Finding：集合为空为 `PASS`，否则为 `FAIL`。
- `EXISTING` 默认不阻断，`RESOLVED` 只作为改善事实；策略后续扩展必须版本化，不能改变历史结果。
- 无兼容基线、报告或元数据非法、指纹冲突、求值异常和契约不兼容不得产生 `PASS`；根据调用语义返回显式待建立基线状态、配置错误或 `ERROR`。
- CI 入口把 `PASS` 映射为 `0`、`FAIL` 映射为 `2`、配置错误映射为 `64`、执行或契约错误映射为 `70`。

### 事件、顺序和审计

- 报告提交由 Project 内幂等键和请求摘要约束；相同请求返回原结果，不同请求复用幂等键返回冲突。
- GitHub Webhook 验证签名、允许事件、时间窗口和 delivery ID；重放保持幂等，错误签名失败关闭。
- 每个 PR/目标分支保存已知最新 commit 的顺序事实。旧 commit 的迟到报告或事件可以保留审计，但不得覆盖当前 commit 的 GateEvaluation 或外部状态。
- 报告提交、基线提升、活动版本切换、例外创建/撤销/到期、门禁求值和外部状态发布全部审计；审计不记录凭据、完整源码或 Webhook secret。

## 备选方案

- 使用 Scanner Finding ID 跨扫描关联：实现简单，但该 ID 不是已冻结的长期语义身份，拒绝。
- 使用文件和行号作为指纹：行号漂移会制造假新增和假解决，拒绝。
- 让 Scanner 保存基线并计算差异：会把 Project、分支、权限、例外和审计责任泄漏到分析平面，拒绝。
- 由 Platform clone Git 仓库：要求保存 Git 凭据并扩大源码与网络攻击面，拒绝。
- 修改历史 Finding 表达例外：破坏不可变事实和重放，拒绝。
- 跨 RuleSetVersion 自动复用基线：无法证明规则语义兼容，拒绝。

## 正面影响

- 分类和门禁可以由完整输入重放，且不受报告顺序或行号变化影响。
- 基线、例外和历史结果边界清晰，满足审计和恢复要求。
- GitHub 是可替换 Adapter，未来 Provider 不需要改变领域模型。
- Scanner 继续保持独立；Platform 可以先用现有 `0.1.0` 报告验证消费方指纹。

## 负面影响与风险

- 3B 必须为不同 Finding 类型定义规范载荷，指纹算法和迁移需要长期版本管理。
- Platform 不 clone Git，不能自行证明 commit ancestry；必须明确信任经过认证的 Webhook 与 CI 元数据，并对乱序失败关闭。
- 默认只阻断新增高风险问题意味着存量债务不会立刻使 CI 失败，需要通过趋势和后续策略治理。
- 不可变历史增加存储与查询成本，清理策略只能归档非权威附件，不能删除审计事实。

## 验证方式

- 相同报告重复提交不重复创建任务、Finding 或门禁。
- 随机打乱基线和候选数组，三类集合与门禁保持逐字节一致的规范结果。
- 仅改变行号，逻辑指纹保持相同；改变 Rule、实体或稳定区分字段，指纹改变。
- RuleSetVersion 变化不会找到旧空间的活动基线。
- 基线版本内容无法更新或删除，活动版本切换保留历史引用和审计。
- 有效例外使匹配问题通过，到期后新求值重新失败，历史求值不变。
- Webhook 错误签名、重放、乱序和迟到事件不会覆盖较新 commit 状态。
- 跨 Project 的读取、提交、基线提升和例外创建全部拒绝且不泄漏资源存在性。

## 何时重新评估

- 固定报告证明 Result Schema `0.1.0` 无法表达某类 Finding 的稳定逻辑身份。
- 真实 Git Provider 要求出现且 Provider 无关模型无法承载。
- 证据表明完整扫描或 PostgreSQL 集合比较无法满足明确的容量目标。
- 组织需要阻断存量问题或跨 RuleSetVersion 迁移基线；届时必须新增版本化策略或 ADR，不改写本决策和历史结果。
