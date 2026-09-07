# 阶段 6：GitHub PR 集成

## 阶段目标

以 GitHub App 最小权限接收 PR 事件，安全触发增量扫描并发布只读 Check 或有限评论，形成完整审计链。

## 输入与范围

- 必需：Feature Spec、Technical Design、威胁分析和必要 ADR。
- 允许修改：Platform、必要的契约/部署配置、模拟测试和文档。
- 非目标：自动修改代码、自动合并、执行任意仓库脚本、长期 PAT 和写入非必要资源。
- 真实 GitHub App 创建、权限变更和远程写操作必须有明确授权。

## 开始前检查

1. 验证阶段 5 的异步扫描和幂等处理。
2. 列出 GitHub App 权限矩阵，逐项说明为何需要。
3. 定义 Webhook 事件、delivery ID、installation、repository 和 PR 的映射。
4. 完成威胁建模：伪造签名、重放、跨租户访问、恶意 Diff、Token 泄漏、限流和提示注入。
5. 明确 Check 与评论的最大数量、更新策略和失败降级方式。

## 执行流程

### 6A：安全设计

1. 只申请 Contents/Metadata/Pull Requests/Checks 所需的最小只读或精确写权限。
2. 使用安装级短期 Token，不保存用户 PAT。
3. 定义 Webhook Secret 的注入、轮换和审计方式。
4. 明确时间窗口、原始请求体签名验证和失败响应。
5. 将 GitHub 仓库映射到已授权的组织、项目和资源归属。

### 6B：Webhook 接入

1. 在解析业务 Payload 前验证签名、事件类型、时间窗口和大小限制。
2. 使用 delivery ID 做持久化幂等，重复事件返回稳定结果。
3. 只处理明确白名单中的 PR opened、synchronize、reopened 等事件。
4. 将接收与扫描解耦，快速返回并创建异步任务。
5. 保存最小审计摘要，不记录 Token、完整 Diff 或源码。
6. 对无权限、安装删除、仓库更名和过期 Token 返回可诊断错误。

### 6C：增量扫描和 PR 反馈

1. 安全获取 PR 元数据和允许范围内的 Diff。
2. 限制文件数、Diff 大小、下载时间和重试次数。
3. 将变更范围传入 Scanner，同时保留全量扫描降级策略。
4. Check 输出包含确定性结论、证据位置和运行链接。
5. 评论只输出高置信、去重且数量受限的建议。
6. 重跑时更新已有 Check/评论，不重复刷屏。
7. AI 解释尚未启用时不得伪造 AI 结果。

## 交付物

- 权限矩阵、威胁分析和 Technical Design。
- Webhook 验证、防重放和事件幂等实现。
- 安装 Token Adapter、PR Diff Adapter、Check/评论 Adapter。
- 模拟/录制响应测试、审计事件、指标和运行手册。

## 验证

1. 正确签名、错误签名、过期时间、超大 Payload 和未知事件测试。
2. 同一 delivery 重放和并发投递测试。
3. 无权限、安装删除、Token 过期、GitHub 限流和超时测试。
4. PR 更新触发增量扫描，重复运行不重复评论。
5. 使用模拟或录制响应，不在测试中依赖真实 Token。
6. 扫描日志、测试夹具和提交内容中的 Secret。

## 兼容与回滚

先发布能够忽略新事件的 Platform，再启用 GitHub App 订阅和 Check 写入。回滚时先暂停 Webhook/写权限，再回退应用；保留 delivery 审计和未处理任务的处置记录。

## 停止条件

需要扩大 GitHub 权限、处理私有源码方式未确认、签名验证无法使用原始请求体或准备执行任何自动写代码行为时停止。

## 退出条件

合法 PR 事件只处理一次，未授权请求全部阻断，短期 Token 不落盘，Check/评论可去重且审计链完整。
