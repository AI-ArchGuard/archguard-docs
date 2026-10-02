# Reports

本目录只保存阶段退出、正式发布、性能基线、安全测试和故障演练的可复现证据。日常 CI 输出保留在 CI/PR，不为每个切片创建独立验收报告。

## 当前有效报告

- [阶段 0 Foundation 验收](2026-09-10-foundation-acceptance.md)
- [阶段 1 Scanner `v0.2.0` 验收](2026-09-19-scanner-v0.2.0-acceptance.md)
- [阶段 2 Platform `v0.3.0` 验收](2026-09-22-platform-v0.3.0-acceptance.md)
- [阶段 3 持续治理 `v0.4.0` 验收](2026-09-27-governance-v0.4.0-acceptance.md)

报告必须写明对象版本、环境、执行方式、结果和未验证项，不得包含密钥、个人数据或真实客户源码。被新阶段报告完全取代且没有合规保留要求时，应删除旧报告并同步链接。

阶段 4 尚未退出；当前合成 Compose 证据见 Deploy [4H Issue](https://github.com/AI-ArchGuard/archguard-deploy/issues/10)和[候选矩阵](https://github.com/AI-ArchGuard/archguard-deploy/blob/main/compatibility/agent-synthetic.md)。真实外发/正式发布关卡未满足前，不创建 Passed/Closed 阶段报告，也不以切片日志代替唯一退出报告。

最终阶段 4 报告须按 [ADR-0012](../adr/0012-personal-deepseek-release-scope.md)明确个人自用、合成真实调用和本地演练范围，并链接延期的 ADR-0010/0011 企业/客户严格条件；范围批准不是调用或验收通过。不得宣称零保留、固定处理地区、企业数据、数据库灾备或生产负载验收通过。
