# 工程检查脚本中文阅读

本仓库的业务设计由需求、架构和 ADR 文档承载；可执行手写代码只有两个文档检查脚本，已补中文说明。工作流、契约和历史报告保持原内容。

先读 [check_docs.py](../scripts/check_docs.py)：从仓库根枚举 Markdown，依次收集本地链接、退役引用和文件结尾问题，再统一返回退出码。它只做离线静态检查，不验证远端链接、锚点或文档中描述的运行事实。

再读 [test_check_docs.py](../scripts/test_check_docs.py)：临时目录与替换 ROOT 让每个回归用真实文件验证精确模型名豁免、原有检测不退化及诊断行号。测试没有执行模型、部署或修改真实文档。

本地验证保持原命令：`python -m unittest discover -s scripts -p 'test_*.py' -v`，然后运行 `python scripts/check_docs.py`。中文注释不修改检查规则、批准记录或阶段状态。
