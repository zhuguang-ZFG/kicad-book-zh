import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ink import Ink, save  # noqa: E402

# Repo-relative so the script works from any git worktree, not just one checkout.
OUT = Path(__file__).resolve().parents[1] / "yuyu-book" / "illustrations"
MONO = "Noto Serif CJK SC, Songti SC, SimSun, serif"


def box(a, x, y, w, h, label="", sub="", fs=16, dash=None, op=None, r=2):
    a.rect(x, y, w, h, width=2.0, radius=r, dash=dash, opacity=op)
    if label:
        a.text(x + w / 2, y + h / 2 + (0 if not sub else -6), label, size=fs)
    if sub:
        a.text(x + w / 2, y + h / 2 + 13, sub, size=fs - 3, opacity=.55)


def chip(a, x, y, w, h, label="", pins=4, fs=14, side="both"):
    a.rect(x, y, w, h, width=2.0, radius=2)
    a.text(x + w / 2, y + h / 2 + 4, label, size=fs, opacity=.7)
    if side in ("both", "left"):
        for i in range(pins):
            yy = y + 10 + i * (h - 20) / max(pins - 1, 1)
            a.line(x - 12, yy, x, yy, width=1.3)
    if side in ("both", "right"):
        for i in range(pins):
            yy = y + 10 + i * (h - 20) / max(pins - 1, 1)
            a.line(x + w, yy, x + w + 12, yy, width=1.3)


def title(a, x, y, s, size=17, op=.55):
    a.text(x, y, s, size=size, anchor="start", opacity=op)


def cross(a, x, y, s=7, w=2.2):
    a.line(x - s, y - s, x + s, y + s, width=w)
    a.line(x + s, y - s, x - s, y + s, width=w)


def check(a, x, y, s=8, w=2.2):
    a.path(f"M{x-s} {y}l{s*0.7} {s*0.7}L{x+s} {y-s*0.8}", width=w)


def board(a, x, y, w, h, r=6):
    a.rect(x, y, w, h, width=2.4, radius=r)
    for cx, cy in ((x + 8, y + 8), (x + w - 8, y + 8), (x + 8, y + h - 8), (x + w - 8, y + h - 8)):
        a.circle(cx, cy, 3.4, width=1.2)
        a.circle(cx, cy, 1.2, width=.8, opacity=.4)


def fig(name, w, h, fn):
    a = Ink(w, h)
    fn(a)
    save(a, OUT / f"{name}.svg", limit=24000)


# ---- preface ----------------------------------------------------------
def learning_path(a):
    stages = [
        ("入门", "第 1—4 章", "ERC 通过的原理图"),
        ("独立设计", "第 5—9 章", "通过 DRC 的两层板"),
        ("制造验证", "第 10—12 章", "制造文件齐全"),
        ("工程化", "第 13—15 章", "仿真 · 库 · 自动化"),
    ]
    xs = [28, 198, 368, 538]
    ys = [134, 112, 90, 68]
    a.text(360, 35, "从入门到工程化：四个阶段，每一步都有可检查的成果", size=18, opacity=.55)
    for i, (stage, chapters, outcome) in enumerate(stages):
        x, y = xs[i], ys[i]
        a.rect(x, y, 150, 100, width=2.0, radius=5)
        a.circle(x + 18, y + 18, 9, width=1.4, opacity=.65)
        a.text(x + 18, y + 22, str(i + 1), size=10, opacity=.6)
        a.text(x + 86, y + 25, stage, size=14)
        a.text(x + 75, y + 49, chapters, size=11, opacity=.6)
        a.line(x + 12, y + 62, x + 138, y + 62, width=1.0, opacity=.3)
        a.text(x + 75, y + 83, outcome, size=10, opacity=.6)
        if i < 3:
            a.arrow(x + 152, y + 50, xs[i + 1] - 4, ys[i + 1] + 50,
                    width=1.6, head=4)


# ---- chapter 1 ---------------------------------------------------------
def ch01_flow(a):
    a.text(360, 28, "从设计数据到制造交付", size=14, opacity=.7)

    # Schematic sheet with a small electrical intent sketch.
    a.rect(70, 64, 220, 96, width=1.8, radius=3)
    a.line(270, 64, 290, 84, width=1.2, opacity=.6)
    a.line(270, 64, 270, 84, width=1.2, opacity=.6)
    a.line(270, 84, 290, 84, width=1.2, opacity=.6)
    a.text(180, 84, "原理图", size=14)
    a.line(96, 118, 136, 118, width=1.4)
    a.path("M136 118l8-6 8 12 8-12 8 12 8-12 8 6", width=1.4)
    a.line(176, 118, 216, 118, width=1.4)
    a.line(226, 108, 226, 128, width=1.4)
    a.line(232, 108, 232, 128, width=1.4)
    a.line(216, 118, 226, 118, width=1.4)
    a.line(232, 118, 250, 118, width=1.4)
    a.rect(250, 104, 36, 28, width=1.4, radius=2)
    a.text(180, 150, "电气连接 · 器件字段", size=10, opacity=.75)

    # PCB board with copper traces, pads and a device.
    a.rect(430, 64, 220, 96, width=2.0, radius=6)
    for x, y in ((450, 84), (630, 84), (450, 140), (630, 140)):
        a.circle(x, y, 4, width=1.0, opacity=.6)
    a.text(540, 84, "PCB", size=14)
    a.path("M462 108h38v22h44v-18h34", width=1.3, opacity=.7)
    a.path("M462 128h44v-18h38v18h34", width=1.3, opacity=.7)
    a.rect(516, 100, 48, 40, width=1.6, radius=2)
    for x in (506, 574):
        for y in (108, 120, 132):
            a.rect(x - 3, y - 2, 6, 4, width=.8, opacity=.6)
    a.text(540, 152, "封装 · 板框 · 铜与规则", size=10, opacity=.75)

    a.arrow(294, 112, 426, 112, width=1.8, head=5)
    a.text(360, 102, "同步", size=10, opacity=.75)

    # Outputs sit directly under their source document.
    a.arrow(180, 164, 180, 190, width=1.4, head=4)
    a.text(196, 181, "生成", size=9.5, anchor="start", opacity=.75)
    a.arrow(540, 164, 540, 190, width=1.4, head=4)
    a.text(556, 181, "导出", size=9.5, anchor="start", opacity=.75)

    a.rect(120, 196, 160, 56, width=1.6, radius=3)
    a.rect(170, 190, 60, 10, width=1.2, radius=2)
    a.text(200, 214, "BOM", size=12)
    a.line(132, 224, 268, 224, width=.8, opacity=.4)
    a.text(200, 246, "Ref · Value · MPN", size=8.5, opacity=.75)

    a.path("M390 212V202h48l12 10h150", width=1.6)
    a.rect(390, 212, 210, 40, width=1.6, radius=2)
    a.text(495, 228, "制造数据", size=12)
    a.text(430, 244, "Gerber", size=9, opacity=.75)
    a.text(495, 244, "Drill", size=9, opacity=.75)
    a.text(560, 244, "POS", size=9, opacity=.75)

    # Side drawers supply object definitions to both design documents.
    a.rect(16, 196, 88, 56, width=1.4, radius=2)
    a.line(24, 224, 96, 224, width=1.0, opacity=.5)
    a.text(60, 216, "符号库", size=10, opacity=.75)
    a.text(60, 240, "对象定义", size=8.5, opacity=.75)
    a.rect(616, 196, 88, 56, width=1.4, radius=2)
    a.line(624, 224, 696, 224, width=1.0, opacity=.5)
    a.text(660, 216, "封装库", size=10, opacity=.75)
    a.text(660, 240, "对象定义", size=8.5, opacity=.75)
    a.arrow(60, 196, 110, 160, width=1.2, head=4)
    a.arrow(660, 196, 610, 160, width=1.2, head=4)

    a.text(360, 330, "库提供对象定义；同步、导出后仍须核对规则、装配范围与工厂模板。", size=11, opacity=.7)


def ch01_toolmap(a):
    a.circle(360, 150, 60, width=2.0)
    a.text(360, 145, "KiCad", size=22)
    a.text(360, 168, "项目管理器", size=12, opacity=.6)
    sats = [("原理图编辑器", 120, 60), ("符号编辑器", 600, 60), ("PCB 编辑器", 120, 240),
            ("封装编辑器", 600, 240), ("Gerber 查看器", 50, 150), ("PCB 计算器", 670, 150)]
    for lab, x, y in sats:
        box(a, x - 64, y - 24, 128, 48, lab, fs=13)
        a.line(360 + (x - 360) * .28, 150 + (y - 150) * .28, x, y, width=1.5, opacity=.6)
    a.text(360, 285, "同一套库，同一套工程；编辑器只是不同的“窗口”。", size=13, opacity=.5)


# ---- chapter 2 ---------------------------------------------------------
def ch02_symbol(a):
    a.rect(220, 70, 280, 140, width=2.4, radius=4)
    a.text(360, 112, "U1", size=22)
    a.text(360, 140, "ATtiny85-20SU", size=14, opacity=.65)
    a.text(360, 172, "SOIC-8", size=12, opacity=.5)
    for i, lab in enumerate(("RESET", "PB3", "PB4", "GND")):
        y = 92 + i * 30
        a.line(196, y, 220, y, width=1.8)
        a.circle(220, y, 2.0, width=1.0)
        a.text(206, y - 6, str(i + 1), size=10, opacity=.55)
        a.text(232, y + 4, lab, size=12, anchor="start", opacity=.7)
    for i, lab in enumerate(("PB0/MOSI", "PB1/MISO", "PB2/SCK", "VCC")):
        y = 92 + i * 30
        a.line(500, y, 524, y, width=1.8)
        a.circle(500, y, 2.0, width=1.0)
        a.text(514, y - 6, str(5 + i), size=10, opacity=.55)
        a.text(488, y + 4, lab, size=12, anchor="end", opacity=.7)
    a.line(360, 210, 360, 240, width=1.2, opacity=.4, dash="2 4")
    a.text(360, 256, "符号是电气意图；封装是物理焊盘。两者靠编号对应。", size=13, opacity=.55)


def ch02_net(a):
    # three panels
    for x, lab in ((24, "A · 导线"), (256, "B · 网络标签"), (488, "C · 电源符号")):
        a.rect(x, 42, 208, 196, width=1.0, opacity=.3, radius=3)
        a.text(x + 104, 64, lab, size=14, opacity=.6)
    # A wire
    a.line(60, 130, 140, 130, width=2.4)
    a.line(140, 130, 140, 180, width=2.4)
    a.line(140, 130, 200, 130, width=2.4)
    a.circle(140, 130, 3.0, width=1.2, fill="currentColor")
    a.text(100, 120, "导线", size=12, opacity=.55)
    a.text(148, 170, "T 形连接", size=11, opacity=.5)
    # B labels
    a.line(292, 130, 340, 130, width=2.2)
    a.text(340, 125, "SDA", size=13, anchor="start")
    a.line(432, 130, 480, 130, width=2.2)
    a.text(432, 125, "SDA", size=13, anchor="end")
    a.line(386, 110, 386, 150, width=1.0, opacity=.35, dash="2 4")
    a.text(386, 170, "同名即同网", size=11, opacity=.5)
    # C power
    a.line(524, 150, 560, 150, width=2.2)
    a.line(560, 130, 560, 170, width=2.0)
    a.line(552, 130, 568, 130, width=2.0)
    a.text(560, 118, "VCC", size=13)
    a.line(600, 150, 636, 150, width=2.2)
    a.line(612, 150, 612, 168, width=2.0)
    a.line(604, 168, 620, 168, width=2.0)
    a.line(608, 174, 616, 174, width=2.0)
    a.text(612, 192, "GND", size=13)
    a.text(360, 262, "同名网络标签和电源符号，都是“按名字连接”，不靠画线。", size=13, opacity=.55)


# ---- chapter 3 ---------------------------------------------------------
def ch03_erc(a):
    a.circle(360, 140, 78, width=1.4, opacity=.35, dash="3 7")
    steps = [("画原理图", 360, 42), ("跑 ERC", 475, 140), ("读报告", 360, 238), ("修正", 245, 140)]
    for lab, x, y in steps:
        box(a, x - 58, y - 24, 116, 48, lab, fs=14)
    a.arrow(400, 60, 447, 112, width=1.8)
    a.arrow(495, 164, 430, 218, width=1.8)
    a.arrow(320, 218, 276, 164, width=1.8)
    a.arrow(276, 112, 320, 62, width=1.8)
    a.text(360, 148, "0 errors", size=17, opacity=.75)
    a.text(360, 170, "0 warnings", size=13, opacity=.5)
    a.text(360, 288, "ERC 不是“找茬”，是把设计意图写成机器能核对的约束。", size=13, opacity=.55)


def ch03_hier(a):
    box(a, 270, 34, 180, 54, "根图纸 root", fs=15)
    subs = [("power", 84, 160), ("mcu", 286, 160), ("io", 488, 160)]
    for lab, x, y in subs:
        box(a, x, y, 148, 58, lab, fs=15)
        a.line(x + 74, y, 360, 88, width=1.6)
    for x, lab in ((158, "5V / GND"), (360, "SPI / I2C"), (562, "LED / BTN")):
        a.text(x, 246, lab, size=11, opacity=.5)
    a.text(360, 286, "层次图把一张大图拆成可复用的页；页脚标签就是页与页之间的“插头”。", size=13, opacity=.55)


# ---- chapter 4 ---------------------------------------------------------
def ch04_map(a):
    a.rect(40, 54, 220, 160, width=1.0, opacity=.3, radius=3)
    a.text(150, 78, "符号 U1", size=14, opacity=.6)
    a.rect(90, 100, 120, 90, width=2.0, radius=2)
    for i in range(4):
        y = 112 + i * 20
        a.line(70, y, 90, y, width=1.4); a.text(78, y - 5, str(i + 1), size=9, opacity=.5)
        a.line(210, y, 230, y, width=1.4); a.text(216, y - 5, str(8 - i), size=9, opacity=.5)
    a.text(150, 150, "U1", size=15)
    # footprint
    a.rect(460, 54, 220, 160, width=1.0, opacity=.3, radius=3)
    a.text(570, 78, "封装 SOIC-8", size=14, opacity=.6)
    a.rect(500, 104, 140, 82, width=1.4, opacity=.5, radius=2)
    for i in range(4):
        y = 112 + i * 20
        a.rect(480, y - 4, 20, 10, width=1.4, radius=1)
        a.rect(640, y - 4, 20, 10, width=1.4, radius=1)
        a.text(490, y + 3, str(i + 1), size=8, opacity=.5)
        a.text(650, y + 3, str(8 - i), size=8, opacity=.5)
    # mapping lines
    for i in range(4):
        y1 = 112 + i * 20
        a.line(230, y1, 480, y1, width=1.0, opacity=.25, dash="2 5")
    a.text(360, 250, "引脚号是唯一契约：符号的 pin number 对上封装的 pad number，电气才落到铜上。", size=12, opacity=.55)


def ch04_bom(a):
    a.text(40, 42, "符号字段", size=15, anchor="start", opacity=.6)
    rows = [("Reference", "U1"), ("Value", "ATtiny85-20SU"), ("Footprint", "SOIC-8"), ("MPN", "ATTINY85-20SU"), ("Qty", "1")]
    for i, (k, v) in enumerate(rows):
        y = 60 + i * 34
        a.rect(40, y, 160, 28, width=1.2, radius=1)
        a.text(50, y + 19, k, size=11, anchor="start", opacity=.65)
        a.rect(200, y, 190, 28, width=1.2, radius=1)
        a.text(210, y + 19, v, size=11, anchor="start")
    a.arrow(410, 140, 470, 140, width=2.0)
    a.text(440, 128, "导出", size=10, opacity=.5)
    # BOM table
    a.rect(490, 54, 200, 190, width=1.4, radius=2)
    heads = ("Ref", "Value", "Qty")
    for i, h in enumerate(heads):
        a.text(510 + i * 62, 76, h, size=10, opacity=.55, anchor="start")
    for r in range(4):
        y = 96 + r * 32
        a.line(500, y, 680, y, width=.8, opacity=.25)
        a.text(510, y + 18, ("U1", "C1", "R1", "J1")[r], size=10, anchor="start")
        a.text(572, y + 18, ("MCU", "100n", "10k", "USB-C")[r], size=10, anchor="start")
        a.text(650, y + 18, "1", size=10, anchor="start")
    a.text(360, 278, "BOM 不是“零件清单”，而是采购、贴片和追溯共用的同一张事实表。", size=12, opacity=.55)


def ch04_audit(a):
    a.text(360, 26, "SOIC-8 封装核对卡", size=15, opacity=.78)
    a.path("M24 44H342Q346 44 346 48V238Q346 242 342 242H24Q20 242 20 238V48Q20 44 24 44Z",
           width=1.2, opacity=.4)
    a.path("M366 44H684Q688 44 688 48V238Q688 242 684 242H366Q362 242 362 238V48Q362 44 366 44Z",
           width=1.2, opacity=.4)
    a.circle(47, 64, 8, width=1.3)
    a.text(47, 68, "1", size=9)
    a.text(62, 68, "方向与编号", size=12, anchor="start", opacity=.78)
    a.circle(389, 64, 8, width=1.3)
    a.text(389, 68, "2", size=9)
    a.text(404, 68, "尺寸与边界", size=12, anchor="start", opacity=.78)

    # Top view rotated so pin 1 is at the upper right, matching the caption.
    a.rect(94, 104, 154, 84, width=2.0, radius=3)
    a.text(171, 151, "SOIC-8", size=13, opacity=.8)
    for i in range(4):
        x = 108 + i * 38
        a.rect(x, 90, 26, 14, width=1.6, radius=2)
        a.rect(x, 188, 26, 14, width=1.6, radius=2)
        a.text(x + 13, 84, str(4 - i), size=11, opacity=.8)
        a.text(x + 13, 218, str(5 + i), size=11, opacity=.8)
    a.dot(238, 113, 3)
    a.line(242, 110, 264, 94, width=1.1, opacity=.7)
    a.text(270, 94, "pin 1", size=10, anchor="start", opacity=.8)
    a.path("M248 78H104Q94 78 94 88V194Q94 204 104 204H248V78",
           width=1.0, opacity=.55, dash="4 5")
    a.line(248, 78, 243, 85, width=1.0)
    a.line(248, 78, 253, 85, width=1.0)
    a.text(171, 239, "从 pin 1 逆时针核对 1 → 8", size=10, opacity=.78)

    # Side cross-section: direct leaders tie each check to the geometry.
    a.rect(404, 178, 224, 18, width=1.6, opacity=.75, radius=2)
    a.text(516, 191, "PCB", size=10, opacity=.8)
    a.rect(458, 104, 116, 62, width=2.0, radius=3)
    a.text(516, 140, "本体", size=11, opacity=.8)
    a.poly([(458, 140), (436, 140), (436, 178)], width=1.8)
    a.poly([(574, 140), (596, 140), (596, 178)], width=1.8)
    a.rect(428, 174, 20, 10, width=1.4, radius=2)
    a.rect(584, 174, 20, 10, width=1.4, radius=2)
    a.rect(412, 88, 220, 118, width=1.2, dash="4 5", opacity=.6, radius=2)
    a.text(380, 132, "引脚", size=9.5, anchor="start", opacity=.8)
    a.line(405, 129, 436, 140, width=1.0, opacity=.7)
    a.dot(436, 140, 1.8)
    a.text(380, 170, "焊盘", size=9.5, anchor="start", opacity=.8)
    a.line(405, 167, 438, 179, width=1.0, opacity=.7)
    a.dot(438, 179, 1.8)
    a.text(650, 104, "courtyard", size=9.5, opacity=.8)
    a.text(650, 121, "允许占用边界", size=9, opacity=.8)
    a.line(622, 95, 642, 101, width=1.0, opacity=.7)
    a.text(650, 158, "3.9 × 4.9 mm", size=9.5, opacity=.8)
    a.line(574, 112, 620, 136, width=1.0, opacity=.7)
    a.text(650, 184, "P1.27 mm", size=9.5, opacity=.8)

    checks = (("1", "方向", "pin 1 与丝印同向"),
              ("2", "编号", "1→8 逐脚核对"),
              ("3", "尺寸", "3.9×4.9 / P1.27"),
              ("4", "边界", "courtyard 不压邻居"))
    for i, (num, label, sub) in enumerate(checks):
        x = 20 + i * 172
        a.rect(x, 256, 160, 44, width=1.2, opacity=.55, radius=3)
        a.circle(x + 17, 278, 9, width=1.3)
        a.text(x + 17, 282, num, size=10)
        a.text(x + 33, 274, label, size=11, anchor="start", opacity=.8)
        a.text(x + 33, 291, sub, size=9.5, anchor="start", opacity=.78)


# ---- chapter 5 ---------------------------------------------------------
def ch05_stack(a):
    def stack(x, layers, lab):
        a.text(x + 130, 38, lab, size=15, opacity=.6)
        total = 180
        h = total / len(layers)
        for i, (name, kind) in enumerate(layers):
            y = 54 + i * h
            if kind == "cu":
                a.rect(x, y, 260, h, width=1.6, opacity=.9)
                a.hatch(x, y, 260, h, step=8, opacity=.15)
            elif kind == "core":
                a.rect(x, y, 260, h, width=1.2, opacity=.55)
            else:
                a.rect(x, y, 260, h, width=1.0, opacity=.35, dash="2 4")
            a.text(x + 130, y + h / 2 + 4, name, size=10, opacity=.6)
    stack(40, [("F.Cu", "cu"), ("FR-4 core", "core"), ("B.Cu", "cu")], "2 层 · 1.6 mm")
    stack(390, [("F.Cu", "cu"), ("prepreg", "pre"), ("In1.Cu · GND", "cu"),
                ("core", "core"), ("In2.Cu · PWR", "cu"), ("prepreg", "pre"), ("B.Cu", "cu")], "4 层 · 1.6 mm")
    a.text(360, 262, "层数不是“更高级”，而是为回流路径、阻抗和布线密度付费。", size=12, opacity=.55)


def ch05_netclass(a):
    cards = [("Default", "0.20 mm", "0.20 mm"), ("Power", "0.50 mm", "0.25 mm"), ("USB*", "0.25 mm", "0.20 mm")]
    for i, (name, w, cl) in enumerate(cards):
        x = 34 + i * 220
        a.rect(x, 46, 196, 120, width=1.6, radius=3)
        a.text(x + 98, 76, name, size=16)
        a.text(x + 98, 108, f"线宽 {w}", size=11, opacity=.6)
        a.text(x + 98, 130, f"间距 {cl}", size=11, opacity=.6)
        if name == "USB*":
            a.text(x + 98, 153, "仅数据版", size=8, opacity=.5)
    # board strip
    a.rect(34, 190, 620, 52, width=1.6, radius=3)
    for i, w in enumerate((1.6, 2.4, 5.0)):
        y = 204 + i * 14
        a.line(50, y, 300 + i * 80, y, width=w, opacity=.75)
    a.text(360, 268, "基线用 Default / Power；USB* 仅数据版。", size=12, opacity=.55)


def ch05_rule_floor(a):
    a.text(360, 30, "规则从具体到通用，都不能穿过硬下限", size=15, opacity=.55)
    a.rect(80, 216, 560, 38, width=2.2, radius=3)
    a.text(360, 241, "板级 Constraints：最小值是硬下限", size=14)
    for x, title, sub in ((110, "网类", "线宽 / 过孔 / 间距的规则值"),
                          (400, "自定义规则", "例外 / 区域 / 条件")):
        a.rect(x, 104, 210, 72, width=1.6, radius=3)
        a.text(x + 105, 132, title, size=15)
        a.text(x + 105, 155, sub, size=10, opacity=.55)
        a.arrow(x + 105, 178, x + 105, 212, width=1.5, head=5)
        a.text(x + 115, 198, "不能突破", size=9, anchor="start", opacity=.5)
    a.text(360, 80, "网类给规则值；自定义规则处理例外", size=11, opacity=.55)


# ---- chapter 6 ---------------------------------------------------------
def ch06_floor(a):
    board(a, 84, 48, 552, 202, r=8)
    # Relative placement concept for the book's USB-C power-only teaching board.
    box(a, 94, 101, 70, 82, "USB-C", "J1", fs=12, r=5)
    box(a, 181, 77, 105, 58, "入口保护", "保险丝 / TVS", fs=12, r=5)
    box(a, 181, 155, 105, 64, "LDO", "+5V → +3V3", fs=13, r=5)
    box(a, 331, 77, 110, 77, "ATtiny85", "MCU", fs=13, r=5)
    box(a, 316, 172, 140, 47, "去耦 / RESET", fs=11, r=5)
    box(a, 481, 77, 140, 58, "LED / 按键", "用户接口", fs=12, r=5)
    box(a, 481, 164, 140, 55, "ISP / 测试点", fs=12, r=5)
    a.arrow(166, 120, 177, 108, width=1.5, head=3)
    a.arrow(233, 139, 233, 151, width=1.5, head=3)
    a.arrow(289, 182, 326, 146, width=1.5, head=3)
    a.arrow(445, 115, 477, 106, width=1.5, head=3)
    a.arrow(399, 158, 450, 181, width=1.5, head=3)
    a.text(360, 276, "按连接器、外壳与电流回路定位置；箭头仅表示相邻功能关系。", size=12, opacity=.55)


def ch06_decouple(a):
    # Same MCU pinout and same 100 nF capacitor in both concept diagrams.
    a.text(170, 38, "靠近 VCC / GND 引脚", size=14, opacity=.62)
    chip(a, 72, 80, 108, 100, "MCU", pins=3, fs=13, side="right")
    a.text(190, 81, "VCC pin", size=9, anchor="start", opacity=.62)
    a.text(190, 186, "GND pin", size=9, anchor="start", opacity=.62)
    a.line(180, 90, 220, 90, width=1.5)
    a.line(220, 90, 220, 127, width=1.5)
    a.line(210, 127, 230, 127, width=1.5, amp=.1)
    a.line(210, 138, 230, 138, width=1.5, amp=.1)
    a.line(220, 138, 220, 170, width=1.5)
    a.line(220, 170, 180, 170, width=1.5)
    a.text(235, 136, "100 nF", size=9, anchor="start", opacity=.62)

    a.text(540, 38, "远离 VCC / GND 引脚", size=14, opacity=.62)
    chip(a, 400, 80, 108, 100, "MCU", pins=3, fs=13, side="right")
    a.text(518, 104, "VCC", size=10, anchor="start")
    a.text(518, 154, "GND", size=10, anchor="start")
    a.line(508, 90, 650, 90, width=1.5)
    a.line(650, 90, 650, 150, width=1.5)
    a.line(640, 150, 660, 150, width=1.5, amp=.1)
    a.line(640, 161, 660, 161, width=1.5, amp=.1)
    a.line(650, 161, 650, 226, width=1.5)
    a.line(650, 226, 508, 226, width=1.5)
    a.line(508, 226, 508, 170, width=1.5)
    a.text(665, 158, "100 nF", size=9, opacity=.62, anchor="start")
    a.text(360, 266, "同一电容值；减小 VCC—电容—GND 回路面积，才能降低连接寄生电感。", size=12, opacity=.55)


# ---- chapter 7 ---------------------------------------------------------
def ch07_route(a):
    # 90 degree
    a.text(170, 40, "90° · 阻抗突变", size=14, opacity=.6)
    a.line(70, 110, 170, 110, width=4.0)
    a.line(170, 110, 170, 190, width=4.0)
    a.line(170, 190, 260, 190, width=4.0)
    cross(a, 170, 110, 10, 2.0)
    # 45 degree
    a.text(530, 40, "45° · 连续过渡", size=14, opacity=.6)
    a.line(390, 110, 470, 110, width=4.0)
    a.line(470, 110, 500, 140, width=4.0)
    a.line(500, 140, 500, 160, width=4.0)
    a.line(500, 160, 530, 190, width=4.0)
    a.line(530, 190, 620, 190, width=4.0)
    check(a, 500, 140, 9, 2.2)
    a.text(360, 258, "高速信号怕的不是“拐弯”，而是拐弯处突然改变线宽与参考面。", size=12, opacity=.55)


def ch07_highspeed_gate(a):
    """One 30 mm trace, three edge times: where the lumped model stops working.

    Thresholds are TD > 0.2*RT with 6.7 ps/mm on FR4, so
    L = 0.2*RT/6.7ps. 20 ns -> 600 mm, 2 ns -> 60 mm, 0.1 ns -> 3 mm.
    """
    x0, x1 = 168, 660
    def lx(mm):
        return x0 + (math.log10(mm) / 3) * (x1 - x0)

    a.text(360, 26, "同一条 30 mm 走线，三种边沿时间", size=17, opacity=.55)
    a.text(168, 50, "横轴：走线长度（对数刻度）", size=11, anchor="start", opacity=.5)

    # decade ticks
    for mm in (1, 10, 100, 1000):
        x = lx(mm)
        a.line(x, 66, x, 268, width=.8, dash="3 6", opacity=.22)
        a.text(x, 288, f"{mm} mm", size=10, opacity=.5)

    rows = [("RT = 20 ns", 600, "本板量级"),
            ("RT = 2 ns", 60, "加晶振/串口"),
            ("RT = 0.1 ns", 3, "高速链路")]
    for i, (label, thr, note) in enumerate(rows):
        y = 100 + i * 62
        a.text(158, y + 4, label, size=12, anchor="end")
        a.text(158, y + 20, note, size=9, anchor="end", opacity=.45)
        a.line(lx(1), y, lx(thr), y, width=3.0)
        a.line(lx(thr), y, lx(1000), y, width=1.4, dash="5 5", opacity=.45)
        a.circle(lx(thr), y, 4.6, width=1.6)
        a.text(lx(thr), y - 12, f"{thr} mm", size=10, opacity=.6)

    # the board's longest trace
    xs = lx(30)
    a.line(xs, 76, xs, 262, width=1.6, opacity=.7)
    a.text(xs + 7, 72, "本板 ≈ 30 mm", size=10, anchor="start", opacity=.65)

    a.text(300, 316, "阈值左侧：可当集总电路", size=10, opacity=.45)
    a.text(556, 316, "阈值右侧：必须当传输线", size=10, opacity=.45)
    a.text(360, 334, "判据 TD > 0.2 × RT，FR4 约 6.7 ps/mm；边沿变快，门限向短走线移动。", size=11, opacity=.5)

def ch07_diff(a):
    a.text(360, 36, "可选扩展：带 USB 数据的版本", size=12, opacity=.55)
    a.rect(40, 54, 120, 60, width=2.0, radius=3)
    a.text(100, 88, "USB-C", size=13)
    a.text(100, 108, "D+ / D-", size=10, opacity=.55)
    a.line(160, 76, 300, 76, width=2.6)
    a.line(160, 96, 300, 96, width=2.6)
    a.path("M300 76L340 96L380 96", width=2.6)
    a.path("M300 96L340 76L380 76", width=2.6)
    a.line(380, 76, 520, 76, width=2.6)
    a.line(380, 96, 520, 96, width=2.6)
    a.rect(520, 58, 120, 58, width=2.0, radius=3)
    a.text(580, 92, "MCU", size=13)
    a.text(250, 62, "等长", size=10, opacity=.5)
    a.line(260, 120, 400, 120, width=1.0, opacity=.3, dash="2 5")
    a.text(360, 142, "差分对 · 90 Ω", size=12, opacity=.6)
    a.line(250, 160, 250, 200, width=1.0, opacity=.3)
    a.line(340, 160, 340, 200, width=1.0, opacity=.3)
    a.line(250, 200, 340, 200, width=1.0, opacity=.3)
    a.text(295, 218, "间距由叠层决定，不靠目测", size=10, opacity=.5)
    a.text(360, 252, "差分对的“等长”是结果，先有连续参考面和恒定间距。", size=12, opacity=.55)


# ---- chapter 8 ---------------------------------------------------------
def ch08_pour(a):
    a.text(360, 28, "GND 铺铜与缝合过孔", size=13, opacity=.55)
    board(a, 80, 44, 560, 200, r=8)
    # zone boundary
    a.path("M100 64Q110 58 122 64L600 64Q620 66 620 84L620 220Q618 232 604 232L110 232Q96 230 96 216L96 80Q96 66 100 64Z", width=1.0, opacity=.35, dash="4 5")
    for y in (96, 124, 152, 180, 208):
        for x in (140, 200, 260, 320, 380, 440, 500, 560):
            a.circle(x, y, 2.0, width=.8, opacity=.55)
            a.circle(x, y, .6, width=.6, fill="currentColor")
    # component + thermal spokes
    a.rect(280, 120, 100, 60, width=2.0, radius=2)
    a.text(330, 156, "MCU", size=13, opacity=.6)
    a.circle(330, 210, 5.0, width=1.4)
    for ang in (0, 90, 180, 270):
        import math
        x1 = 330 + 5 * math.cos(math.radians(ang)); y1 = 210 + 5 * math.sin(math.radians(ang))
        x2 = 330 + 14 * math.cos(math.radians(ang)); y2 = 210 + 14 * math.sin(math.radians(ang))
        a.line(x1, y1, x2, y2, width=1.2)
    # Symbol key: decode the three repeated marks without changing the board.
    a.line(64, 258, 96, 258, width=1.0, dash="3 4", opacity=.55)
    a.text(106, 262, "铺铜边界", size=10, anchor="start", opacity=.6)
    a.circle(286, 258, 2.8, width=.8, opacity=.55)
    a.circle(286, 258, .8, width=.6, fill="currentColor")
    a.text(300, 262, "缝合过孔", size=10, anchor="start", opacity=.6)
    a.circle(470, 258, 4.0, width=1.2)
    a.line(466, 258, 474, 258, width=1.0)
    a.line(470, 254, 470, 262, width=1.0)
    a.text(492, 262, "热焊盘", size=10, anchor="start", opacity=.6)

    a.text(360, 278, "铺铜是“回流路径”，不是“把空白填满”；过孔缝合让地平面真正连成一片。", size=12, opacity=.55)


def ch08_antenna(a):
    a.text(360, 32, "选读：射频模块天线净空示意", size=12, opacity=.55)
    board(a, 100, 44, 520, 200, r=8)
    # module at edge
    a.rect(120, 90, 120, 110, width=2.0, radius=3)
    a.text(180, 150, "ESP32", size=13, opacity=.6)
    # antenna keepout
    a.rect(250, 70, 150, 150, width=1.2, opacity=.4, dash="4 5", radius=2)
    a.text(325, 150, "天线净空", size=13, opacity=.6)
    a.text(325, 170, "no copper / no via", size=9, opacity=.45)
    a.path("M300 110q15-20 30 0t30 0", width=2.0)
    a.line(300, 110, 300, 90, width=1.2, opacity=.5)
    a.line(360, 110, 360, 90, width=1.2, opacity=.5)
    # keepout hatch marks
    for y in range(80, 210, 14):
        a.line(255, y, 395, y, width=.6, opacity=.12)
    a.line(420, 100, 590, 100, width=1.0, opacity=.25, dash="2 5")
    a.text(505, 92, "其余区域可铺地", size=10, opacity=.45)
    a.text(360, 278, "天线不是“放在板边就行”：净空、参考地和外壳，三者一起决定它能不能工作。", size=12, opacity=.55)


def ch08_return_path(a):
    a.text(360, 28, "同样的信号，地平面开槽后要绕路", size=13, opacity=.55)
    board(a, 60, 48, 600, 190, r=8)
    a.path("M110 112L180 112L240 152L430 152L480 112L610 112", width=2.4)
    a.text(120, 100, "信号电流 →", size=10, anchor="start", opacity=.6)
    # B.Cu plane: a short slot in the upper part, continuous copper below it
    for x, w in ((84, 266), (370, 264)):
        a.rect(x, 190, w, 22, width=1.0, opacity=.35)
        a.hatch(x, 190, w, 22, step=7, opacity=.12)
    a.rect(84, 212, 550, 12, width=1.0, opacity=.35)
    a.hatch(84, 212, 550, 12, step=7, opacity=.12)
    a.text(100, 214, "B.Cu GND", size=9, anchor="start", opacity=.55)
    a.text(360, 184, "开槽", size=9)
    a.path("M100 205L330 205L340 218L380 218L390 205L500 205L610 205",
           width=1.6, dash="7 5", opacity=.8)
    a.text(470, 198, "返回电流", size=9, anchor="end", opacity=.6)
    a.text(360, 275, "开槽迫使回流绕过槽端，环路面积随之变大。", size=12, opacity=.55)


# ---- chapter 9 ---------------------------------------------------------
def ch09_drc(a):
    # board with markers
    board(a, 54, 54, 300, 190, r=6)
    for x, y, lab in ((100, 100, "1"), (220, 130, "2"), (160, 200, "3")):
        a.circle(x, y, 12, width=1.4, dash="2 3")
        a.text(x, y + 4, lab, size=11)
    # report panel
    a.rect(390, 54, 280, 190, width=1.4, radius=3)
    a.text(530, 78, "DRC 报告", size=14, opacity=.6)
    rows = [("1", "Clearance", "violation · 0.15 < 0.20"), ("2", "Unconnected Items", "GND"), ("3", "Silkscreen clipped", "by solder mask · J1")]
    for i, (n, kind, detail) in enumerate(rows):
        y = 100 + i * 40
        a.text(410, y, n, size=11)
        a.text(430, y, kind, size=11, anchor="start")
        a.text(430, y + 16, detail, size=9, anchor="start", opacity=.5)
        a.line(400, y + 24, 660, y + 24, width=.6, opacity=.2)
    a.text(360, 280, "DRC 的每一条都要能回答“哪条规则、哪个对象、为什么”。", size=12, opacity=.55)


def ch09_dfm(a):
    # cross-section of pad and mask
    a.line(60, 190, 660, 190, width=3.0)
    a.rect(200, 150, 120, 40, width=1.6)
    a.text(260, 175, "铜焊盘", size=11, opacity=.55)
    a.rect(180, 130, 160, 20, width=1.0, opacity=.35, dash="2 4")
    a.text(260, 118, "阻焊开窗", size=10, opacity=.5)
    a.rect(212, 120, 96, 30, width=1.2)
    a.text(260, 140, "钢网开口", size=9, opacity=.5)
    # annular ring
    a.circle(470, 170, 26, width=1.4)
    a.circle(470, 170, 12, width=1.2)
    a.line(470, 138, 470, 154, width=.8, opacity=.4)
    a.text(470, 210, "环宽 ≥ 0.05 mm", size=10, opacity=.6)
    # silk over pad
    a.rect(540, 140, 70, 40, width=1.6)
    a.line(548, 150, 602, 170, width=1.2, opacity=.5)
    cross(a, 575, 160, 10, 1.8)
    a.text(575, 210, "丝印不要压焊盘", size=10, opacity=.6)
    a.text(360, 254, "DFM 不是“工厂的事”：孔环、阻焊、钢网和丝印都在你的文件里。", size=12, opacity=.55)


def ch09_three_gates(a):
    a.text(360, 27, "三道门都过，才叫“可以发板”", size=15, opacity=.75)
    gates = [("DRC", "规则 · 连通 · 几何", "0 通过 / 5 违规", "只覆盖工程规则"),
             ("电气确认", "接得对 · 值对 · 回流顺", "原理图 / 器件参数走查", "只确认电气正确"),
             ("工厂能力", "线宽 · 环宽 · 阻焊桥", "DFM 表 + 工厂确认", "只覆盖工艺能力")]
    for i, (title, l1, l2, tail) in enumerate(gates):
        x = 35 + i * 230
        cx = x + 95
        a.rect(x, 48, 190, 178, width=1.8, radius=4)
        if i == 0:
            # Board geometry plus a violation marker and a resolved check.
            a.rect(cx - 27, 61, 54, 36, width=1.4, radius=3)
            a.path(f"M{cx-18} 75h18v12h18", width=1.1, opacity=.7)
            cross(a, cx - 10, 88, 5, 1.6)
            check(a, cx + 12, 88, 5, 1.6)
        elif i == 1:
            # A schematic network: resistor, capacitor and checked nodes.
            a.line(cx - 31, 80, cx - 19, 80, width=1.4)
            a.path(f"M{cx-19} 80l5-7 6 14 6-14 6 14 5-7", width=1.4)
            a.line(cx + 9, 80, cx + 18, 80, width=1.4)
            a.line(cx + 18, 71, cx + 18, 89, width=1.4)
            a.line(cx + 23, 71, cx + 23, 89, width=1.4)
            a.line(cx + 23, 80, cx + 31, 80, width=1.4)
            check(a, cx, 62, 5, 1.4)
        else:
            # Annular ring under caliper jaws: a physical process limit.
            a.circle(cx - 7, 80, 18, width=1.4)
            a.circle(cx - 7, 80, 7, width=1.2)
            a.line(cx + 20, 61, cx + 20, 99, width=1.4)
            a.line(cx + 10, 68, cx + 27, 68, width=1.2)
            a.line(cx + 10, 92, cx + 27, 92, width=1.2)
            a.line(cx + 20, 68, cx + 20, 92, width=.8, opacity=.5)
        a.text(cx, 124, title, size=15)
        a.text(cx, 148, l1, size=10, opacity=.75)
        a.line(x + 18, 159, x + 172, 159, width=.8, opacity=.35)
        a.text(cx, 177, "检查证据", size=9, opacity=.75)
        a.text(cx, 196, l2, size=10, opacity=.78)
        a.text(cx, 216, tail, size=9, opacity=.75)
        a.line(cx, 226, cx, 242, width=1.3)
    a.line(130, 242, 590, 242, width=1.3)
    a.arrow(360, 242, 360, 258, width=1.5, head=5)
    a.rect(300, 260, 120, 28, width=1.6, radius=3)
    a.text(360, 279, "才可发板", size=12)


# ---- chapter 10 --------------------------------------------------------
def ch10_pkg(a):
    # Separate the minimum fab package from files used only by assembly or
    # mechanical review; their inclusion depends on the factory and workflow.
    a.text(178, 40, "投板所需", size=14, opacity=.62)
    a.rect(30, 55, 310, 190, width=1.5, radius=4)
    a.text(55, 78, "fab/gerbers/", size=12, anchor="start", opacity=.72)
    for i, lab in enumerate(("F.Cu / B.Cu", "F.Mask / B.Mask", "F.SilkS / B.SilkS", "Edge.Cuts")):
        a.text(58, 96 + i * 22, lab, size=11, anchor="start")
    a.line(48, 187, 322, 187, width=1.0, opacity=.28)
    a.text(55, 209, "钻孔文件 · fab/README.txt", size=11,
           anchor="start")
    a.text(533, 40, "按需加入", size=14, opacity=.62)
    a.rect(378, 55, 310, 190, width=1.5, radius=4)
    for i, lab in enumerate(("POS / CPL + BOM：委托组装", "STEP：结构检查",
                              "IPC-2581 / ODB++：工厂要求")):
        a.text(398, 104 + i * 39, lab, size=11, anchor="start")
    a.text(360, 278, "先按本次板厂 / 组装厂清单核对；可选文件不是每单都要交付。", size=12,
           opacity=.55)


def ch10_handoff(a):
    a.text(360, 28, "从 fab.zip 到工厂验包台", size=15, opacity=.62)
    a.text(150, 55, "你：导出制造包", size=13, opacity=.68)
    a.rect(58, 72, 184, 112, width=2.0, radius=4)
    a.rect(70, 84, 160, 80, width=1.0, opacity=.42, radius=2)
    a.rect(92, 96, 116, 56, width=1.8, radius=3)
    a.line(108, 124, 192, 124, width=1.0, opacity=.5)
    a.line(150, 104, 150, 144, width=1.0, opacity=.5)
    for x, y in ((104, 108), (196, 108), (104, 140), (196, 140)):
        a.circle(x, y, 3, width=1.0)
    a.path("M42 198 L258 198 L236 212 L64 212 Z", width=1.8)
    a.text(150, 235, "同一版本 · 同一原点", size=11, opacity=.55)

    a.path("M286 119 L326 119 L338 131 L380 131 L380 169 L286 169 Z", width=1.8)
    a.text(333, 154, "fab.zip", size=11)
    a.arrow(386, 144, 418, 144, width=2.0, head=7)

    a.text(558, 55, "工厂：解压、叠加、抽查", size=13, opacity=.68)
    for dx, dy in ((14, 10), (7, 5), (0, 0)):
        a.rect(438 + dx, 80 + dy, 138, 92, width=1.0, opacity=.3, radius=3)
    a.rect(438, 80, 138, 92, width=2.0, radius=4)
    a.line(454, 126, 560, 126, width=1.0, opacity=.45)
    a.line(507, 94, 507, 158, width=1.0, opacity=.45)
    for x, y in ((460, 102), (554, 102), (460, 150), (554, 150)):
        a.circle(x, y, 4, width=1.2)
    a.circle(596, 164, 25, width=2.2)
    a.line(576, 183, 556, 204, width=3.0)

    a.circle(660, 91, 18, width=1.8)
    a.path("M642 116 Q660 106 678 116 L692 246 L628 246 Z", width=1.8)
    a.path("M643 132 Q620 139 607 158", width=1.8)
    a.circle(605, 160, 3, width=1.0)
    a.line(410, 278, 700, 278, width=1.8)
    a.rect(430, 207, 126, 62, width=1.2, radius=2)
    for i, lab in enumerate(("版本", "原点", "装配范围")):
        yy = 222 + i * 18
        a.path(f"M442 {yy}l4 4 7-8", width=1.3)
        a.text(462, yy + 4, lab, size=10, anchor="start", opacity=.72)
    a.text(555, 310, "文件能打开，不等于能一起生产", size=12, opacity=.55)


def ch10_cli(a):
    a.rect(40, 44, 640, 200, width=1.8, radius=4)
    a.line(40, 76, 680, 76, width=1.0, opacity=.4)
    a.circle(58, 60, 4, width=1.0); a.circle(74, 60, 4, width=1.0); a.circle(90, 60, 4, width=1.0)
    cmds = ["kicad-cli pcb drc board.kicad_pcb -o drc.rpt",
            "kicad-cli pcb export gerbers board.kicad_pcb -o fab/",
            "kicad-cli pcb export drill board.kicad_pcb -o fab/",
            "kicad-cli pcb export pos board.kicad_pcb -o fab/board-pos.csv"]
    for i, c in enumerate(cmds):
        a.text(60, 108 + i * 30, "> " + c, size=11, anchor="start", opacity=.8 if i < 3 else .6)
    a.text(60, 232, "加 --exit-code-violations：0 = 通过；5 = 有违规", size=9, anchor="start", opacity=.45)
    a.text(360, 278, "把“点菜单”变成可复现的命令，才有资格谈自动化。", size=12, opacity=.55)


# ---- chapter 11 --------------------------------------------------------
def ch11_order(a):
    rows = [("层数", "2 / 4 / 6"), ("板厚", "1.6 mm"), ("铜厚", "1 oz"), ("阻焊", "绿色"), ("表面", "无铅喷锡"), ("最小线宽", "0.15 mm")]
    for i, (k, v) in enumerate(rows):
        y = 54 + i * 32
        a.rect(50, y, 150, 26, width=1.1, radius=1)
        a.text(60, y + 18, k, size=10, anchor="start", opacity=.6)
        a.rect(200, y, 180, 26, width=1.1, radius=1)
        a.text(210, y + 18, v, size=10, anchor="start")
    a.rect(430, 54, 220, 190, width=1.6, radius=3)
    a.text(540, 82, "下单检查", size=14, opacity=.6)
    for i, s in enumerate(("层叠与阻抗", "孔径与槽孔", "阻焊桥", "拼板与工艺边", "首件测试")):
        check(a, 452, 110 + i * 26, 5, 1.8)
        a.text(468, 114 + i * 26, s, size=10, anchor="start", opacity=.7)
    a.text(360, 278, "下单页不是填空题：每一个选项都应在设计文件里有对应证据。", size=12, opacity=.55)


def ch11_assembly(a):
    a.text(360, 24, "组装线：从钢网到检验", size=14, opacity=.7)
    centers = (88, 232, 376, 520, 664)

    def label(x, num, text):
        a.circle(x - 34, 54, 9, width=1.4)
        a.text(x - 34, 58, str(num), size=10)
        a.text(x - 18, 59, text, size=12, anchor="start", opacity=.75)

    def pcb(x):
        a.rect(x - 34, 196, 68, 14, width=1.4, radius=2)

    for x, num, text in zip(centers, range(1, 6), ("钢网", "印刷", "贴片", "回流", "检验")):
        label(x, num, text)
        pcb(x)

    # Stencil frame, openings and squeegee.
    x = centers[0]
    a.rect(x - 42, 86, 84, 74, width=1.8, radius=2)
    for dx in (-24, 0, 24):
        a.rect(x + dx - 6, 106, 12, 10, width=1.0, opacity=.6)
        a.rect(x + dx - 6, 136, 12, 10, width=1.0, opacity=.6)
    a.line(x - 32, 148, x + 30, 110, width=2.2)
    a.rect(x - 10, 150, 20, 8, width=1.4, radius=1)

    # Paste print: blade, handle and fresh paste dots.
    x = centers[1]
    a.line(x - 34, 102, x + 30, 132, width=2.4)
    a.rect(x - 8, 134, 16, 22, width=1.4, radius=2)
    for dx in (-20, 0, 20):
        a.dot(x + dx, 202, 1.8)

    # Pick-and-place gantry, nozzle, component and feeder reel.
    x = centers[2]
    a.rect(x - 44, 86, 88, 16, width=1.8, radius=2)
    a.line(x, 102, x, 148, width=1.6)
    a.rect(x - 10, 148, 20, 12, width=1.4, radius=1)
    a.rect(x - 8, 170, 16, 10, width=1.2, radius=1)
    a.circle(x + 38, 122, 14, width=1.4)
    a.circle(x + 38, 122, 4, width=1.0)
    a.line(x + 24, 122, x + 12, 150, width=1.2)

    # Reflow oven with heat waves and a through-conveyor.
    x = centers[3]
    a.rect(x - 48, 90, 96, 98, width=1.8, radius=3)
    a.rect(x - 38, 106, 76, 66, width=1.0, opacity=.5)
    for dx in (-22, 0, 22):
        a.path(f"M{x+dx} 156q-8-10 0-20t0-20", width=1.2, opacity=.6)
    a.line(x - 58, 198, x + 58, 198, width=2.0)

    # Inspection camera, magnifier and acceptance mark.
    x = centers[4]
    a.rect(x - 30, 86, 60, 16, width=1.8, radius=2)
    a.line(x, 102, x, 136, width=1.6)
    a.circle(x, 148, 18, width=1.6)
    a.line(x + 12, 160, x + 26, 174, width=2.0)
    check(a, x, 202, 7, 1.8)

    # Conveyor and process-record band.
    a.rect(36, 210, 648, 18, width=1.6, radius=2)
    a.arrow(40, 239, 680, 239, width=1.2, head=6)
    a.rect(96, 250, 528, 26, width=1.2, radius=3, opacity=.7)
    a.text(360, 268, "批次 · 钢网 · 锡膏 · 贴片程序 · 回流曲线 · 检验记录", size=10, opacity=.75)
    a.text(360, 292, "手焊和回流不是两件事，而是同一套“热、锡、助焊剂”的不同尺度。", size=11, opacity=.7)


def ch11_ibom(a):
    a.text(360, 30, "InteractiveHtmlBom：把 BOM 和板图放进同一个离线页面", size=15,
           opacity=.62)
    box(a, 24, 70, 176, 72, "PCB 数据", ".kicad_pcb", fs=14)
    box(a, 24, 166, 176, 64, "BOM", "位号 · 值 · 封装", fs=14)
    box(a, 260, 92, 196, 116, "InteractiveHtmlBom", "插件生成自包含 HTML", fs=13)
    box(a, 510, 70, 180, 72, "离线 HTML", "无需联网", fs=14)
    box(a, 510, 166, 180, 64, "装配视图", "高亮 · 勾选 · 对账", fs=14)
    a.arrow(202, 106, 256, 120, width=1.6, head=5)
    a.arrow(202, 198, 256, 180, width=1.6, head=5)
    a.arrow(458, 138, 506, 106, width=1.6, head=5)
    a.arrow(458, 162, 506, 198, width=1.6, head=5)
    a.text(360, 250, "点 BOM 行高亮板位；点封装反查 BOM；可标记已焊。", size=12, opacity=.55)
    a.text(360, 276, "它只读 PCB 数据，不替代 Gerber、坐标或 BOM 本身。", size=11, opacity=.5)


def ch11_kikit(a):
    a.text(360, 30, "KiKit：把单板排成可制造的拼板", size=15, opacity=.62)
    board(a, 40, 92, 110, 68, 4)
    a.text(95, 184, "单板", size=12, opacity=.6)
    a.arrow(154, 126, 220, 126, width=1.8, head=6)
    a.rect(230, 58, 260, 172, width=2.2, radius=4)
    for row in range(2):
        for col in range(2):
            board(a, 250 + col * 112, 78 + row * 72, 96, 56, 4)
    for cx, cy in ((242, 70), (478, 70), (242, 218), (478, 218)):
        a.circle(cx, cy, 3.4, width=1.2)
        a.circle(cx, cy, 1.2, width=.8, opacity=.4)
    a.text(360, 250, "工艺边 + 阵列 + 基准点", size=12, opacity=.6)
    a.text(360, 276, "拼板后重跑 DRC；分板方式与最小间距先问工厂。", size=11, opacity=.5)


# ---- chapter 12 --------------------------------------------------------
def ch12_bringup(a):
    steps = ["目视", "测短路", "限流", "上电", "测轨", "测电流", "时钟", "编程"]
    for i, s in enumerate(steps):
        y = 44 + i * 28
        a.circle(80, y + 10, 9, width=1.2)
        a.text(80, y + 14, str(i + 1), size=9)
        a.text(102, y + 15, s, size=12, anchor="start", opacity=.7)
        if i < len(steps) - 1:
            a.line(80, y + 20, 80, y + 36, width=1.0, opacity=.3)
    a.rect(220, 64, 440, 144, width=1.4, radius=3)
    a.text(440, 92, "上电顺序的原则", size=14, opacity=.6)
    for i, s in enumerate(("先限流，再上电", "先测电压，再测电流", "先看电源，再看时钟", "先能编程，再谈功能")):
        a.text(250, 120 + i * 24, "· " + s, size=11, anchor="start", opacity=.65)
    a.text(360, 262, "第一次上电的目标不是“跑起来”，而是“没有东西在悄悄发热”。", size=12, opacity=.55)


def ch12_debug(a):
    a.rect(230, 40, 260, 52, width=2.0, radius=3)
    a.text(360, 72, "板子不工作", size=15)
    branches = [("不上电", 100, "查电源 / 短路"), ("上电无响应", 360, "查复位 / 时钟"), ("能编程但不跑", 620, "查启动 / 外设")]
    for lab, x, fix in branches:
        a.line(360, 92, x, 132, width=1.4)
        a.rect(x - 82, 132, 164, 48, width=1.4, radius=2)
        a.text(x, 161, lab, size=12)
        a.text(x, 206, fix, size=10, opacity=.55)
    a.text(360, 252, "把“坏”拆成可观察的边界：电源、复位、时钟、启动、外设。", size=12, opacity=.55)


def ch12_power(a):
    a.text(360, 28, "上电后先测这三段，再插 ISP", size=14, opacity=.7)

    # Power chain. Numbered badges link each test point to the measurement rows.
    a.rect(28, 92, 74, 60, width=2.0, radius=4)
    a.text(65, 118, "USB-C", size=11)
    a.text(65, 136, "VBUS/GND", size=10, opacity=.7)
    a.line(102, 122, 166, 122, width=2.0)
    a.circle(166, 122, 5, width=1.4)
    a.line(166, 117, 166, 88, width=1.0, opacity=.5)
    a.circle(166, 78, 9, width=1.4)
    a.text(166, 82, "1", size=10)
    a.text(166, 58, "VBUS", size=11, opacity=.75)

    a.line(171, 122, 188, 122, width=1.8)
    a.rect(188, 108, 58, 28, width=1.8, radius=2)
    a.text(217, 127, "F1", size=12)
    a.line(246, 122, 284, 122, width=2.0)
    a.circle(284, 122, 5, width=1.4)
    a.line(284, 117, 284, 88, width=1.0, opacity=.5)
    a.circle(284, 78, 9, width=1.4)
    a.text(284, 82, "2", size=10)
    a.text(284, 58, "+5V", size=11, opacity=.75)

    a.line(289, 122, 326, 122, width=1.8)
    a.rect(326, 90, 98, 64, width=2.0, radius=3)
    a.text(375, 118, "U2", size=13)
    a.text(375, 138, "LDO", size=10, opacity=.7)
    a.line(424, 122, 464, 122, width=2.0)
    a.circle(464, 122, 5, width=1.4)
    a.line(464, 117, 464, 88, width=1.0, opacity=.5)
    a.circle(464, 78, 9, width=1.4)
    a.text(464, 82, "3", size=10)
    a.text(464, 58, "+3V3", size=11, opacity=.75)

    a.line(469, 122, 514, 122, width=1.8)
    a.rect(514, 90, 156, 64, width=2.0, radius=3)
    a.text(592, 118, "ATtiny85", size=12)
    a.text(592, 138, "+ LED", size=10, opacity=.7)

    # Ground rail and returns.
    a.line(52, 192, 650, 192, width=2.0)
    for x, y0 in ((65, 152), (375, 154), (592, 154)):
        a.line(x, y0, x, 192, width=1.2, opacity=.7)
    a.line(375, 192, 375, 204, width=2.0)
    a.line(359, 204, 391, 204, width=1.6)
    a.line(365, 210, 385, 210, width=1.4)
    a.line(371, 216, 379, 216, width=1.2)
    a.text(401, 208, "GND", size=10, anchor="start", opacity=.7)

    # Hand-drawn meter: black lead returns to GND, red lead visits 1 → 2 → 3.
    a.rect(24, 218, 190, 100, width=1.2, radius=3, opacity=.7)
    a.text(119, 236, "万用表", size=12, opacity=.7)
    a.rect(52, 244, 124, 44, width=1.8, radius=4)
    a.rect(66, 252, 96, 16, width=1.0, radius=1, opacity=.6)
    a.text(114, 265, "V", size=13)
    a.text(154, 265, "DC", size=8, anchor="end", opacity=.7)
    a.circle(146, 276, 7, width=1.2)
    a.line(146, 276, 151, 270, width=1.2)
    a.circle(78, 286, 2.5, width=1.2)
    a.circle(108, 286, 2.5, width=1.2)
    a.line(78, 290, 78, 300, width=1.4)
    a.line(70, 300, 86, 300, width=1.2)
    a.line(73, 305, 83, 305, width=1.0)
    a.line(76, 310, 80, 310, width=.9)
    a.text(96, 307, "黑笔 → GND", size=9.5, anchor="start", opacity=.7)
    a.path("M108 290 L108 298 L220 298 L220 264", width=1.4, opacity=.7)
    a.arrow(220, 264, 238, 264, width=1.4, head=5)
    a.text(229, 254, "红笔", size=9.5, opacity=.7)

    rows = (
        ("1", "VBUS → GND", "≈5 V", "无：查 USB-C / 线缆"),
        ("2", "F1 后 → GND", "≈5 V", "无：查 F1 / 焊点"),
        ("3", "+3V3 → GND", "3.3 V", "无：查 LDO / EN / 负载"),
    )
    for i, (num, lab, val, hint) in enumerate(rows):
        y = 218 + i * 34
        a.rect(240, y, 452, 32, width=1.0, radius=2, opacity=.55)
        a.circle(258, y + 16, 8, width=1.2)
        a.text(258, y + 20, num, size=10)
        a.text(278, y + 13, lab, size=11, anchor="start", opacity=.75)
        a.text(452, y + 16, val, size=16, anchor="start", opacity=.85)
        a.text(278, y + 29, hint, size=9.5, anchor="start", opacity=.7)

    a.text(360, 332, "黑笔固定 GND，红笔逐点；先断电再换档。", size=11, opacity=.7)


# ---- chapter 13 --------------------------------------------------------
def rc_rise_path(x0, y0, width, height, duration_tau=5, samples=80):
    """Sample the exact first-order RC step response for an illustrative curve."""
    points = []
    for i in range(samples + 1):
        ratio = i / samples
        t_tau = duration_tau * ratio
        x = x0 + width * ratio
        y = y0 - height * (1 - math.exp(-t_tau))
        points.append((x, y))

    def fmt(value):
        return f"{value:.2f}".rstrip("0").rstrip(".")

    return "M" + "L".join(f"{fmt(x)} {fmt(y)}" for x, y in points)


def ch13_sim(a):
    # First-order RC low-pass: pulse source -> R -> Vout; C and source return to GND.
    a.circle(75, 128, 18, width=2.0)
    a.text(75, 125, "+", size=9)
    a.text(75, 141, "−", size=9)
    a.text(43, 122, "V1", size=9, anchor="end")
    a.text(43, 140, "VPULSE", size=8, anchor="end")
    a.line(75, 110, 75, 94, width=1.8)
    a.line(75, 94, 132, 94, width=1.8)
    a.poly([(132, 94), (142, 80), (152, 108), (162, 80),
            (172, 108), (182, 80), (192, 94)], width=1.8)
    a.text(162, 76, "R", size=10)
    a.line(192, 94, 270, 94, width=1.8)
    a.dot(270, 94, 2.8)
    a.text(270, 82, "Vout", size=10)
    a.line(270, 94, 270, 123, width=1.8)
    a.line(254, 123, 286, 123, width=2.0)
    a.line(254, 137, 286, 137, width=2.0)
    a.line(270, 137, 270, 178, width=1.8)
    a.line(75, 146, 75, 178, width=1.8)
    a.line(75, 178, 270, 178, width=1.8)
    a.line(270, 178, 270, 190, width=1.8)
    a.line(258, 190, 282, 190, width=1.6)
    a.line(263, 196, 277, 196, width=1.4)
    a.line(267, 202, 273, 202, width=1.2)
    a.text(286, 198, "GND", size=9, anchor="start", opacity=.6)

    # Monotonic response of the output voltage to a 0 -> 3.3 V step.
    a.rect(385, 64, 282, 151, width=1.2, radius=2)
    x0, x1, y0 = 415, 645, 178
    response_height = 82
    a.text(416, 55, "Vout", size=10, anchor="start", opacity=.65)
    a.text(645, 55, "TRAN", size=10, anchor="end", opacity=.55)
    a.line(x0, 84, x0, y0, width=1.0, opacity=.35)
    a.line(x0, y0, x1, y0, width=1.0, opacity=.35)
    a.line(x0, y0 - response_height, x1, y0 - response_height,
           width=1.0, opacity=.25, dash="2 4")
    a.text(410, y0 - response_height + 3, "3.3 V", size=8,
           anchor="end", opacity=.55)
    a.path(rc_rise_path(x0, y0, x1 - x0, response_height), width=1.8)
    for t_tau, label in ((1, "τ"), (3, "3τ"), (5, "5τ")):
        ratio = t_tau / 5
        x = x0 + (x1 - x0) * ratio
        y = y0 - response_height * (1 - math.exp(-t_tau))
        a.line(x, y, x, y0, width=1.0, opacity=.28, dash="2 4")
        a.dot(x, y, 2.0)
        a.line(x, y0, x, y0 + 5, width=1.0, opacity=.4)
        a.text(x, y0 + 17, label, size=9, opacity=.55)
    a.text(530, 230, "对 0 → 3.3 V 阶跃的输出响应", size=10, opacity=.55)
    a.text(360, 280, "仿真回答的是模型与拓扑问题；PCB 铜皮、过孔和回流几何需另行验证。", size=11, opacity=.55)


def ch13_wave(a):
    x0, x1, y0 = 70, 660, 190
    response_height = 110
    a.line(x0, y0, x1, y0, width=1.6)
    a.line(x0, 190, x0, 60, width=1.6)
    a.text(360, 43, "Vout(t) = 3.3 V × (1 - e^(-t/τ))", size=13, opacity=.65)
    a.line(x0, y0 - response_height, x1, y0 - response_height,
           width=1.0, opacity=.22, dash="2 4")
    a.text(654, y0 - response_height - 7, "3.3 V", size=9,
           anchor="end", opacity=.5)
    a.path(rc_rise_path(x0, y0, x1 - x0, response_height), width=2.2)

    for i in range(6):
        x = x0 + (x1 - x0) * i / 5
        a.line(x, y0, x, y0 + 7, width=1.0, opacity=.4)
        a.text(x, 214, "0" if i == 0 else ("τ" if i == 1 else f"{i}τ"),
               size=10, opacity=.55)

    for t_tau, pct in ((1, "63.2%"), (3, "95.0%"), (5, "99.3%")):
        ratio = t_tau / 5
        x = x0 + (x1 - x0) * ratio
        y = y0 - response_height * (1 - math.exp(-t_tau))
        a.line(x, y, x, y0, width=1.0, opacity=.25, dash="2 4")
        a.dot(x, y, 2.6)
        if t_tau == 1:
            a.text(x + 10, y + 21, pct, size=9, anchor="start", opacity=.55)
        elif t_tau == 3:
            a.text(x + 10, y + 21, pct, size=9, anchor="start", opacity=.55)
        else:
            a.text(x - 8, y + 21, pct, size=9, anchor="end", opacity=.55)
    a.text(360, 242, "时间常数 τ = R × C：响应按指数趋近终值。", size=12, opacity=.55)


# ---- chapter 14 --------------------------------------------------------
def ch14_library(a):
    cards = [("符号", 60, "U1 · 8 pin"), ("封装", 280, "SOIC-8 · 1.27 mm"), ("3D", 500, "STEP · 本体")]
    for lab, x, sub in cards:
        a.rect(x, 54, 160, 140, width=1.6, radius=3)
        a.text(x + 80, 92, lab, size=18, opacity=.7)
        a.text(x + 80, 120, sub, size=10, opacity=.5)
    a.arrow(220, 124, 280, 124, width=1.6)
    a.arrow(440, 124, 500, 124, width=1.6)
    a.text(360, 224, "同一个器件名贯穿三件套：符号、封装、3D 模型", size=13, opacity=.6)
    a.text(360, 258, "库不是“找得到就行”：命名、引脚、 courtyard 和版本都要能被团队复核。", size=12, opacity=.55)


def ch14_git(a):
    a.line(70, 140, 650, 140, width=2.0)
    for i, x in enumerate((120, 220, 320, 420, 520, 620)):
        a.circle(x, 140, 8, width=1.4)
        a.text(x, 168, f"v{i}", size=9, opacity=.5)
    a.circle(320, 140, 3.0, width=1.0, fill="currentColor")
    a.text(320, 108, "review", size=9, opacity=.55)
    a.text(420, 108, "tag", size=9, opacity=.55)
    a.line(420, 120, 420, 132, width=1.0, opacity=.4)
    a.text(120, 216, "文本格式", size=12, opacity=.6)
    a.text(120, 238, "可 diff / 可合并", size=10, opacity=.45)
    a.text(620, 216, "标签", size=12, opacity=.6)
    a.text(620, 238, "可回滚", size=10, opacity=.45)
    a.text(360, 278, "原理图和 PCB 都是文本：版本控制不是额外工作，是设计的一部分。", size=12, opacity=.55)


# ---- chapter 15 --------------------------------------------------------
def ch15_ci(a):
    steps = [("commit", 20), ("10.0.8", 158), ("ERC/DRC", 296), ("Gerber", 434), ("upload", 572)]
    for i, (lab, x) in enumerate(steps):
        box(a, x, 88, 108, 54, lab, fs=12)
        if i < len(steps) - 1:
            a.arrow(x + 110, 115, steps[i + 1][1] - 2, 115, width=1.6, head=5)
    a.line(212, 144, 212, 178, width=1.3)
    a.line(350, 144, 350, 178, width=1.3)
    a.line(212, 178, 350, 178, width=1.3)
    a.arrow(352, 178, 402, 178, width=1.4, head=4)
    a.rect(408, 158, 224, 40, width=1.4, radius=3)
    a.text(520, 183, "失败：仍上传版本号与报告", size=10, opacity=.65)
    a.text(360, 238, "版本不符或 ERC/DRC 违规会阻断 Gerber；失败报告仍归档。", size=12, opacity=.55)
    a.text(360, 274, "把检查结果与制造文件绑到同一次提交，才可复核。", size=11, opacity=.5)


def ch15_plugin(a):
    a.circle(360, 140, 54, width=2.0)
    a.text(360, 134, "KiCad", size=20)
    a.text(360, 156, "工程", size=10, opacity=.55)
    sats = [("kicad-cli", 120, 64), ("pcbnew Python", 600, 64), ("IPC API", 120, 216), ("PCM 插件", 600, 216)]
    for lab, x, y in sats:
        box(a, x - 78, y - 24, 156, 48, lab, fs=12)
        a.line(360 + (x - 360) * .3, 140 + (y - 140) * .3, x, y, width=1.4, opacity=.6)
    a.text(360, 278, "四条入口，各管一段：命令行管批处理，Python 管板级操作，IPC 管实时会话，PCM 管分发。", size=11, opacity=.55)


def ch15_kibot(a):
    a.text(360, 30, "KiBot：一份 YAML 驱动预检与制造输出", size=15, opacity=.62)
    box(a, 24, 86, 120, 62, "Git 提交", "固定版本", fs=13)
    box(a, 196, 54, 196, 68, "KiBot action", "固定 commit / 镜像", fs=13)
    box(a, 196, 158, 196, 68, ".kibot.yaml", "ERC/DRC + 输出", fs=13)
    box(a, 500, 44, 184, 58, "预检报告", "ERC · DRC", fs=13)
    box(a, 500, 124, 184, 58, "制造输出", "Gerber·Drill·POS·BOM", fs=11)
    box(a, 500, 196, 184, 44, "artifact", "失败也上传", fs=13)
    a.arrow(144, 117, 192, 88, width=1.6, head=5)
    a.arrow(294, 158, 294, 126, width=1.6, head=5)
    a.arrow(392, 88, 496, 64, width=1.6, head=5)
    a.arrow(392, 105, 496, 140, width=1.6, head=5)
    a.arrow(592, 182, 592, 192, width=1.6, head=5)
    a.text(360, 260, "配置、版本、镜像 digest 一起入库；失败报告仍归档。", size=12, opacity=.55)
    a.text(360, 284, "复用上游 action，不等于放弃对输出与许可边界的复核。", size=11, opacity=.5)


figs = {
    "kicad-learning-path": (720, 260, learning_path),
    "kicad-ch01-flow": (720, 340, ch01_flow),
    "kicad-ch01-toolmap": (720, 300, ch01_toolmap),
    "kicad-ch02-symbol-anatomy": (720, 280, ch02_symbol),
    "kicad-ch02-net-label": (720, 280, ch02_net),
    "kicad-ch03-erc-loop": (720, 300, ch03_erc),
    "kicad-ch03-hierarchy": (720, 300, ch03_hier),
    "kicad-ch04-symbol-footprint": (720, 280, ch04_map),
    "kicad-ch04-footprint-audit": (720, 310, ch04_audit),
    "kicad-ch04-bom": (720, 300, ch04_bom),
    "kicad-ch05-stackup": (720, 280, ch05_stack),
    "kicad-ch05-netclass": (720, 280, ch05_netclass),
    "kicad-ch05-rule-floor": (720, 280, ch05_rule_floor),
    "kicad-ch06-floorplan": (720, 300, ch06_floor),
    "kicad-ch06-decouple": (720, 280, ch06_decouple),
    "kicad-ch07-route": (720, 280, ch07_route),
    "kicad-ch07-highspeed-gate": (720, 350, ch07_highspeed_gate),
    "kicad-ch07-diffpair": (720, 280, ch07_diff),
    "kicad-ch08-pour": (720, 300, ch08_pour),
    "kicad-ch08-antenna": (720, 300, ch08_antenna),
    "kicad-ch08-return-path": (720, 300, ch08_return_path),
    "kicad-ch09-drc": (720, 300, ch09_drc),
    "kicad-ch09-dfm": (720, 280, ch09_dfm),
    "kicad-ch09-three-gates": (720, 300, ch09_three_gates),
    "kicad-ch10-fab-package": (720, 300, ch10_pkg),
    "kicad-ch10-handoff": (720, 330, ch10_handoff),
    "kicad-ch10-cli": (720, 300, ch10_cli),
    "kicad-ch11-order": (720, 300, ch11_order),
    "kicad-ch11-assembly": (720, 300, ch11_assembly),
    "kicad-ch11-ibom": (720, 300, ch11_ibom),
    "kicad-ch11-kikit": (720, 300, ch11_kikit),
    "kicad-ch12-bringup": (720, 280, ch12_bringup),
    "kicad-ch12-power": (720, 340, ch12_power),
    "kicad-ch12-debug": (720, 280, ch12_debug),
    "kicad-ch13-sim": (720, 300, ch13_sim),
    "kicad-ch13-wave": (720, 260, ch13_wave),
    "kicad-ch14-library": (720, 280, ch14_library),
    "kicad-ch14-git": (720, 300, ch14_git),
    "kicad-ch15-automation": (720, 280, ch15_ci),
    "kicad-ch15-plugin": (720, 280, ch15_plugin),
    "kicad-ch15-kibot": (720, 300, ch15_kibot),
}
for name, (w, h, fn) in figs.items():
    fig(name, w, h, fn)
print("figures:", len(figs))
