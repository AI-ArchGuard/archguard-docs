# Architecture

本目录只维护跨仓库总体架构，不保存单个模块的类设计、接口草稿或实施步骤。

- [系统上下文](context.md)：用户、外部系统和一级信任边界。
- [容器与六平面](containers.md)：Platform、Scanner、Gateway、Agent、Evals 和 Deploy 的所有权。
- [ADR 索引](../adr/README.md)：重要选择、原因和替代关系。

Scanner、Platform、Gateway 等实现级设计分别保存在对应仓库的 `docs/technical-design/`。跨仓库机器接口由生产者发布，状态在[契约索引](../contracts/README.md)汇总。
