# ADR-0007：阶段 2 使用独立 Web 客户端仓库

- 状态：Accepted
- 日期：2026-09-19
- 决策者：ArchGuard 项目所有者
- 扩展：[ADR-0006](0006-java-first-phased-delivery.md)

## 背景

阶段 2 需要通过浏览器演示 Project、Repository、RuleSet、ScanJob、Finding 和处置闭环。现有七仓库没有用户界面所有者，把浏览器代码放入 Platform 会把 Node 构建、OIDC 浏览器状态和 UI 发布节奏混入 Java 控制面。

项目所有者已创建 `AI-ArchGuard/archguard-web`，并明确选择独立 React 前端。该选择要求把仓库、运行容器、契约消费者和发布顺序纳入现有治理，而不能把 Web 当作 Platform 内部静态资源。

## 决策

- 增加第八个仓库 `archguard-web`，使用 React、Vite 和 TypeScript。
- Web 是 Platform REST/OpenAPI 的外部消费者，不访问 PostgreSQL、Scanner、Runner 或 Platform 内部类。
- Web 使用 OIDC Authorization Code + PKCE；访问令牌不进入 `localStorage`、日志或构建制品。
- Web 构建为独立静态容器，在本地 Compose 中作为唯一公开入口，并反向代理 `/api` 和 `/auth`。
- Platform 继续作为 Java/Spring Boot 模块化单体，独立 Web 不构成 Platform 微服务拆分。
- Platform 拥有 OpenAPI；Web 通过固定版本的 OpenAPI 生成类型化客户端并运行消费方测试。
- Web 独立发布，首个版本为 `v0.1.0`；Deploy 记录与 Platform、Scanner 的兼容组合。

## 备选方案

- Platform 内嵌服务端页面：部署简单，但把 UI 技术栈和会话边界绑定到控制面，拒绝。
- Platform 仓库内独立前端子项目：保持七仓库，但仍共享发布和代码所有权，项目所有者未选择。
- 手工调用 REST 或只提供 OpenAPI：不足以满足浏览器独立演示结果，拒绝。

## 影响

- 仓库范围从七个扩展为八个；Stage 0 的七仓库历史事实保持不变。
- 新仓库必须先完成许可证、协作、CI、依赖、Secret 和分支保护基线。
- Web 和 Platform 可以独立发布，但必须承担 OpenAPI 兼容、OIDC 配置和 Compose 路由测试。
- 不增加第二套业务权限；Web 只能展示 Platform 已授权返回的数据。

## 验证

- Web CI 完成 lint、类型检查、单元/组件测试、生产构建、依赖审计和 Secret 检查。
- 消费方测试从固定 Platform OpenAPI 生成客户端并阻止接口漂移。
- Playwright 通过 OIDC 登录、Project、Repository、RuleSet、ScanJob、Finding 和处置主流程。
- Compose 中只有 Web 入口公开；直接访问内部数据库、Platform 或 Runner 被部署边界阻止。

## 重新评估

只有实际运营证明独立仓库导致无法接受的发布协调成本，或产品改为完全无浏览器界面时重新评估。重新合并到 Platform 必须给出迁移、发布、缓存、OIDC 和回滚方案。
