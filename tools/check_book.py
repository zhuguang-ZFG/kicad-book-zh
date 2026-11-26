#!/usr/bin/env python3
"""Content checks for the KiCad book.

This is deliberately narrower than the HTML assembler: it checks facts that
the assembler cannot know (pin maps, figure references, SVG contracts) and
fails loudly instead of producing a pretty but wrong book.
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "yuyu-book"
ART = BOOK / "illustrations"
MANIFEST = json.loads((BOOK / "manifest.json").read_text(encoding="utf-8"))

errors: list[str] = []


def md_files() -> list[Path]:
    out = []
    for p in ROOT.rglob("*.md"):
        if ("yuyu-book" in p.parts or "node_modules" in p.parts
                or ".git" in p.parts or ".tmp" in p.parts
                or "book-improvement" in p.parts):
            continue
        out.append(p)
    return sorted(out)


def book_sources() -> list[Path]:
    """Return exactly the files assembled into the book, in manifest order."""
    paths = [ROOT / MANIFEST["front"]["zh"]]
    for part in MANIFEST["parts"]:
        paths.extend(ROOT / unit["zh"] for unit in part["units"])
    paths.extend(ROOT / unit["zh"] for unit in MANIFEST["appendices"])
    return paths


def check_units() -> None:
    units = [MANIFEST["front"]]
    for part in MANIFEST["parts"]:
        units.extend(part["units"])
    units.extend(MANIFEST["appendices"])
    for u in units:
        p = ROOT / u["zh"]
        if not p.exists():
            errors.append(f"missing unit file: {p}")
            continue
        text = p.read_text(encoding="utf-8")
        first = next((ln for ln in text.splitlines() if ln.startswith("# ")), "")
        if not first:
            errors.append(f"{p}: no H1")
        if len(text.strip()) < 1200:
            errors.append(f"{p}: too short ({len(text.strip())} chars)")
        if p.parent.name.startswith("第") and "第" in first and "章" not in first:
            errors.append(f"{p}: chapter H1 lacks 章")


_SOURCE_FIG_CAPTION = re.compile(r"^\s*(?:\*)?图\s*([A-Za-z]|\d+)-(\d+)")
_SOURCE_FIG_CAPTION_HTML = re.compile(
    r'<span class="fig-no">\s*图\s*([A-Za-z]|\d+)-(\d+)\s*</span>')


def source_figure_number_problems() -> list[str]:
    """Source captions must be 1..N per chapter even though the renderer
    renumbers figures. Duplicate or out-of-order source numbers make the
    Markdown misleading and hide a future renderer regression."""
    problems: list[str] = []
    for p in book_sources():
        captions: list[tuple[str, int]] = []
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.lstrip().startswith("!["):
                continue  # image alt text repeats the caption number by design
            html = _SOURCE_FIG_CAPTION_HTML.findall(line)
            if html:
                captions.extend((prefix, int(number)) for prefix, number in html)
                continue
            m = _SOURCE_FIG_CAPTION.match(line)
            if m:
                captions.append((m.group(1), int(m.group(2))))
        if not captions:
            continue
        prefixes = {prefix for prefix, _ in captions}
        if len(prefixes) != 1:
            problems.append(f"{p}: mixed source figure prefixes {sorted(prefixes)}")
        actual = [number for _, number in captions]
        expected = list(range(1, len(actual) + 1))
        if actual != expected:
            problems.append(
                f"{p}: source figure captions {actual}, expected {expected}")
    return problems


def check_source_figure_numbers() -> None:
    errors.extend(source_figure_number_problems())


def check_ills() -> None:
    names = set()
    for p in md_files():
        text = p.read_text(encoding="utf-8")
        for name in re.findall(r"```ill\n([^\n]+)\n```", text):
            names.add(name.strip())
            svg = ART / f"{name.strip()}.svg"
            if not svg.exists():
                errors.append(f"{p}: ill references missing {svg.name}")
    for svg in ART.glob("*.svg"):
        text = svg.read_text(encoding="utf-8")
        if "viewBox" not in text.split(">", 1)[0]:
            errors.append(f"{svg.name}: no viewBox")
        if "currentColor" not in text:
            errors.append(f"{svg.name}: no currentColor")
        for bad in ("<script", "<style", " id=", "href=", "url("):
            if bad in text:
                errors.append(f"{svg.name}: banned {bad!r}")
        if len(text.encode("utf-8")) > 24000:
            errors.append(f"{svg.name}: too large for inline")
    print(f"illustrations referenced: {len(names)}; files: {len(list(ART.glob('*.svg')))}")


def check_photos() -> None:
    """Every offline photograph must exist, fit the inline budget and be credited."""
    names: set[str] = set()
    photo_types = {".jpg", ".jpeg", ".png", ".webp"}
    for p in md_files():
        text = p.read_text(encoding="utf-8")
        for name in re.findall(r"!\[[^\]]*\]\(illustrations/([^)]+)\)", text):
            names.add(name)
            photo = ART / name
            if not photo.is_file():
                errors.append(f"{p}: photograph missing {name}")
                continue
            if photo.suffix.lower() not in photo_types:
                errors.append(f"{p}: unsupported photograph type {name}")
            if photo.stat().st_size > 300_000:
                errors.append(
                    f"{name}: {photo.stat().st_size} bytes, over the 300000-byte inline budget")
    credits_path = ART / "README.md"
    credits = credits_path.read_text(encoding="utf-8") if credits_path.exists() else ""
    if not credits:
        errors.append("illustrations/README.md: missing photograph credits")
    for name in sorted(names):
        if name not in credits:
            errors.append(f"illustrations/README.md: no credit row for {name}")
    shipped = {p.name for p in ART.glob("photo-*") if p.suffix.lower() in photo_types}
    for name in sorted(shipped - names):
        errors.append(f"{name}: shipped photograph is not referenced")
    print(f"photographs referenced: {len(names)}; files: {len(shipped)}")


_SCREENSHOT_IMG = re.compile(r'<img[^>]+src="(?:\.\./)?yuyu-book/screenshots/([^"]+)"')


def check_screenshots() -> None:
    """Every embedded UI screenshot must exist and have a provenance row."""
    names: set[str] = set()
    shot_types = {".jpg", ".jpeg", ".png", ".webp"}
    for p in md_files():
        text = p.read_text(encoding="utf-8")
        for name in _SCREENSHOT_IMG.findall(text):
            names.add(name)
            shot = BOOK / "screenshots" / name
            if not shot.is_file():
                errors.append(f"{p}: screenshot missing {name}")
                continue
            if shot.suffix.lower() not in shot_types:
                errors.append(f"{p}: unsupported screenshot type {name}")
            if shot.stat().st_size == 0:
                errors.append(f"{name}: empty screenshot")
    credits_path = BOOK / "screenshots/README.md"
    credits = credits_path.read_text(encoding="utf-8") if credits_path.exists() else ""
    if not credits:
        errors.append("screenshots/README.md: missing screenshot credits")
    for name in sorted(names):
        row = re.compile(
            rf"^\|\s*`{re.escape(name)}`\s*\|\s*https?://", re.MULTILINE)
        if not row.search(credits):
            errors.append(f"screenshots/README.md: no credit row for {name}")
    shipped = {p.name for p in (BOOK / "screenshots").glob("*")
               if p.suffix.lower() in shot_types}
    for name in sorted(shipped - names):
        errors.append(f"{name}: shipped screenshot is not referenced")
    print(f"screenshots referenced: {len(names)}; files: {len(shipped)}")


def check_attiny_pinmap() -> None:
    text = (ROOT / "第一部分-入门篇/02-原理图第一笔.md").read_text(encoding="utf-8")
    required = {
        "1": "PB5",
        "2": "PB3",
        "3": "PB4",
        "4": "GND",
        "5": "PB0",
        "6": "PB1",
        "7": "PB2",
        "8": "VCC",
    }
    for pin, name in required.items():
        row = re.search(rf"^\|\s*{pin}\s*\|\s*([^|]+)\|", text, re.M)
        if not row:
            errors.append(f"ATtiny table: missing row {pin}")
            continue
        if name not in row.group(1):
            errors.append(f"ATtiny table: pin {pin} should be {name}, got {row.group(1).strip()}")
    # ISP mapping must be explicit and correct
    if not re.search(r"PB0（pin 5）.*PB1（pin 6）.*PB2（pin 7）", text):
        errors.append("ATtiny: ISP mapping sentence is missing or out of order")
    # Catch the old, wrong mapping in prose.
    for bad in (r"PB3[^\n]{0,30}MOSI", r"PB4[^\n]{0,30}MISO", r"PB2[^\n]{0,30}RESET"):
        if re.search(bad, text):
            errors.append(f"ATtiny: stale wrong mapping matches {bad!r}")
    fig = (ART / "kicad-ch02-symbol-anatomy.svg").read_text(encoding="utf-8")
    for token in ("RESET", "PB3", "PB4", "GND", "PB0/MOSI", "PB1/MISO", "PB2/SCK", "VCC"):
        if token not in fig:
            errors.append(f"symbol figure missing label {token!r}")


def led_net_problems(text: str) -> list[str]:
    """Keep the schematic contract aligned with the PB3 LED branch."""
    problems: list[str] = []
    rows = {m.group(1): m.group(2).strip()
            for m in re.finditer(r"^\|\s*`([^`]+)`\s*\|\s*([^|]+)\|\s*([^|]+)\|", text, re.M)}
    rail = rows.get("+3V3", "")
    led = rows.get("LED", "")
    if "LED" in rail or "限流电阻" in rail:
        problems.append("+3V3 must not include the LED branch")
    if "PB3" not in led or "限流电阻" not in led:
        problems.append("LED net must join MCU PB3 and the series resistor")
    return problems


def check_led_net_contract() -> None:
    text = (ROOT / "第一部分-入门篇/02-原理图第一笔.md").read_text(encoding="utf-8")
    errors.extend(f"ch02: {problem}" for problem in led_net_problems(text))


def selection_lock_problems(text: str) -> list[str]:
    """Open component selection must be recorded before layout/purchasing."""
    problems: list[str] = []
    for token in ("### 先把器件选型锁定", "MPN、数据手册、封装",
                  "暂时没有决定的格子标“待定”", "AVR 编译与烧录工具链的安装入口见 12.3"):
        if token not in text:
            problems.append(f"missing selection-lock contract: {token}")
    return problems


def check_selection_lock() -> None:
    text = (ROOT / "第一部分-入门篇/02-原理图第一笔.md").read_text(encoding="utf-8")
    errors.extend(f"ch02: {problem}" for problem in selection_lock_problems(text))


def round2_claim_problems(texts: dict[str, str]) -> list[str]:
    """Keep round-two calibrations explicit instead of silently drifting back."""
    required = {
        "ch02": ("输入电流约 9–10 mA",
                 "引脚编号和电气类型仍要按所选器件的数据手册核对"),
        "ch06": ("**不含 `Iq`**",),
        "ch07": ("在这个 20 ns 假设下",),
        "ch08": ("量级估算，不是合格证", "特定几何", "不要用它当验收签字"),
        "ch10": ("版本与日期、层数、板厚、铜厚、表面处理、单位、原点、特殊工艺、联系人",),
        "ch11": ("工艺选择要和实际贴片厂确认",),
        "ch12": ("不要拿“几 mA”当通用标准",),
        "ch15": ("版本受约束、但不是完全可复现", "同一个文件的后半段",
                 "docker buildx imagetools inspect"),
    }
    forbidden = {
        "ch02": ("照抄结构通常比自创更稳",),
        "ch07": ("**本板不需要阻抗控制、不需要等长、不需要仿真**",),
        "ch08": ("偏差就能控制在 1% 以内", "串扰基本可以不管",
                 "至少各有 3 倍介质厚度宽"),
        "ch12": ("MCU 未编程时通常几 mA",),
    }
    problems: list[str] = []
    for key, tokens in required.items():
        text = texts.get(key, "")
        problems.extend(f"{key}: missing calibration: {token}"
                        for token in tokens if token not in text)
    for key, tokens in forbidden.items():
        text = texts.get(key, "")
        problems.extend(f"{key}: restored overclaim: {token}"
                        for token in tokens if token in text)
    return problems


def check_round2_contracts() -> None:
    paths = {
        "ch02": "第一部分-入门篇/02-原理图第一笔.md",
        "ch06": "第二部分-设计篇/06-布局.md",
        "ch07": "第二部分-设计篇/07-布线.md",
        "ch08": "第二部分-设计篇/08-铺铜与电磁兼容.md",
        "ch10": "第三部分-制造篇/10-输出制造文件.md",
        "ch11": "第三部分-制造篇/11-打样与组装.md",
        "ch12": "第三部分-制造篇/12-焊接调试与返修.md",
        "ch15": "第四部分-进阶篇/15-自动化与插件.md",
    }
    texts = {key: (ROOT / path).read_text(encoding="utf-8")
             for key, path in paths.items()}
    errors.extend(round2_claim_problems(texts))


def breath_firmware_problems(text: str) -> list[str]:
    """The named project must ship a breathing baseline, not only blink."""
    problems: list[str] = []
    required = (
        "static void pwm_frame(uint8_t level)",
        "#define LEVELS 64U",
        "#define SLICE_US 150U",
        "PORTB |= (1 << PB3)",
        "avr-gcc -mmcu=attiny85 -Os -o breath.elf breath.c",
        "烧录 `breath.hex` 后，LED 能连续渐亮、渐暗并循环",
        "avr-gcc --version",
        "avr-objcopy --version",
        "avrdude -v",
    )
    for token in required:
        if token not in text:
            problems.append(f"missing breathing/toolchain contract: {token}")
    return problems


def check_breath_firmware() -> None:
    text = (ROOT / "第三部分-制造篇/12-焊接调试与返修.md").read_text(encoding="utf-8")
    errors.extend(f"ch12: {problem}" for problem in breath_firmware_problems(text))


def cli_origin_problems(text: str) -> list[str]:
    """Gerber, drill and POS examples must share the drill/place origin."""
    section = re.search(r"(?ms)^## 15\.2 .*?(?=^## 15\.3 )", text)
    if not section:
        return ["section 15.2 is missing"]
    body = section.group(0)
    problems: list[str] = []
    gerbers = re.search(r"kicad-cli pcb export gerbers[\s\S]*?\n\n", body)
    drill = re.search(r"kicad-cli pcb export drill[\s\S]*?\n\n", body)
    pos = re.search(r"kicad-cli pcb export pos[\s\S]*?\n\n", body)
    if not gerbers or "--use-drill-file-origin" not in gerbers.group(0):
        problems.append("15.2 Gerber export must use --use-drill-file-origin")
    if not drill or "--drill-origin plot" not in drill.group(0):
        problems.append("15.2 drill export must use --drill-origin plot")
    if not pos or "--use-drill-file-origin" not in pos.group(0):
        problems.append("15.2 POS export must use --use-drill-file-origin")
    return problems


def check_cli_origin_contract() -> None:
    text = (ROOT / "第四部分-进阶篇/15-自动化与插件.md").read_text(encoding="utf-8")
    errors.extend(f"ch15: {problem}" for problem in cli_origin_problems(text))


def check_sources() -> None:
    data = json.loads((BOOK / "sources.json").read_text(encoding="utf-8"))
    official_libraries = {"kicad-symbols", "kicad-footprints", "klc"}
    for key in sorted(official_libraries):
        if key not in data:
            errors.append(f"source {key}: missing official library/guideline entry")
        elif data[key].get("kind") != "library":
            errors.append(f"source {key}: official library/guideline must use kind:library")
    for key in ("attiny25-45-85-datasheet", "avrdude-8-1-manual", "microchip-avr-gcc",
                "kicad-docs-eeschema", "kicad-docs-pcbnew", "kicad-docs-cli"):
        if key not in data:
            errors.append(f"source {key}: missing device/toolchain/documentation reference")
    for key, src in data.items():
        if key == "schema_version":
            continue
        for field in ("title", "authority", "kind", "url", "snapshot", "accessed", "license", "scope"):
            if not str(src.get(field, "")).strip():
                errors.append(f"source {key}: empty {field}")
        if not str(src.get("url", "")).startswith("https://"):
            errors.append(f"source {key}: url must be https")
        if src.get("kind") in ("community", "book") and src.get("normative") is not False:
            errors.append(f"source {key}: {src.get('kind')} must set normative:false")


def check_cli_claims() -> None:
    # BOM: the quantity field is QUANTITY, not the display label Qty.
    found_fields = False
    for p in md_files():
        text = p.read_text(encoding="utf-8")
        for match in re.finditer(r'--fields "([^"]+)"', text):
            found_fields = True
            fields = [f.strip() for f in match.group(1).split(",")]
            if "Qty" in fields:
                errors.append(f"{p}: BOM --fields uses display name Qty")
            if "QUANTITY" not in fields:
                errors.append(f"{p}: BOM --fields must include QUANTITY")
    if not found_fields:
        errors.append("no BOM --fields example found")

    # jobset --output is a destination selector, not a directory.
    # Scope the check to fenced bash examples so prose cannot satisfy it.
    ch10 = (ROOT / "第三部分-制造篇/10-输出制造文件.md").read_text(encoding="utf-8")
    jobset_blocks = [b for b in re.findall(r"```bash\n([\s\S]*?)```", ch10) if "jobset run" in b]
    if not jobset_blocks:
        errors.append("ch10: no jobset run example")
    for block in jobset_blocks:
        for match in re.finditer(r"--output\s+(\S+)", block):
            if match.group(1).endswith("/"):
                errors.append("ch10: jobset --output looks like a directory")
    if "不是输出目录" not in ch10:
        errors.append("ch10: jobset --output semantics not explained")

    # The DRC exit code figure must say that 5 requires the flag.
    fig = (ART / "kicad-ch10-cli.svg").read_text(encoding="utf-8")
    claims_exit_codes = ("0 = 通过" in fig or "5 = 有违规" in fig)
    if claims_exit_codes and "--exit-code-violations" not in fig:
        errors.append("ch10-cli figure: exit code 5 needs --exit-code-violations")
    if "只有加 `--exit-code-violations`" not in ch10:
        errors.append("ch10: DRC exit code not qualified in prose")


def check_lib_table_examples() -> None:
    """Every sym-lib-table example must put its version first."""
    for p in md_files():
        text = p.read_text(encoding="utf-8")
        for block in re.findall(r"```text\n([\s\S]*?)```", text):
            if "(sym_lib_table" in block and not re.search(
                    r"\(sym_lib_table\s*\(version\s+\d+\)", block):
                errors.append(f"{p}: sym-lib-table example lacks (version ...) after opener")


def check_trace_width_table() -> None:
    """Chapter 7's table claims IPC-2221 values; recompute them."""
    text = (ROOT / "第二部分-设计篇/07-布线.md").read_text(encoding="utf-8")
    rows = re.findall(
        r"^\|\s*([0-9.]+)\s*A\s*\|\s*约\s*([0-9.]+)\s*mm\s*\|"
        r"\s*约\s*([0-9.]+)\s*mm\s*\|",
        text, re.M)
    if len(rows) != 4:
        errors.append(f"ch07: expected 4 trace-width rows, got {len(rows)}")
        return
    thickness_mil = 1.378  # 1 oz copper
    for current, outer_mm, inner_mm in rows:
        i = float(current)
        for layer, k, claimed in (("outer", 0.048, float(outer_mm)),
                                  ("inner", 0.024, float(inner_mm))):
            area = (i / (k * 10 ** 0.44)) ** (1 / 0.725)  # mil^2
            expected = area / thickness_mil * 0.0254       # mm
            if abs(claimed - expected) > max(0.05, expected * 0.08):
                errors.append(
                    f"ch07: {i} A {layer} width {claimed} mm, IPC-2221 gives "
                    f"{expected:.2f} mm")


def check_file_header_examples() -> None:
    """Each KiCad 10 header quotes its generator and carries its version."""
    expected = (("kicad_sch", "eeschema"), ("kicad_pcb", "pcbnew"))
    for p in md_files():
        text = p.read_text(encoding="utf-8")
        for block in re.findall(r"```text\n([\s\S]*?)```", text):
            for file_type, generator in expected:
                starts = [m.start() for m in re.finditer(
                    rf"\({file_type}\s+\(version", block)]
                header = re.compile(
                    rf"\({file_type}\s+\(version\s+\d+\)\s+"
                    rf"\(generator\s+\"{generator}\"\)\s+"
                    r"\(generator_version\s+\"[^\"]+\"\)")
                if any(not header.match(block, start) for start in starts):
                    errors.append(f"{p}: {file_type} header must quote {generator} and include generator_version")


def check_si_numbers() -> None:
    """Recompute every signal-integrity number quoted in chapters 7 and 8.

    These figures are easy to copy wrong and hard for a reader to spot, so the
    table values are derived here from the same constants the prose states
    (BW = 0.35/RT, 6.7 ps/mm on FR4, TD > 0.2*RT, C_corner = 2*w(mil) fF,
    stub = 5 fF/mil, reference copper 3h, spacing 3w). If a constant and a
    table drift apart, the check fails instead of the book lying quietly.
    """
    ch07 = (ROOT / "第二部分-设计篇/07-布线.md").read_text(encoding="utf-8")
    ch08 = (ROOT / "第二部分-设计篇/08-铺铜与电磁兼容.md").read_text(encoding="utf-8")
    if "在这个 20 ns 假设下" not in ch07:
        errors.append("ch07: 7.3 conclusion must stay conditional on the 20 ns assumption")
    delay_ps_per_mm = 6.7

    # -- 7.3 bandwidth / length threshold table -------------------------
    rows = re.findall(
        r"^\|\s*([0-9.]+)\s*ns\s*\|\s*约\s*([0-9.]+)\s*(MHz|GHz)\s*\|\s*约\s*([0-9.]+)\s*mm\s*\|",
        ch07, re.M)
    if len(rows) != 4:
        errors.append(f"ch07: expected 4 SI threshold rows, got {len(rows)}")
    for rt_ns, bw, unit, length_mm in rows:
        rt = float(rt_ns) * 1e-9
        want_bw = 0.35 / rt / 1e6
        stated_bw = float(bw) * (1000 if unit == "GHz" else 1)
        want_len = 0.2 * rt * 1e12 / delay_ps_per_mm
        if abs(stated_bw - want_bw) > max(1.0, want_bw * 0.06):
            errors.append(
                f"ch07: RT {rt_ns} ns bandwidth {bw} {unit}, 0.35/RT gives {want_bw:.0f} MHz")
        if abs(float(length_mm) - want_len) > max(1.0, want_len * 0.06):
            errors.append(
                f"ch07: RT {rt_ns} ns threshold {length_mm} mm, 0.2*RT/{delay_ps_per_mm} ps/mm gives {want_len:.0f} mm")

    # -- 7.3 corner capacitance ----------------------------------------
    corners = re.findall(r"([0-9.]+)\s*mm（约\s*([0-9]+)\s*mil）线宽\s*→\s*约\s*([0-9]+)\s*fF", ch07)
    if len(corners) != 2:
        errors.append(f"ch07: expected 2 corner-capacitance examples, got {len(corners)}")
    for w_mm, mil, ff in corners:
        if abs(float(w_mm) / 0.0254 - float(mil)) > 1.0:
            errors.append(f"ch07: {w_mm} mm is not {mil} mil")
        want = 2 * float(mil)
        if abs(float(ff) - want) > max(2.0, want * 0.1):
            errors.append(f"ch07: corner at {mil} mil gives {ff} fF, 2*w(mil) gives {want:.0f} fF")

    # -- 7.3 via stub --------------------------------------------------
    stub = re.search(r"([0-9.]+)\s*mm\s*板厚（约\s*([0-9]+)\s*mil）.*?约\s*([0-9]+)\s*fF", ch07)
    if not stub:
        errors.append("ch07: via-stub example missing")
    else:
        t_mm, mil, ff = stub.groups()
        if abs(float(t_mm) / 0.0254 - float(mil)) > 1.5:
            errors.append(f"ch07: {t_mm} mm is not {mil} mil")
        want = 5 * float(mil)
        if abs(float(ff) - want) > max(5.0, want * 0.1):
            errors.append(f"ch07: stub {mil} mil gives {ff} fF, 5 fF/mil gives {want:.0f} fF")

    # -- 7.3 microstrip impedance table --------------------------------
    if "四层以上板子" in ch07 or "必须先改叠层" in ch07 or "就得先改叠层" in ch07:
        errors.append("ch07: do not turn the board's line-width result into a two-layer impossibility claim")
    zrows = re.findall(r"^\|\s*([0-9.]+)\s*mm\s*\|\s*约\s*([0-9.]+)\s*mm\s*\|\s*约\s*([0-9]+)\s*Ω\s*\|",
                       ch07, re.M)
    if len(zrows) != 3:
        errors.append(f"ch07: expected 3 microstrip impedance rows, got {len(zrows)}")
    for w_mm, h_mm, z in zrows:
        want = microstrip_z0(float(w_mm), float(h_mm))
        if abs(float(z) - want) > max(4.0, want * 0.08):
            errors.append(
                f"ch07: {w_mm} mm over {h_mm} mm claims {z} Ω, microstrip estimate gives {want:.0f} Ω")

    # -- 8.4 reference copper and spacing -------------------------------
    hrows = re.findall(r"^\|\s*([^|]+?)\s*\|\s*约\s*([0-9.]+)\s*mm\s*\|\s*约\s*([0-9.]+)\s*mm\s*\|",
                       ch08, re.M)
    if len(hrows) != 2:
        errors.append(f"ch08: expected 2 reference-width rows, got {len(hrows)}")
    for stack, h_mm, copper_mm in hrows:
        want = 3 * float(h_mm)
        if abs(float(copper_mm) - want) > max(0.2, want * 0.08):
            errors.append(
                f"ch08: {stack.strip()} h={h_mm} mm needs {want:.1f} mm of copper, table says {copper_mm} mm")
    if "4.5 mm" not in ch08:
        errors.append("ch08: prose must state the 3h result for the 1.6 mm two-layer board")

    # Scope the 3h/3w rules to section 8.4 so a passing mention elsewhere in the
    # chapter cannot satisfy the check while the actual rule was deleted.
    section = re.search(r"(?ms)^## 8\.4 .*?(?=^## )", ch08)
    if not section:
        errors.append("ch08: section 8.4 (return path) is missing")
    else:
        body = section.group(0)
        if "量级估算，不是合格证" not in body or "特定几何" not in body:
            errors.append("ch08: 8.4 must label 3h/3w as context-dependent estimates")
        if "3 倍介质厚度" not in body:
            errors.append("ch08: 8.4 must state the 3h reference-copper rule")
        if not re.search(r"3 倍线宽", body):
            errors.append("ch08: 8.4 must state the 3w spacing rule")
        if not re.search(r"3 倍线宽[^。]{0,60}?1%", body) and not re.search(
                r"1%[^。]{0,60}?3 倍线宽", body):
            errors.append("ch08: 8.4 must tie the 3w spacing to the ~1% coupling claim")


def microstrip_z0(w_mm: float, h_mm: float, er: float = 4.3) -> float:
    """Microstrip characteristic impedance, Hammerstad-Jensen style estimate.

    Same closed form the chapter uses for its 86-138 ohm claim: not a field
    solver, but accurate enough to catch a wrong table entry.
    """
    u = w_mm / h_mm
    ee = (er + 1) / 2 + (er - 1) / 2 / math.sqrt(1 + 12 / u)
    if u <= 1:
        return 60 / math.sqrt(ee) * math.log(8 / u + u / 4)
    return 120 * math.pi / (math.sqrt(ee) * (u + 1.393 + 0.667 * math.log(u + 1.444)))


def check_power_only_usb() -> None:
    """Reject USB data-enumeration diagnostics for the power-only example."""
    ch12 = (ROOT / "第三部分-制造篇/12-焊接调试与返修.md").read_text(encoding="utf-8")
    appendix = (ROOT / "附录/C-常见错误与排查表.md").read_text(encoding="utf-8")
    enumeration = re.compile(r"不识别|无法识别|无法枚举|枚举")
    not_required = re.compile(
        r"(?:不需要|无需|不必|不用)(?:进行)?[^。！？；;，,、:：\n|]*?枚举")
    data_checks = re.compile(
        r"(?:检查|测(?:量)?|确认|排查|验证)[^。\n|]{0,12}(?:D\+/D-|D\+|D-)")
    disconnected = re.compile(
        r"(?:D\+/D-|D\+|D-)[^。\n|]{0,16}(?:悬空|不接|不用于数据)")

    def has_data_diagnostic(text: str) -> bool:
        return bool(data_checks.search(disconnected.sub("", text)))

    def has_enumeration_diagnostic(text: str) -> bool:
        return bool(enumeration.search(not_required.sub("", text)))

    for section in re.split(r"(?m)(?=^### )", ch12):
        lines = section.splitlines()
        if lines and lines[0].startswith("### USB"):
            if has_enumeration_diagnostic(section) or has_data_diagnostic(section):
                errors.append("ch12: USB power-only diagnostics must not require data enumeration")
    for line in appendix.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells and "USB" in cells[0] and (has_enumeration_diagnostic(line) or has_data_diagnostic(line)):
            errors.append("appendix C: USB power-only row must not require data enumeration")


def readme_link_problems(readme: str, root: Path) -> list[str]:
    """Find broken local Markdown links in README, ignoring code and URLs."""
    visible_lines: list[str] = []
    fence_char = ""
    fence_length = 0
    for line in readme.splitlines():
        fence = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence_char:
            visible_lines.append("")
            if fence:
                marker = fence.group(1)
                if marker[0] == fence_char and len(marker) >= fence_length:
                    fence_char = ""
            continue
        if fence:
            marker = fence.group(1)
            fence_char, fence_length = marker[0], len(marker)
            visible_lines.append("")
            continue
        visible_lines.append(line)

    visible = "\n".join(visible_lines)
    visible = re.sub(r"(?<!`)`+[^`\n]*`+(?!`)", "", visible)
    link_pattern = re.compile(r"(?<!!)\[[^\]]*\]\(\s*(<[^>]+>|[^)\s]+)(?:\s+[^)]*)?\)")
    problems: list[str] = []
    for match in link_pattern.finditer(visible):
        target = match.group(1)
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        base = root.resolve()
        destination = (base / unquote(parsed.path)).resolve()
        try:
            destination.relative_to(base)
        except ValueError:
            problems.append(f"README: local link escapes repository root {target!r}")
        else:
            if not destination.is_file():
                problems.append(f"README: broken local link {target!r}")
    reference_pattern = re.compile(r"(?m)^[ \t]{0,3}\[[^\]]+\]:[ \t]*(<[^>]+>|[^\s]+)")
    for match in reference_pattern.finditer(visible):
        target = match.group(1)
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        base = root.resolve()
        destination = (base / unquote(parsed.path)).resolve()
        try:
            destination.relative_to(base)
        except ValueError:
            problems.append(f"README: local link escapes repository root {target!r}")
        else:
            if not destination.is_file():
                problems.append(f"README: broken local link {target!r}")
    return problems


def check_readme_stats() -> None:
    """README's word-count claim must track the chapter sources."""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    claims = re.findall(r"约\s*([0-9.]+)\s*万字符（([0-9.]+)\s*万汉字", readme)
    if not claims:
        return
    chars = 0
    han = 0
    for p in book_sources():
        text = p.read_text(encoding="utf-8")
        chars += len(text)
        han += len(re.findall(r"[\u4e00-\u9fff]", text))
    for claim_chars, claim_han in claims:
        if abs(chars - float(claim_chars) * 10000) > chars * 0.05:
            errors.append(
                f"README: claims {claim_chars} 万字符, sources have {chars / 10000:.2f} 万")
        if abs(han - float(claim_han) * 10000) > han * 0.05:
            errors.append(
                f"README: claims {claim_han} 万汉字, sources have {han / 10000:.2f} 万")


def check_artifact_claims() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    structure_path = ROOT / "STRUCTURE.md"
    structure = structure_path.read_text(encoding="utf-8") if structure_path.exists() else ""
    errors.extend(readme_link_problems(readme, ROOT))
    if "完整工程" in readme and not list(ROOT.glob("*.kicad_pro")):
        errors.append("README: claims a complete KiCad project but none exists")
    if "本次未生成" not in readme and re.search(r"PDF", readme):
        # A PDF claim is only acceptable if a PDF actually exists.
        if not list((ROOT / "yuyu-book/dist").glob("*.pdf")):
            errors.append("README: mentions PDF but dist/ has no PDF")

    claim = re.search(r"HTML：.*?约\s*([0-9.]+)\s*MB", readme)
    limit = re.search(r"HTML 构建大小 <\s*([0-9.]+)\s*MB", structure)
    if claim and not limit:
        errors.append("STRUCTURE: README claims HTML size but no build-size limit exists")
    if claim and limit and float(claim.group(1)) >= float(limit.group(1)):
        errors.append(
            f"STRUCTURE: HTML limit {limit.group(1)}MB is below the README claim "
            f"{claim.group(1)}MB")
    html = BOOK / "dist" / "kicad-book-zh.html"
    if claim and not html.exists():
        errors.append("README: claims HTML size but dist/ has no HTML artifact")
    if html.exists():
        size_mb = html.stat().st_size / 1_000_000
        if claim and abs(size_mb - float(claim.group(1))) > 0.15:
            errors.append(
                f"README: claims {claim.group(1)}MB HTML, artifact is {size_mb:.2f}MB")
        if limit and size_mb >= float(limit.group(1)):
            errors.append(
                f"STRUCTURE: HTML limit {limit.group(1)}MB, artifact is {size_mb:.2f}MB")



def claim_problems(preamble: str, notice: str, structure: str) -> list[str]:
    """Return problems with claims that would imply verification we did not do."""
    problems: list[str] = []
    if "CLI 上核对" in preamble:
        problems.append("preface: commands claimed to be executed on CLI")
    if "按 KiCad 10.0.8 的 CLI 文档核对" not in preamble:
        problems.append("preface: missing docs-based CLI wording")
    if "本地构建链" in notice:
        problems.append("manifest notice: claims local build-chain verification")
    if "按官方文档核对" not in notice:
        problems.append("manifest notice: missing docs-based verification wording")
    if "usb_breath_led/" in structure and "不随书附带" not in structure:
        problems.append("STRUCTURE: presents usb_breath_led/ as existing")
    return problems


def check_unverified_claims() -> None:
    preamble = (ROOT / "00-前言.md").read_text(encoding="utf-8")
    notice = json.loads((BOOK / "manifest.json").read_text(encoding="utf-8"))["notice"]["zh"]
    structure = (ROOT / "STRUCTURE.md").read_text(encoding="utf-8")
    errors.extend(claim_problems(preamble, notice, structure))


def check_placeholders() -> None:
    for p in md_files():
        text = p.read_text(encoding="utf-8")
        for token in ("TODO", "TBD", "lorem ipsum", "PLACEHOLDER"):
            if token.lower() in text.lower():
                errors.append(f"{p}: leftover {token}")


def main() -> int:
    check_units()
    check_source_figure_numbers()
    check_ills()
    check_photos()
    check_screenshots()
    check_attiny_pinmap()
    check_led_net_contract()
    check_selection_lock()
    check_breath_firmware()
    check_cli_origin_contract()
    check_round2_contracts()
    check_sources()
    check_cli_claims()
    check_lib_table_examples()
    check_file_header_examples()
    check_trace_width_table()
    check_si_numbers()
    check_power_only_usb()
    check_readme_stats()
    check_artifact_claims()
    check_unverified_claims()
    check_placeholders()
    if errors:
        print("CONTENT CHECK FAILED")
        for e in errors:
            print(" -", e)
        return 1
    print("CONTENT CHECK OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
