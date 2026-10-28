from __future__ import annotations

# 文档仓库离线检查器：检查本地目标存在、退役标识和文件结尾，不请求网页或执行文档示例。
import re
import sys
from pathlib import Path
from urllib.parse import unquote


# 路径以脚本所属仓库为根，调用目录变化不会切换检查对象。
ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
LEGACY_REFERENCE = re.compile(
    r"\b(?:M(?:[0-9]|1[0-3])|D(?:[0-9]|1[0-6])|G[1-4]|V[1-5])\b"
    r"|engineering/|runbooks/|architecture/adr/"
    r"|reports/(?:g[1-4]-|m0-)|requirements/v1-"
)
APPROVED_MODEL_REFERENCE = re.compile(
    r"(?<![\w.-])DeepSeek-V4\.1-Flash-1017(?![\w-]|\.[\w-])"
)
SKIPPED_SCHEMES = ("http://", "https://", "mailto:", "codex://", "#")


def relative(path: Path) -> str:
    # 诊断使用仓库相对路径，便于 CI 与本地定位同一文件。
    return path.relative_to(ROOT).as_posix()


def check_links(files: list[Path]) -> list[str]:
    # 提取简单 Markdown 链接/图片；只验证本地目标存在，不验证远端状态或页内锚点。
    errors: list[str] = []
    for file in files:
        text = file.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            target = match.group(1).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            if target.startswith(SKIPPED_SCHEMES):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            if not (file.parent / target).resolve().exists():
                errors.append(f"{relative(file)} -> {target}")
    return errors


def check_legacy_references(files: list[Path]) -> list[str]:
    # 仅排除获批的完整模型名，不能因此掩盖同一行中真正退役的编号或路径。
    errors: list[str] = []
    for file in files:
        for line_number, line in enumerate(file.read_text(encoding="utf-8").splitlines(), 1):
            # 只遮盖精确名称，保留周围文本以继续检测其他旧引用。
            legacy_text = APPROVED_MODEL_REFERENCE.sub(" ", line)
            matches = sorted(set(LEGACY_REFERENCE.findall(legacy_text)))
            if matches:
                errors.append(f"{relative(file)}:{line_number}: {', '.join(matches)}")
    return errors


def check_file_endings(files: list[Path]) -> list[str]:
    # 同时接受 LF/CRLF，但要求末尾换行且不能有多余空白行；不自动改文件。
    errors: list[str] = []
    trailing_blank_lines = re.compile(rb"(?:\r?\n[ \t]*){2,}$")
    for file in files:
        content = file.read_bytes()
        if not content.endswith(b"\n"):
            errors.append(f"{relative(file)}: missing final newline")
        elif trailing_blank_lines.search(content):
            errors.append(f"{relative(file)}: trailing blank line")
    return errors


def main() -> int:
    # 汇总全部类别再返回退出码，方便一次修复多项问题；不会因先遇到一类就跳过其他检查。
    files = sorted(path for path in ROOT.rglob("*.md") if ".git" not in path.parts)
    link_errors = check_links(files)
    legacy_errors = check_legacy_references(files)
    ending_errors = check_file_endings(files + [Path(__file__)])

    print(f"Markdown files checked: {len(files)}")
    print(f"Broken local links/images: {len(link_errors)}")
    print(f"Legacy documentation references: {len(legacy_errors)}")
    print(f"Invalid file endings: {len(ending_errors)}")

    for error in link_errors + legacy_errors + ending_errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if link_errors or legacy_errors or ending_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
