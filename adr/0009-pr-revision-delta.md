# ADR-0009：PR 修订差异独立于基线门禁分类

- 状态：Accepted
- 日期：2026-09-27
- 决策者：ArchGuard 项目所有者
- 扩展：[ADR-0008](0008-baseline-and-quality-gate-semantics.md)，不替代其基线与门禁定义

## 背景

3H 真实 Compose 验收发现：干净默认分支基线 `B=∅`，PR 首次提交含一个新增违规 `C₁={f}`，修复后 `C₂=∅`。按 ADR-0008，门禁始终比较 `B` 与候选，因此修复时 `RESOLVED=B−C₂=∅`，虽然门禁正确地从 `FAIL/2` 变为 `PASS/0`。阶段最小用户闭环还要求解释“这次 PR 修复了上个修订的违规”。把 `C₁−C₂` 填入基线 `RESOLVED` 会改写其参考点与历史语义，不能接受。

## 决策

增加独立、只读的 **PR 修订差异**。它以相同 Project、Repository、PR、目标分支、RuleSetVersion 和指纹算法版本下，前一个已验签且已应用的不同 head 修订的完整候选 Finding 集合 `P` 为参考，以当前已验签 head 的完整候选集合 `C` 为目标：`NEW=C−P`、`EXISTING=C∩P`、`RESOLVED=P−C`。沿用 `platform-finding-v1` 的逻辑指纹和固定排序；不改变 Scanner Schema 或原始报告。

基线分类仍严格使用 ADR-0008 的 `B` 与 `C`，其计数、GateEvaluation、CI 退出码、例外和历史保持不变。PR 修订差异只帮助用户理解 PR 内变化，**不参与质量门禁求值**。Web 必须明确标注两个参考点，不能把 PR `RESOLVED` 计数显示为基线门禁的 `resolvedCount`。

## 可信修订与缺失状态

- 只记录 HMAC 验签、时间窗口和乱序检查后实际 `APPLIED` 的 GitHub PR head 事件；delivery ID 幂等。同一 head 的重复事件不构成新的“前一个不同修订”。旧事件、迟到报告、错误签名或碰撞均不能改变当前 head 或其前驱。
- PR head 历史追加到 PostgreSQL，不回填既有 webhook 的未经保存正文。当前 head 与前一个不同 head 依签名事件时间严格排序；当前门禁必须确实指向当前 head。
- 两个修订都须有完成的报告、成功生成的比较、相同 RuleSetVersion 与指纹算法版本。若首次修订、任一报告未完成、范围或算法不兼容，接口返回显式不可用状态与原因，不能猜测前驱或把未知当作空集合。
- 查询先验证 Viewer 的 Project/Repository 边界，并在一致的数据库快照中读取当前 head、前驱、门禁与不可变 Finding 快照。跨 Project 保持隐藏式 404。
- 返回当前和前驱 head SHA、确切 GateEvaluation ID、参考类型 `PR_PREVIOUS_REVISION`、算法版本、三类计数和确定排序的 Finding。历史扫描、基线选择、门禁和审计事实不被重写。

## 备选方案

- 把 PR 修复计入基线 `RESOLVED`：改变 ADR-0008 集合定义并污染门禁历史，拒绝。
- 根据报告到达顺序选“上一修订”：网络重试和迟到提交会误选前驱，拒绝。
- 从 GitHub 再次 clone/fetch 或保存凭据求 ancestry：扩大 Platform 信任面，拒绝。
- 仅在 Web 推断两次查询结果：无法保证验签事件顺序、版本和一致快照，拒绝。

## 影响与验证

Platform 增加向后兼容的只读 API、追加式 head 历史迁移和集成测试；Web 消费固定 API 快照并分别展示基线与 PR 差异；Deploy 用干净→新增→修复的真实 Scanner/Compose 闭环验证 `FAIL/2`、`PASS/0` 与 PR `RESOLVED=1`。旧客户端不调用新 API，原有门禁行为不变。部署顺序为迁移与 Platform → Web → Deploy 验收 → Docs 阶段报告。回滚先关闭 Web 新区块，再回退 Platform 应用；迁移和已记录的签名事件保留，不执行 down migration。历史 PR 在新迁移前没有可信 head 序列时明确显示不可用。

若需要让 PR 修订差异参与门禁，或支持第二个 Git Provider，必须另立版本化策略与决策，不能隐式扩大本 ADR。
