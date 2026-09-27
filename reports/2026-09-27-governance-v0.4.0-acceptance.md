# 持续治理 `v0.4.0-governance` 阶段验收报告

- 日期：2026-09-27
- 阶段：3 持续治理闭环，3A–3H
- 结论：Passed / Closed（本地合成 Compose 与已发布版本组合）
- 架构参考：[ADR-0008](../adr/0008-baseline-and-quality-gate-semantics.md)、[ADR-0009](../adr/0009-pr-revision-delta.md)
- 固定组合：[Deploy 兼容矩阵](https://github.com/AI-ArchGuard/archguard-deploy/blob/v0.4.0/compatibility/governance-v0.4.md)

## 验收对象与发布制品

| 对象 | 版本 / 提交 | 制品证据 |
|---|---|---|
| Platform | [`v0.4.0`](https://github.com/AI-ArchGuard/archguard-platform/releases/tag/v0.4.0) / `354392e58e2fac7dc79de3619e39aebb1e03bee7` | JAR SHA-256 `1ab6f01551c1aa79edb42c5365d041f621e9ea3a690f727c1ad4efb7f67c26ba`；[release run 36300665644](https://github.com/AI-ArchGuard/archguard-platform/actions/runs/36300665644) 成功 |
| Web | [`v0.2.0`](https://github.com/AI-ArchGuard/archguard-web/releases/tag/v0.2.0) / `a05cffb665d2ddc1d185991890c0183357572f8a` | 静态包 SHA-256 `e5e73509c003f1722912db6a105b9c2810b359bdc6be42c7304a48a8c5638773`；[release run 36300720294](https://github.com/AI-ArchGuard/archguard-web/actions/runs/36300720294) 成功 |
| Deploy | [`v0.4.0`](https://github.com/AI-ArchGuard/archguard-deploy/releases/tag/v0.4.0) / `390dc54ff8d23cc467e9acd769ccdf574ee4ed1e` | 兼容矩阵发布资产 SHA-256 `31c2ba309a053614264549071e55a38602dd83d8b251e765d9300ab7dfb89c04` |
| Scanner | [`v0.2.1`](https://github.com/AI-ArchGuard/archguard-scanner/releases/tag/v0.2.1) / `aad5ad6e135aa5ae86f3732f21552f9d2108e383` | 已发布 JAR SHA-256 `c2119c2e5ded8d5f1de18f64e0f3959864033b44af22e0ca6611c9761db1ed1f`；容器使用仅修改 Dockerfile/CI 的 `d4b8e98` 构建 |
| Samples | `4b63edb8909d9c12b93c2dc9ad07707cb009781a` | 固定合成 `governance/java-ci-journey`，无真实客户源码 |

Scanner Result/Rules Schema 均保持 `0.1.0`；Platform 使用 `platform-finding-v1` 逻辑指纹关联跨扫描 Finding，没有发布新 Scanner Schema。Platform 内部保持 Git Provider 无关，阶段 3 只启用 GitHub；不持有 Git 凭据、不远程 clone/fetch 源码。PR 修订差异只读，不参与基线门禁。

## 托管 CI 与发布证据

- 3A–3G 的完成记录见[阶段跟踪 Issue #24](https://github.com/AI-ArchGuard/archguard-platform/issues/24)；3H 的 ADR 扩展由[Docs PR #28](https://github.com/AI-ArchGuard/archguard-docs/pull/28) 合入，[Docs `main` run 36297988291](https://github.com/AI-ArchGuard/archguard-docs/actions/runs/36297988291) 成功。
- Platform [PR #32](https://github.com/AI-ArchGuard/archguard-platform/pull/32) 实现可信 PR head 历史与只读差异，[PR #33](https://github.com/AI-ArchGuard/archguard-platform/pull/33) 发布 `v0.4.0`；两次 PR CI 均成功，最终 [`main` run 36300508796](https://github.com/AI-ArchGuard/archguard-platform/actions/runs/36300508796) 成功。
- Web [PR #7](https://github.com/AI-ArchGuard/archguard-web/pull/7) 区分两个 Finding 参考点，[PR #8](https://github.com/AI-ArchGuard/archguard-web/pull/8) 发布 `v0.2.0`；两次 PR CI 均成功，最终 [`main` run 36300594867](https://github.com/AI-ArchGuard/archguard-web/actions/runs/36300594867) 成功。
- Deploy [PR #9](https://github.com/AI-ArchGuard/archguard-deploy/pull/9) 交付兼容矩阵、回归测试和 Compose 验收；PR 的 governance、compose、Windows startup 三项检查成功，最终 [`main` run 36301191654](https://github.com/AI-ArchGuard/archguard-deploy/actions/runs/36301191654) 成功。Deploy Release 由固定 `main` 标签手动创建，未声称有不存在的发布工作流。

上述 PR 合并时，仓库独立审批规则也约束管理员；依据项目所有者授权，仅短时解除该规则对管理员的适用以完成合并，随后逐仓库核对管理员保护已恢复开启。PR CI、合并后 `main` CI 与发布检查均未被跳过。此操作不能替代独立代码审查，后续普通变更应按仓库审批规则执行。

## 执行环境与结果

Windows / Docker Desktop 上使用专用 Compose 项目 `archguard-governance-3h`、本地随机凭据和固定合成 Samples。Platform `mvnw verify` 通过 66 项测试（含从初始迁移到 V7、V6→V7 升级、权限和 Webhook/CI 集成）；Web `check:api`、lint、6 项组件测试、类型检查/生产构建、Playwright 冒烟及依赖审计成功；Deploy 11 项 CI 适配器单元测试、Windows 本地重复启动测试、Compose 配置和验收脚本语法通过。

最终 Compose 从 Platform `v0.4.0` / Web `v0.2.0` 源码标签对应提交构建。Platform、Web、PostgreSQL 健康，Scanner Runner 稳定；只有 Web 绑定 `127.0.0.1:8080`，数据库、Keycloak、Platform 和 Runner 不向主机开放端口。保留的 PostgreSQL 数据卷从 Flyway V6 升级到 V7；未清空数据。实际 Scanner JAR 扫描固定 clean 与违规样例，CI 提交路径和签名 Webhook 由本地验收脚本调用：

| 步骤 | 实测 |
|---|---|
| 无基线的首次报告 | `ERROR/64`；成功扫描提升为不可变基线版本 1 |
| PR 新增非法依赖 | `NEW=1`，门禁 `FAIL`，退出 `2`；相同报告重放返回同一提交 |
| 有效、到期例外 | 有效时 `PASS/0`，到期后重新 `FAIL/2` |
| 修复后的 PR | 当前 head 与门禁指针更新，门禁 `PASS/0`；相对基线 `RESOLVED=0`，相对上一 PR 修订 `RESOLVED=1` |
| 事件与审计 | 错误签名拒绝；合成 Project 的基线提升 1、比较 2、门禁 5、Webhook 2、例外创建 1、报告接收/完成各 3 次成功审计 |

门禁的 `RESOLVED` 永远以基线为参考；修复一个只存在于先前 PR head 的违规，由 ADR-0009 独立差异显示。输入顺序、行号移动、RuleSetVersion 隔离、跨 Project 拒绝、重放/乱序/迟到事件、过期例外及历史不可变性由 Platform 集成测试覆盖；本地 Compose 复验覆盖上述最小用户闭环。验收脚本结束时删除了仅用于合成测试的 Keycloak 客户端。

## 发现、边界与回滚

首次 Compose 验收揭示：Scanner 制品卷挂载到 `/opt/archguard` 会遮蔽镜像内 `platform.jar`，使新镜像仍运行旧代码。Deploy PR #9 将其移到专用子目录，增加 Compose 布局断言；修复后实际容器应用和 V7 迁移均核对成功。重复启动还验证本地凭据不随已有数据卷轮换，Windows Runner 脚本保持 LF。

本次没有验证公网 GitHub 实际投递、GitHub Status 发布或生产 IdP，也没有远程 ArchGuard Registry 镜像与供应链签名；这些不能由本地合成测试推断为通过。Scanner JAR 在本地容器中重打包，字节摘要不能冒充已发布的 `v0.2.1` JAR，兼容矩阵分别标注。回滚先关闭 Web PR 差异入口，再停止 CI 提交/Webhook，最后回退 Platform 应用；Flyway V7 和已记录事实保留，不执行 down migration。直接回退旧 `v0.3.0` 应用对 V7 数据库的兼容性未演练，实施前必须另行验证。Agent、Gateway、Evals、第二 Git Provider、部分 AST 扫描、Kafka/Redis/Kubernetes 与自动修改 PR/源码/RuleSet 均未启动。
