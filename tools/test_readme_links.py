#!/usr/bin/env python3
"""Regression coverage for local README navigation destinations."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import check_book


def _collect_errors(root: Path, text: str) -> list[str]:
    (root / "README.md").write_text(text, encoding="utf-8")
    with patch.object(check_book, "ROOT", root), patch.object(check_book, "errors", []):
        check_book.check_artifact_claims()
        return list(check_book.errors)


def test_missing_chapter_link_is_rejected() -> None:
    with TemporaryDirectory() as tmp:
        errors = _collect_errors(Path(tmp), "[第 1 章](第一部分/不存在.md)\n")
        assert any("第一部分/不存在.md" in error for error in errors), errors


def test_existing_unicode_and_encoded_paths_pass() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        chapter = root / "第一部分" / "入门 示例.md"
        chapter.parent.mkdir()
        chapter.write_text("# 入门\n", encoding="utf-8")
        text = (
            "[入门](第一部分/入门%20示例.md)\n"
            "[带片段](第一部分/入门%20示例.md#学习目标)\n"
            "[带标题](第一部分/入门%20示例.md \"入门\")\n"
        )
        assert _collect_errors(root, text) == []


def test_external_fragment_and_code_examples_are_not_local_files() -> None:
    with TemporaryDirectory() as tmp:
        text = (
            "[官方](https://docs.kicad.org/10.0/)\n"
            "[联系](mailto:editor@example.org)\n"
            "[目录](#目录)\n"
            "`[代码示例](missing-inline.md)`\n"
            "```markdown\n[代码示例](missing-fenced.md)\n```\n"
        )
        assert _collect_errors(Path(tmp), text) == []


def test_reference_link_and_repository_escape_are_checked() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        errors = _collect_errors(root, "[章节][chapter]\n\n[chapter]: missing.md\n")
        assert any("missing.md" in error for error in errors), errors
        errors = _collect_errors(root, "[越界](../outside.md)\n")
        assert any("escapes repository root" in error for error in errors), errors


if __name__ == "__main__":
    test_missing_chapter_link_is_rejected()
    test_existing_unicode_and_encoded_paths_pass()
    test_external_fragment_and_code_examples_are_not_local_files()
    test_reference_link_and_repository_escape_are_checked()
    print("README link regression: OK")
