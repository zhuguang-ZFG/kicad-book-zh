#!/usr/bin/env python3
"""Regression tests for USB diagnostic checks in the book content checker."""
from unittest.mock import patch

import check_book


class _FixtureFile:
    def __init__(self, text: str) -> None:
        self.text = text

    def read_text(self, encoding: str = "utf-8") -> str:
        assert encoding == "utf-8"
        return self.text


class _FixtureRoot:
    def __init__(self, chapter: str, appendix: str) -> None:
        self.chapter = chapter
        self.appendix = appendix

    def __truediv__(self, path: str) -> _FixtureFile:
        if path.startswith("第三部分"):
            return _FixtureFile(self.chapter)
        return _FixtureFile(self.appendix)


def _collect_errors(chapter: str, appendix: str = "") -> list[str]:
    root = _FixtureRoot(chapter, appendix)
    with patch.object(check_book, "ROOT", root), patch.object(check_book, "errors", []):
        check_book.check_power_only_usb()
        return list(check_book.errors)


def test_negated_enumeration_explanations_pass_in_chapter_and_table() -> None:
    chapter = "### USB 供电握手失败\nUSB 不需要枚举；本板只取电、不传数据。\n"
    appendix = "| USB 不供电 | CC 下拉缺失 | 本板不需要进行枚举 | 换线 |\n"
    assert _collect_errors(chapter, appendix) == []


def test_long_negation_phrase_passes_in_chapter_and_table() -> None:
    chapter = "### USB 供电握手失败\n本板不需要对 USB 设备进行枚举；本板只取电、不传数据。\n"
    appendix = "| USB 供电异常 | 本板不需要对 USB 设备进行枚举 | 查看设备状态 | 排查主机 |\n"
    assert _collect_errors(chapter, appendix) == []


def test_enumeration_diagnostics_still_fail_in_chapter_and_table() -> None:
    chapter = "### USB 供电握手失败\n连接后检查是否枚举成功。\n"
    appendix = "| USB 设备故障 | 无法识别 | 检查设备是否枚举成功 | 排查主机 |\n"
    errors = _collect_errors(chapter, appendix)
    assert any(error.startswith("ch12:") for error in errors), errors
    assert any(error.startswith("appendix C:") for error in errors), errors


def test_negated_clause_does_not_hide_separate_diagnostic() -> None:
    chapter = "### USB 供电握手失败\nUSB 无需对 USB 设备进行枚举；如果无法枚举则检查主机。\n"
    appendix = "| USB 供电异常 | 本板无需对 USB 设备进行枚举；如果无法枚举则检查主机 | 查看设备状态 | 排查主机 |\n"
    errors = _collect_errors(chapter, appendix)
    assert any(error.startswith("ch12:") for error in errors), errors
    assert any(error.startswith("appendix C:") for error in errors), errors


def test_data_line_diagnostics_still_fail() -> None:
    chapter = "### USB 供电握手失败\n检查 D+/D- 是否反接。\n"
    errors = _collect_errors(chapter)
    assert any(error.startswith("ch12:") for error in errors), errors


if __name__ == "__main__":
    test_negated_enumeration_explanations_pass_in_chapter_and_table()
    test_long_negation_phrase_passes_in_chapter_and_table()
    test_enumeration_diagnostics_still_fail_in_chapter_and_table()
    test_negated_clause_does_not_hide_separate_diagnostic()
    test_data_line_diagnostics_still_fail()
    print("USB diagnostic regression: OK")
