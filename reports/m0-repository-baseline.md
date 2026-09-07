# M0 仓库基线验收报告

- 检查日期：2026-09-07
- 工作区：`C:\Users\Lenovo\Desktop\archguard-workspace`
- Issue：未提供；本次不执行远程 Issue 写操作
- 目标版本：M0；未提供语义化版本，不擅自设定
- 范围：七个 ArchGuard 独立仓库的治理、模板、最小 CI 和本地验收证据

## 验收结论

七个仓库均有独立 `.git`、与仓库名称一致的 GitHub `origin` 和本地 `main` 初始化分支。外层工作区没有 `.git`。本地没有提交或远程跟踪 ref；远程实时 HEAD 查询受网络环境阻断，因而远程默认分支状态未核验。必须在各仓库初始提交和首轮 CI 完成后复核远程默认分支，再配置分支保护与必需状态检查。

本阶段只建立治理基线，没有实现业务代码、创建许可证、提交、推送或修改远程设置。

## 仓库身份与状态

| 仓库 | 绝对路径 | origin | 本地分支 | 独立 Git | 当前状态 |
|---|---|---|---|---|---|
| archguard-docs | `C:\Users\Lenovo\Desktop\archguard-workspace\archguard-docs` | `https://github.com/AI-ArchGuard/archguard-docs.git` | `main` | 是 | 无提交；基线文件未跟踪 |
| archguard-platform | `C:\Users\Lenovo\Desktop\archguard-workspace\archguard-platform` | `https://github.com/AI-ArchGuard/archguard-platform.git` | `main` | 是 | 无提交；基线文件未跟踪 |
| archguard-scanner | `C:\Users\Lenovo\Desktop\archguard-workspace\archguard-scanner` | `https://github.com/AI-ArchGuard/archguard-scanner.git` | `main` | 是 | 无提交；基线文件未跟踪 |
| archguard-mcp-gateway | `C:\Users\Lenovo\Desktop\archguard-workspace\archguard-mcp-gateway` | `https://github.com/AI-ArchGuard/archguard-mcp-gateway.git` | `main` | 是 | 无提交；基线文件未跟踪；名称无末尾连字符 |
| archguard-deploy | `C:\Users\Lenovo\Desktop\archguard-workspace\archguard-deploy` | `https://github.com/AI-ArchGuard/archguard-deploy.git` | `main` | 是 | 无提交；基线文件未跟踪 |
| archguard-samples | `C:\Users\Lenovo\Desktop\archguard-workspace\archguard-samples` | `https://github.com/AI-ArchGuard/archguard-samples.git` | `main` | 是 | 无提交；基线文件未跟踪 |
| archguard-evals | `C:\Users\Lenovo\Desktop\archguard-workspace\archguard-evals` | `https://github.com/AI-ArchGuard/archguard-evals.git` | `main` | 是 | 无提交；基线文件未跟踪 |

远程只读检查：本地 Git 元数据可确认上述 `origin`，但 `git ls-remote --symref origin HEAD` 因当前环境无法连接 GitHub 而未完成；GitHub CLI 也未安装，且没有提供已认证的 GitHub 管理接口。远程默认分支、Issue、PR、分支保护和项目看板的实际配置状态记为“待核验”，不做推断。

## 职责与依赖方向

| 仓库 | 核心职责 | 明确非职责 | 允许的主要依赖方向 |
|---|---|---|---|
| docs | 产品、需求、架构、ADR、工程规范、运行手册、报告 | 不承载业务实现 | 其他仓库引用 docs 规范 |
| platform | 模块化单体业务平台与扫描编排 | 不实现源码分析或 MCP 路由 | Platform → Scanner 版本化契约；Platform → PostgreSQL |
| scanner | 确定性源码/字节码/依赖图分析 | 不管理业务状态与权限，不依赖 Platform 内部类 | Scanner → Samples 测试夹具；对外发布版本化契约 |
| mcp-gateway | MCP 工具发现、授权、路由、限流、审计 | 不直连业务数据库，不执行任意 Shell | Gateway → Platform/Scanner 公开 API 或版本化契约 |
| deploy | 部署、兼容矩阵、可观测配置、回滚 | 不实现业务逻辑，不保存 Secret | Deploy → 已发布 Platform/Scanner/Gateway 制品 |
| samples | 合成正常/违规/失败样例 | 不含生产实现或真实客户代码 | Scanner/Platform 测试 → 固定版本 Samples |
| evals | 版本化评估集、评分、回归与安全门禁 | 不作为生产推理服务，不绑定单一模型商 | Evals → 公开契约和合成样例 |

核对结果：README 中的职责、非职责和依赖方向一致；Platform 保持模块化单体，Scanner 契约独立，Gateway 默认只读且不直连数据库。

## 治理文件矩阵

| 项目 | docs | platform | scanner | mcp-gateway | deploy | samples | evals |
|---|---:|---:|---:|---:|---:|---:|---:|
| README / AGENTS | 完整 | 完整 | 完整 | 完整 | 完整 | 完整 | 完整 |
| CONTRIBUTING / SECURITY / CHANGELOG | 完整 | 完整 | 完整 | 完整 | 完整 | 完整 | 完整 |
| .editorconfig / .gitignore | 完整 | 完整 | 完整 | 完整 | 完整 | 完整 | 完整 |
| PR 模板 | 完整 | 完整 | 完整 | 完整 | 完整 | 完整 | 完整 |
| Feature / Bug Issue Form | 完整 | 完整 | 完整 | 完整 | 完整 | 完整 | 完整 |
| 最小基线 CI | 完整 | 完整 | 完整 | 完整 | 完整 | 完整 | 完整 |
| LICENSE | 待决策 | 待决策 | 待决策 | 待决策 | 待决策 | 待决策 | 待决策 |

整改前只有 docs 仓库缺少仓库级 AGENTS、通用治理文件、编辑器/忽略规则和 PR/Issue 模板；本次以新增文件补齐。其他六仓库的现有未跟踪基线文件予以保留，没有覆盖。

## 规范与模板入口

- 规范：项目治理、开发流程、工程规范、质量门禁、安全与可观测、发布与运行。
- 模板：Feature Spec、Technical Design、ADR、Pull Request、Postmortem。
- 目录：product、requirements、architecture、adr、runbooks、reports。
- `archguard-docs/README.md` 已提供上述规范、模板和目录导航。

## 许可证方案与建议

| 方案 | 专利条款 | 作品集展示和复用 | 第三方依赖影响 | 主要取舍 |
|---|---|---|---|---|
| Apache-2.0 | 明确授予贡献者专利许可，并含专利诉讼终止条款 | 允许公开展示、修改、分发和商业使用，需保留许可证与 NOTICE 要求 | 仍须逐项核对依赖许可证；分发时维护归属和 NOTICE | 法律文本更长，但对潜在企业协作和专利风险更明确 |
| MIT | 无明确专利授权条款 | 允许公开展示、修改、分发和商业使用，保留版权与许可声明即可 | 仍须逐项核对依赖许可证和归属要求 | 简洁宽松，但专利授权确定性低于 Apache-2.0 |
| 暂不授权 | 没有对外专利许可 | 公开仓库默认不等于允许复制、修改或分发，会降低作品集复用和外部贡献可行性 | 不消除第三方依赖义务 | 保留全部权利，但协作和使用边界不清晰 |

建议优先选择 Apache-2.0：它兼顾公开作品集、企业友好复用和明确专利条款。若所有者更看重最简文本且接受专利条款不足，可选择 MIT。许可证属于所有者决策；本阶段不创建 `LICENSE`，决定后应在七仓库一致落地，并核对依赖清单及 NOTICE 义务。

## 默认分支保护建议

在每个仓库完成初始提交并至少产生一次 CI 状态后执行：

1. 将 `main` 设为默认分支，所有变更通过 PR；至少 1 个批准。
2. 要求分支在合并前保持最新，所有对话已解决。
3. 将实际出现的 `Repository Baseline / governance`（docs 为 `Documentation Baseline / documentation`）设为必需状态检查；不得提前填写不存在的 context。
4. 禁止强推和分支删除；管理员也遵守规则，紧急绕过必须审计。
5. 限制直接推送，默认 Squash Merge，自动删除已合并功能分支。
6. 后续加入构建、测试、依赖/Secret 扫描时，先观察稳定状态，再逐项升级为必需检查。

## 跨仓库项目看板与 M0–M9

建议建立一个组织级项目看板，字段包括：Status、Repository、Milestone、Priority、Type、Owner、Target version、Blocked by、Risk。推荐状态为 Backlog、Ready、In progress、In review、Ready to release、Done。

| 里程碑 | 目标 | 主要仓库 |
|---|---|---|
| M0 | 七仓库基线、治理、模板、最小 CI | 全部 |
| M1 | 产品范围、总体架构、边界与 ADR | docs |
| M2 | Java Platform 模块化单体骨架 | platform、docs |
| M3 | 仓库登记与扫描任务状态机 | platform |
| M4 | Scanner MVP 与版本化契约 | scanner、samples、docs |
| M5 | 真实扫描集成、重试与清理 | platform、scanner、samples |
| M6 | GitHub PR 安全集成 | platform、deploy |
| M7 | 消息与可靠性演进 | platform、deploy、docs |
| M8 | Go MCP Gateway 只读工具与治理 | mcp-gateway、platform、evals |
| M9 | Evals 基线与安全门禁 | evals、samples、docs |

阶段 10–13 保留在后续路线图，不混入 M0–M9 初始化看板配置。

## 各仓库独立变更集合

- docs：README 和六类规范入口；product/requirements/architecture/adr/runbooks/reports；五类模板；AGENTS、CONTRIBUTING、SECURITY、CHANGELOG、编辑器/忽略规则、PR/Issue 模板、文档基线 CI、本报告。
- platform：README、AGENTS、CONTRIBUTING、SECURITY、CHANGELOG、编辑器/Java 忽略规则、PR/Issue 模板、仓库基线 CI。
- scanner：README、AGENTS、CONTRIBUTING、SECURITY、CHANGELOG、编辑器/Java 忽略规则、PR/Issue 模板、仓库基线 CI。
- mcp-gateway：README、AGENTS、CONTRIBUTING、SECURITY、CHANGELOG、编辑器/Go 忽略规则、PR/Issue 模板、仓库基线 CI。
- deploy：README、AGENTS、CONTRIBUTING、SECURITY、CHANGELOG、编辑器/部署制品与 Secret 忽略规则、PR/Issue 模板、仓库基线 CI。
- samples：README、AGENTS、CONTRIBUTING、SECURITY、CHANGELOG、编辑器/Java 与 Go 忽略规则、PR/Issue 模板、仓库基线 CI。
- evals：README、AGENTS、CONTRIBUTING、SECURITY、CHANGELOG、编辑器/评估产物忽略规则、PR/Issue 模板、仓库基线 CI。

这些集合不依赖同一提交，可逐仓库审查和回滚。推荐兼容顺序：docs → samples → scanner → platform → mcp-gateway → evals → deploy；M0 没有运行时契约或数据库变化，因此顺序只影响规范可引用性，不影响运行兼容。

## 回滚方案

本阶段没有提交和远程写操作。若需回滚，按仓库逐一移除本次基线文件或在形成初始提交后 revert 对应仓库提交；不要删除独立 `.git`。docs 中的规范应最后回滚，以便其余仓库在回滚过程中仍可引用治理要求。

## 远程治理待办

1. 所有者决定 Apache-2.0、MIT 或暂不授权，并一致处理七仓库许可证。
2. 分别审查并提交七个仓库的初始基线，确认远程 `main` 和首轮 CI。
3. 使用有权限的 GitHub 身份核验 Issue、PR、Security Advisories、Actions 权限和项目看板状态。
4. 按实际 CI context 配置分支保护，禁止强推和删除。
5. 创建组织级项目看板及 M0–M9 里程碑，把跨仓库 Issue 关联到同一视图。
6. CI 稳定后再加入 Secret、依赖和供应链扫描；新增工具需记录依赖、许可证和维护成本。

## 验证记录

本地验收应覆盖：外层无 `.git`、七个 origin/本地分支/独立 `.git`、必需文件、Markdown 相对链接、YAML 解析、空白错误、常见 Secret 模式、README 边界一致性。由于七仓库尚无提交，GitHub Actions 不能在本地声称已运行；业务构建和测试也尚不存在。
