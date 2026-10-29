# 个人 Project Agent 日常使用契约计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 把所有者已批准的“普通 Finding 解释与所选 Finding PR 摘要直接可用”落实为独立的日常授权、来源快照、请求和费用语义；不授予任何真实调用或费用。

**Architecture:** Platform 仍为模块化单体，复用既有资源授权、最小投影、模型端口、严格输出/引用校验、事务额度和审计。日常请求使用新的版本化生产者契约，合成验收及历史失败批次保持原语义，不通过删守卫或改旧迁移实现。

**Tech Stack:** 规范 Markdown；生产者后续沿用 Java 21、Spring、PostgreSQL、固定 OpenAPI 与原假 HTTP 回归，无新增依赖。

**Spec:** [已批准的完整设计](../specs/2026-10-28-stage4-agent-workbench-design.md)。实现与本计划均不构成外发/费用授权。

## Global Constraints

- 个人所有者、本地部署、获授权的 Project；不接入客户源码、敏感/保密材料或公开服务。
- 固定现有 Responses 协议；不增加模型工具、自动重试、源码投影或第三方服务。
- 完整请求最多6000 UTF-8字节、输出最多1500 Token；输入8000为调用后阈值。单请求本地上限USD0.35，Project/部署UTC日技术上限USD5/20保留；这些上限不是实际花费授权。
- 新费用授权默认缺失，调用次数及预算默认零；仅保存Key、打开页面或批准设计不产生外发。
- 新增契约/迁移，保留合成专用API、旧批次、UNKNOWN预留、凭据密文、引用和审计，不修改Scanner Schema或确定性门禁。
- Docs→Platform→Web→Deploy；源码改动、真实部署和真实验收分别以自身证据证明，不能用本计划或旧CI替代。

## Review Focus

- 日常路径不能依赖手填合成模板或自动把旧批次升级为日常授权。
- 改凭据/Project权限/模型价格/材料版本后，不得沿用失效绑定发送或泄漏旧引用。
- 并发、刷新、丢响应和重启不得创建第二次提供方尝试或释放UNKNOWN预留。
- 本地最小投影不等于材料非敏感证明；所有者须明确承担选材权利和残余风险，系统不伪造批准。
- 无预算、开关关闭、授权失效或请求过大必须零外发；已发生可信费用必须与输出成功独立结算。

### Task 1: Docs 冻结日常语义

**Files:** 新增 `adr/0016-personal-project-agent-use.md`；增量更新 `requirements/agent-v0.5-feature-spec.md`、ADR/Requirements/Contracts索引、`product/roadmap.md`、`development/phase-gates.md`、根README和Docs CI入口。

**Interfaces:** Docs只定义语义和验收，不复制生产者DTO/JSON Schema；Platform拥有随后独立日常API兼容线。

- [x] 对照已批准设计与当前代码，确认可复用边界和旧合成专用路径，记录具体生产者落点。
- [x] 编写ADR与Feature Spec增量：有界可撤销授权、显式资源选择、服务端不可变最小快照、单次尝试/幂等、费用及恢复；默认关闭且不设已批准金额。
- [x] 同步索引和当前状态；既有Accepted ADR正文保留历史，当前入口不把历史条件授权描述为可再次使用。
- [x] 独立技术评审；运行链接/文档检查器测试、YAML和Secret检查及diff检查，保存本地提交。

### Task 2: 生产者实现计划（本切片不伪称已实现）

**Files:** 下一切片由Platform `docs/technical-design/` 与 `openapi/`、`agent/`、新增迁移及测试承担。

- [ ] 按Task1最终语义拟定可执行小切片，复用既有授权/投影/dispatch/validator/账本；先写假HTTP与并发/恢复RED测试，再实现默认关闭路径。
- [ ] 仅在契约及代码自身检查完成后交Web消费，再固定Deploy候选；实际新调用、数据及费用仍须单独具体授权。

## 发布与回滚

先合入Docs规范及其main CI，再合入提供者、Web消费者和Deploy固定兼容组合。日常授权与合成验收分开管理；回滚先关日常入口/Project/后端出口，再退应用，保留追加迁移、快照、请求、可信费用/UNKNOWN及审计。阶段四、#43和4H在所有最终证据齐全前保持开放。

## 本地验证记录（2026-10-29）

Task1独立技术评审的规格、可实施性及质量均通过，无可操作问题。现有脚本检查60份Markdown，断链/退役引用/结尾错误均为0；检查器8项测试通过。工作流YAML解析与ADR入口、Linux换行规范下的既有LICENSE摘要、变更文件凭据模式扫描及diff检查通过。Python运行时未安装PyYAML，改用主检出已有js-yaml只读解析；未新增依赖。Git直连读取远端遭连接重置，不能声称PR/main CI已完成；后续使用现有GitHub连接继续核对。全部为Docs离线检查，未部署或调用模型。
