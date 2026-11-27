#!/usr/bin/env python3
"""Regression tests for claims that must not imply unperformed verification."""
from check_book import (
    breath_firmware_problems,
    claim_problems,
    cli_origin_problems,
    led_net_problems,
    preface_ladder_order_problems,
    round2_claim_problems,
    selection_lock_problems,
)

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


def test_led_net_contract_rejects_power_rail_branch() -> None:
    good = (
        "| `+3V3` | LDO 输出、MCU VCC | 稳压后的 3.3 V |\n"
        "| `LED` | MCU PB3、限流电阻 | PB3 驱动的 PWM 呼吸灯支路 |\n"
    )
    bad = good.replace("LDO 输出、MCU VCC |", "LDO 输出、MCU VCC、LED 限流电阻 |")
    assert led_net_problems(good) == []
    assert any("+3V3" in problem for problem in led_net_problems(bad))


def test_breathing_project_requires_firmware_and_toolchain() -> None:
    text = (
        "static void pwm_frame(uint8_t level)\n"
        "#define LEVELS 64U\n#define SLICE_US 150U\n"
        "PORTB |= (1 << PB3)\n"
        "avr-gcc -mmcu=attiny85 -Os -o breath.elf breath.c\n"
        "烧录 `breath.hex` 后，LED 能连续渐亮、渐暗并循环\n"
        "avr-gcc --version\navr-objcopy --version\navrdude -v\n"
    )
    assert breath_firmware_problems(text) == []
    assert breath_firmware_problems(text.replace("breath.elf", "blink.elf"))


def test_cli_examples_share_one_origin() -> None:
    good = (
        "## 15.2 kicad-cli\n"
        "kicad-cli pcb export gerbers board.kicad_pcb --use-drill-file-origin\n\n"
        "kicad-cli pcb export drill board.kicad_pcb --drill-origin plot\n\n"
        "kicad-cli pcb export pos board.kicad_pcb --use-drill-file-origin\n\n"
        "## 15.3 Python API\n"
    )
    assert cli_origin_problems(good) == []
    assert cli_origin_problems(good.replace("--use-drill-file-origin", "", 1))
    assert cli_origin_problems(good.replace("--drill-origin plot", ""))


def test_open_selection_is_locked_before_layout() -> None:
    text = (
        "### 先把器件选型锁定\n"
        "MPN、数据手册、封装\n"
        "暂时没有决定的格子标“待定”\n"
        "AVR 编译与烧录工具链的安装入口见 12.3\n"
    )
    assert selection_lock_problems(text) == []
    assert selection_lock_problems(text.replace("MPN、数据手册、封装", "型号"))


def test_round2_calibrations_cannot_drift_back() -> None:
    texts = {
        "ch02": "输入电流约 9–10 mA；引脚编号和电气类型仍要按所选器件的数据手册核对",
        "ch06": "**不含 `Iq`**",
        "ch07": "在这个 20 ns 假设下",
        "ch08": "量级估算，不是合格证；特定几何；不要用它当验收签字",
        "ch10": "版本与日期、层数、板厚、铜厚、表面处理、单位、原点、特殊工艺、联系人",
        "ch11": "工艺选择要和实际贴片厂确认",
        "ch12": "不要拿“几 mA”当通用标准",
        "ch15": "版本受约束、但不是完全可复现；同一个文件的后半段；docker buildx imagetools inspect",
    }
    assert round2_claim_problems(texts) == []
    assert round2_claim_problems({**texts, "ch07": "本板不需要阻抗控制"})
    assert round2_claim_problems({**texts, "ch08": "偏差就能控制在 1% 以内"})
    assert round2_claim_problems({**texts, "ch12": "MCU 未编程时通常几 mA"})
    assert round2_claim_problems({**texts, "ch15": "完全可复现"})


def test_preface_learning_path_figure_follows_table() -> None:
    table = (
        "| 阶段 | 交付物 | 过关证据 |\n"
        "| --- | --- | --- |\n"
        "| 入门（1—4） | 通过 ERC 的原理图与 BOM | 字段完整 |\n"
    )
    figure = (
        "```ill\nkicad-learning-path\n```\n\n"
        "图 0-1 从入门到工程化的四个阶段；卡片内容与上表对应。\n"
    )
    assert preface_ladder_order_problems("（图 0-1）\n" + table + figure) == []
    assert preface_ladder_order_problems(figure + table)


if __name__ == "__main__":
    test_old_claims_are_rejected()
    test_new_claims_pass()
    test_led_net_contract_rejects_power_rail_branch()
    test_breathing_project_requires_firmware_and_toolchain()
    test_cli_examples_share_one_origin()
    test_open_selection_is_locked_before_layout()
    test_round2_calibrations_cannot_drift_back()
    test_preface_learning_path_figure_follows_table()
    print("claim regression: OK")
