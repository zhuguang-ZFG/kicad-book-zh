#!/usr/bin/env python3
"""Prove the signal-integrity gate fails when the numbers are wrong.

A gate that has never been seen to go red is decoration. Each case below
breaks one number (or deletes one rule) in the chapter sources, runs
``check_book.py`` in a subprocess, and requires a ``ch07:``/``ch08:`` error.
A final control run requires the restored tree to be clean again, so a gate
that simply fails on everything cannot pass this test either.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CH07 = ROOT / "第二部分-设计篇/07-布线.md"
CH08 = ROOT / "第二部分-设计篇/08-铺铜与电磁兼容.md"

# (name, file, original, replacement, everywhere?)
MUTATIONS: list[tuple] = [
    ("bandwidth 175 -> 250 MHz", CH07,
     "| 2 ns | 约 175 MHz |", "| 2 ns | 约 250 MHz |"),
    ("threshold 60 -> 90 mm", CH07,
     "| 2 ns | 约 175 MHz | 约 60 mm |", "| 2 ns | 约 175 MHz | 约 90 mm |"),
    ("0.1 ns bandwidth 3.5 -> 1.2 GHz", CH07,
     "| 0.1 ns | 约 3.5 GHz |", "| 0.1 ns | 约 1.2 GHz |"),
    ("corner capacitance 20 -> 60 fF", CH07,
     "约 20 fF，对应时间常数约 0.5 ps", "约 60 fF，对应时间常数约 0.5 ps"),
    ("mm -> mil conversion 10 -> 14", CH07,
     "0.25 mm（约 10 mil）线宽", "0.25 mm（约 14 mil）线宽"),
    ("via stub 315 -> 900 fF", CH07,
     "最长残桩约 315 fF", "最长残桩约 900 fF"),
    ("microstrip 138 -> 50 ohm", CH07,
     "| 0.25 mm | 约 1.5 mm | 约 138 Ω |", "| 0.25 mm | 约 1.5 mm | 约 50 Ω |"),
    ("microstrip 112 -> 75 ohm", CH07,
     "| 0.5 mm | 约 1.5 mm | 约 112 Ω |", "| 0.5 mm | 约 1.5 mm | 约 75 Ω |"),
    ("3h result 4.5 -> 1.5 mm", CH08,
     "| 1.6 mm 两层板 | 约 1.5 mm | 约 4.5 mm |",
     "| 1.6 mm 两层板 | 约 1.5 mm | 约 1.5 mm |"),
    ("3h four-layer 0.6 -> 2.0 mm", CH08,
     "| 四层板（内层） | 约 0.2 mm | 约 0.6 mm |",
     "| 四层板（内层） | 约 0.2 mm | 约 2.0 mm |"),
    ("drop the 3h rule", CH08,
     "信号线两侧各留至少 **3 倍介质厚度 `h`**", "信号线两侧留一些铜"),
    ("drop every 3w mention", CH08,
     "3 倍线宽", "更大的间距", True),
    ("drop the 1% coupling fact", CH08,
     "1%", "很低的水平", True),
]


def _run_check() -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools/check_book.py")],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def _gate_errors(output: str) -> list[str]:
    return [line.strip() for line in output.splitlines()
            if line.strip().startswith("- ch07:") or line.strip().startswith("- ch08:")]


def test_each_mutation_turns_the_gate_red() -> None:
    for mutation in MUTATIONS:
        name, path, old, new = mutation[:4]
        everywhere = len(mutation) > 4 and mutation[4] is True
        original = path.read_text(encoding="utf-8")
        assert old in original, f"{name}: anchor not found, mutation never applied"
        try:
            path.write_text(original.replace(old, new) if everywhere
                            else original.replace(old, new, 1), encoding="utf-8")
            code, output = _run_check()
        finally:
            path.write_text(original, encoding="utf-8")
        assert code != 0, f"{name}: check_book.py stayed green (exit 0)"
        assert _gate_errors(output), f"{name}: exited {code} but with no ch07/ch08 error:\n{output[-800:]}"


def test_restored_tree_is_clean() -> None:
    code, output = _run_check()
    assert not _gate_errors(output), (
        "restored sources still trip the SI gate, so the red runs prove nothing:\n"
        + "\n".join(_gate_errors(output)))


if __name__ == "__main__":
    test_each_mutation_turns_the_gate_red()
    test_restored_tree_is_clean()
    print(f"SI number regression: OK ({len(MUTATIONS)} mutations detected)")
