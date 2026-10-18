from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


CHECKER_PATH = Path(__file__).with_name("check_docs.py")
SPEC = importlib.util.spec_from_file_location("check_docs_under_test", CHECKER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load documentation checker")
check_docs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_docs)


class LegacyReferenceTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        self.root = Path(temporary_directory.name)
        root_patch = patch.object(check_docs, "ROOT", self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)

    def check_markdown(self, text: str) -> list[str]:
        markdown = self.root / "example.md"
        markdown.write_text(text, encoding="utf-8")
        return check_docs.check_legacy_references([markdown])

    def test_exact_approved_model_is_not_a_legacy_reference(self) -> None:
        cases = (
            "`DeepSeek-V4.1-Flash-1017`\n",
            "Approved model: DeepSeek-V4.1-Flash-1017.\n",
            "Use (DeepSeek-V4.1-Flash-1017), subject to approval.\n",
            "映射为 `DeepSeek-V4.1-Flash-1017`；出口关闭。\n",
            "[model](https://example.invalid/models/DeepSeek-V4.1-Flash-1017)\n",
            "See https://example.invalid/models/DeepSeek-V4.1-Flash-1017?approved=true.\n",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual([], self.check_markdown(text))

    def test_approved_model_does_not_suppress_same_line_legacy_references(self) -> None:
        for text in (
            "`DeepSeek-V4.1-Flash-1017` still rejects V4.\n",
            "V4 and DeepSeek-V4.1-Flash-1017.\n",
        ):
            with self.subTest(text=text):
                self.assertEqual(["example.md:1: V4"], self.check_markdown(text))

    def test_other_model_like_names_remain_legacy_references(self) -> None:
        names = (
            "V4.1",
            "Other-V4.1-Flash-1017",
            "DeepSeek-V4.2-Flash-1017",
            "DeepSeek-V4.1-Flash-1018",
            "DeepSeek-V4.1-Flash",
            "DeepSeek-V4.1-Flash-101",
            "DeepSeek-V4.1-Flash-1017-preview",
            "DeepSeek-V4.1-Flash-1017.preview",
            "DeepSeek-V4.1-Flash-1017_annotated",
            "DeepSeek-V4.1-Flash-1017a",
            "DeepSeek-V4.1-Flash-10170",
            "PrefixDeepSeek-V4.1-Flash-1017",
            "deepseek-V4.1-Flash-1017",
        )
        for name in names:
            with self.subTest(name=name):
                self.assertEqual(
                    ["example.md:1: V4"], self.check_markdown(f"Model: `{name}`.\n")
                )

    def test_all_original_legacy_stage_identifiers_still_reject(self) -> None:
        identifiers = (
            [f"M{number}" for number in range(14)]
            + [f"D{number}" for number in range(17)]
            + [f"G{number}" for number in range(1, 5)]
            + [f"V{number}" for number in range(1, 6)]
        )
        for identifier in identifiers:
            with self.subTest(identifier=identifier):
                self.assertEqual(
                    [f"example.md:1: {identifier}"],
                    self.check_markdown(f"Retired `{identifier}`.\n"),
                )

    def test_all_original_retired_paths_still_reject(self) -> None:
        paths = (
            "engineering/",
            "runbooks/",
            "architecture/adr/",
            "reports/g1-",
            "reports/g2-",
            "reports/g3-",
            "reports/g4-",
            "reports/m0-",
            "requirements/v1-",
        )
        for retired_path in paths:
            with self.subTest(retired_path=retired_path):
                self.assertEqual(
                    [f"example.md:1: {retired_path}"],
                    self.check_markdown(f"Retired `{retired_path}example.md`.\n"),
                )

    def test_model_does_not_suppress_same_line_retired_path(self) -> None:
        self.assertEqual(
            ["example.md:1: engineering/"],
            self.check_markdown("DeepSeek-V4.1-Flash-1017 uses engineering/old.md.\n"),
        )

    def test_safe_text_passes(self) -> None:
        self.assertEqual(
            [],
            self.check_markdown(
                "# Current documentation\n"
                "阶段 4 uses ADR-0015 and input Schema 0.4.0.\n"
                "The requested alias remains `deepseek-flash`.\n"
            ),
        )

    def test_diagnostics_preserve_line_numbers_and_all_same_line_matches(self) -> None:
        self.assertEqual(
            ["example.md:2: M0, V4, engineering/", "example.md:3: D16"],
            self.check_markdown(
                "# Current documentation\n"
                "DeepSeek-V4.1-Flash-1017, V4, M0 and engineering/old.md.\n"
                "D16 remains retired.\n"
            ),
        )


if __name__ == "__main__":
    unittest.main()
