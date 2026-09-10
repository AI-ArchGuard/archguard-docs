from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
LEGACY_REFERENCE = re.compile(
    r"\b(?:M(?:[0-9]|1[0-3])|D(?:[0-9]|1[0-6])|G[1-4]|V[1-5])\b"
    r"|engineering/|runbooks/|architecture/adr/"
    r"|reports/(?:g[1-4]-|m0-)|requirements/v1-"
)
SKIPPED_SCHEMES = ("http://", "https://", "mailto:", "codex://", "#")


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def check_links(files: list[Path]) -> list[str]:
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
    errors: list[str] = []
    for file in files:
        for line_number, line in enumerate(file.read_text(encoding="utf-8").splitlines(), 1):
            matches = sorted(set(LEGACY_REFERENCE.findall(line)))
            if matches:
                errors.append(f"{relative(file)}:{line_number}: {', '.join(matches)}")
    return errors


def check_file_endings(files: list[Path]) -> list[str]:
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
