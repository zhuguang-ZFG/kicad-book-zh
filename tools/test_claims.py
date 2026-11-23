#!/usr/bin/env python3
"""Regression tests for claims that must not imply unperformed verification."""
from check_book import claim_problems


OLD_PREAMBLE = "书中命令在 KiCad 10.0.8 的 CLI 上核对过。"
OLD_NOTICE = "示例工程、命令与检查步骤均在本地构建链上核对。"
OLD_STRUCTURE = "usb_breath_led/             # 教学用参考工程"

NEW_PREAMBLE = "书中命令按 KiCad 10.0.8 的 CLI 文档核对过。"
NEW_NOTICE = "书中命令与检查步骤按官方文档核对，示例工程由读者按章节自行建立。"
NEW_STRUCTURE = "usb_breath_led/             # 读者按章节建立的工程（不随书附带）"


def test_old_claims_are_rejected() -> None:
    problems = claim_problems(OLD_PREAMBLE, OLD_NOTICE, OLD_STRUCTURE)
    assert any("executed on CLI" in p for p in problems), problems
    assert any("local build-chain" in p for p in problems), problems
    assert any("as existing" in p for p in problems), problems


def test_new_claims_pass() -> None:
    assert claim_problems(NEW_PREAMBLE, NEW_NOTICE, NEW_STRUCTURE) == []


if __name__ == "__main__":
    test_old_claims_are_rejected()
    test_new_claims_pass()
    print("claim regression: OK")
