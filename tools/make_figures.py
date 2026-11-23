import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from ink import Ink, save

OUT = Path(r"D:/Users/kkicad/yuyu-book/illustrations")
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
        ("画图", "第 1—4 章", "ERC 通过的原理图"),
        ("设计", "第 5—9 章", "通过 DRC 的两层板"),
        ("制造", "第 10—12 章", "制造文件齐全"),
        ("系统", "第 13—15 章", "仿真 · 库 · 自动化"),
    ]
    xs = [28, 198, 368, 538]
    ys = [134, 112, 90, 68]
    a.text(360, 35, "从入门到工程化：四个阶段，每一步都有可检查的成果", size=18, opacity=.55)
    for i, (stage, chapters, outcome) in enumerate(stages):
        x, y = xs[i], ys[i]
        a.rect(x, y, 150, 100, width=2.0, radius=5)
        a.circle(x + 18, y + 18, 9, width=1.4, opacity=.65)
        a.text(x + 18, y + 22, str(i + 1), size=10, opacity=.6)
        a.text(x + 90, y + 25, stage, size=15)
        a.text(x + 75, y + 49, chapters, size=11, opacity=.6)
        a.line(x + 12, y + 62, x + 138, y + 62, width=1.0, opacity=.3)
        a.text(x + 75, y + 83, outcome, size=10, opacity=.6)
        if i < 3:
            a.arrow(x + 152, y + 50, xs[i + 1] - 4, ys[i + 1] + 50,
                    width=1.6, head=4)


# ---- chapter 1 ---------------------------------------------------------
def ch01_flow(a):
    items = [("工程", ".kicad_pro"), ("原理图", ".kicad_sch"), ("电路板", ".kicad_pcb"),
             ("库", ".kicad_sym / .kicad_mod"), ("制造", "Gerber / Drill")]
    widths = [112, 112, 112, 178, 112]
    xs = [11]
    for width in widths[:-1]:
        xs.append(xs[-1] + width + 18)
    for i, (lab, sub) in enumerate(items):
        box(a, xs[i], 86, widths[i], 86, lab, sub, fs=15)
        if i < 4:
            a.arrow(xs[i] + widths[i] + 1, 129, xs[i + 1] - 2, 129,
                    width=1.8, head=4)
    a.text(360, 46, "一个工程，五种文件，一条链路", size=19, opacity=.55)
    a.line(28, 205, 692, 205, width=1.0, opacity=.25, dash="2 6")
    a.text(360, 228, "源文件是文本；制造文件是投板前最后一次“翻译”。", size=13, opacity=.5)


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
    for x, lab in ((16, "顶视图"), (248, "侧视图"), (480, "核对项")):
        a.rect(x, 36, 224, 226, width=1.0, opacity=.22, radius=3)
        a.text(x + 112, 58, lab, size=13, opacity=.6)

    # top view: body, pads, pin 1, pitch, body width
    a.rect(64, 100, 128, 80, width=2.0, radius=2)
    a.text(128, 145, "SOIC-8", size=10, opacity=.35)
    for i in range(4):
        x = 64 + i * 34
        a.rect(x, 86, 22, 14, width=1.4, radius=1)
        a.rect(x, 180, 22, 14, width=1.4, radius=1)
        a.text(x + 11, 80, str(4 - i), size=10, opacity=.55)
        a.text(x + 11, 208, str(5 + i), size=10, opacity=.55)
    a.dot(180, 112, 2.6)
    a.line(75, 226, 109, 226, width=1.0, opacity=.5)
    a.line(75, 222, 75, 230, width=1.0, opacity=.4)
    a.line(109, 222, 109, 230, width=1.0, opacity=.4)
    a.text(92, 246, "P1.27", size=10, opacity=.55)
    a.line(208, 100, 208, 180, width=1.0, opacity=.5)
    a.line(204, 100, 212, 100, width=1.0, opacity=.4)
    a.line(204, 180, 212, 180, width=1.0, opacity=.4)
    a.text(220, 140, "3.9", size=10, opacity=.55, rotate=90)

    # side view: gull-wing leads, pads, courtyard
    a.rect(268, 180, 180, 25, width=1.2, opacity=.6)
    a.text(358, 198, "PCB", size=10, opacity=.4)
    a.rect(310, 105, 95, 70, width=1.8, radius=2)
    a.text(358, 145, "本体", size=10, opacity=.4)
    a.poly([(310, 140), (290, 140), (290, 180)], width=1.8)
    a.poly([(405, 140), (425, 140), (425, 180)], width=1.8)
    a.rect(280, 176, 20, 10, width=1.2, radius=1)
    a.rect(416, 176, 20, 10, width=1.2, radius=1)
    a.rect(276, 92, 164, 124, width=1.0, dash="3 5", opacity=.5)
    a.text(358, 84, "courtyard", size=10, opacity=.5)
    a.text(358, 246, "器件允许占用的边界", size=10, opacity=.45)

    rows = ("1 脚与丝印同向", "pad 编号逐脚对", "间距 / 本体量一遍", "courtyard 不压邻居")
    for i, row in enumerate(rows):
        y = 100 + i * 34
        check(a, 498, y - 4, s=6)
        a.text(516, y, row, size=10, anchor="start", opacity=.65)
    a.text(592, 246, "名字相同 ≠ 封装相同", size=10, opacity=.5)

    a.text(360, 288, "封装核对不是“看一眼”：方向、编号、尺寸、边界，四个都过才算分配完成。", size=12, opacity=.55)


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
    board(a, 90, 44, 540, 210)
    zones = [(105, 60, 100, 80, "USB / 电源"), (225, 60, 150, 70, "MCU / 晶振"),
             (395, 60, 110, 80, "可选射频"), (105, 160, 120, 74, "接口 / ESD"),
             (245, 150, 130, 84, "传感器"), (395, 160, 105, 74, "调试 / 测试点")]
    for x, y, w, h, lab in zones:
        a.rect(x, y, w, h, width=1.2, opacity=.45, radius=2)
        a.text(x + w / 2, y + h / 2, lab, size=11, opacity=.65)
    a.arrow(205, 100, 225, 100, width=1.4); a.arrow(375, 95, 395, 95, width=1.4)
    a.arrow(165, 140, 165, 160, width=1.4); a.arrow(305, 130, 305, 150, width=1.4)
    a.text(360, 282, "先摆“必须靠边”的接口，再摆“必须靠近”的电源与去耦，最后才是信号。", size=12, opacity=.55)


def ch06_decouple(a):
    # left: tight loop
    a.text(170, 38, "good · 小环路", size=15, opacity=.6)
    chip(a, 100, 80, 80, 90, "MCU", pins=3, fs=12)
    a.line(180, 100, 220, 100, width=1.4)
    a.line(220, 100, 220, 130, width=1.4)
    a.line(220, 130, 180, 130, width=1.4)
    a.text(238, 100, "VCC", size=10, anchor="start")
    a.text(238, 130, "GND", size=10, anchor="start")
    a.path("M150 100q0 0 0 0", width=1)
    a.circle(220, 115, 12, width=1.4)
    a.line(214, 115, 226, 115, width=1.0); a.line(220, 109, 220, 121, width=1.0)
    a.text(220, 158, "C1", size=9, opacity=.5)
    # right: long loop
    a.text(530, 38, "bad · 大环路", size=15, opacity=.6)
    chip(a, 420, 80, 80, 90, "MCU", pins=3, fs=12)
    a.line(500, 100, 620, 100, width=1.4)
    a.line(620, 100, 620, 190, width=1.4)
    a.line(620, 190, 500, 190, width=1.4)
    a.text(628, 100, "VCC", size=10, anchor="start")
    a.text(628, 190, "GND", size=10, anchor="start")
    a.rect(596, 130, 26, 14, width=1.2)
    a.text(609, 158, "C1", size=9, opacity=.5)
    a.path("M520 100q30 0 30 30", width=1.0, opacity=.3, dash="3 5")
    a.text(360, 250, "去耦电容不是“放在板子上”，而是“让电流的回路尽量小”。", size=12, opacity=.55)


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
    a.text(360, 30, "三道门都过，才叫“可以发板”", size=15, opacity=.55)
    gates = [("DRC", "规则 · 连通 · 几何", "0 通过 / 5 违规", "只证明规则"),
             ("电气确认", "接得对 · 值对 · 回流顺", "人工走查 + 上电", "只证明意图"),
             ("工厂能力", "线宽 · 环宽 · 阻焊桥", "DFM 表 + 工厂确认", "只证明工艺")]
    for i, (title, l1, l2, tail) in enumerate(gates):
        x = 55 + i * 215
        a.rect(x, 70, 180, 122, width=1.8, radius=4)
        a.text(x + 90, 102, title, size=15)
        a.text(x + 90, 130, l1, size=9, opacity=.6)
        a.text(x + 90, 151, l2, size=9, opacity=.55)
        a.line(x + 18, 164, x + 162, 164, width=.8, opacity=.25)
        a.text(x + 90, 184, tail, size=8, opacity=.45)
        a.line(x + 90, 192, x + 90, 220, width=1.3)
    a.line(145, 220, 575, 220, width=1.3)
    a.arrow(360, 220, 360, 246, width=1.5, head=5)
    a.rect(300, 252, 120, 30, width=1.6, radius=3)
    a.text(360, 272, "发板", size=12)


# ---- chapter 10 --------------------------------------------------------
def ch10_pkg(a):
    a.rect(40, 44, 300, 204, width=1.4, radius=3)
    a.text(190, 68, "fab/", size=15, anchor="start", opacity=.65)
    items = [("board-F_Cu.gbr", "顶层铜"), ("board-B_Cu.gbr", "底层铜"), ("board-F_Mask.gbr", "阻焊"),
             ("board-Edge_Cuts.gbr", "板框"), ("board.drl", "钻孔"), ("board-pos.csv", "贴片坐标"),
             ("bom.csv", "物料"), ("board.step", "3D")]
    for i, (f, d) in enumerate(items):
        y = 86 + i * 20
        a.text(58, y, f, size=10, anchor="start")
        a.text(300, y, d, size=9, anchor="end", opacity=.45)
    a.arrow(350, 146, 410, 146, width=2.0)
    a.text(380, 132, "打包", size=10, opacity=.5)
    a.path("M430 78h180v136H430z", width=1.6, opacity=.5, dash="3 4")
    a.path("M430 78l-18 18v136h180V96l-18-18", width=1.6, opacity=.6)
    a.line(412, 96, 610, 96, width=1.0, opacity=.4)
    a.text(520, 160, "fab.zip", size=18, opacity=.7)
    a.text(520, 186, "一次投板的最小完整集", size=10, opacity=.45)
    a.text(360, 278, "Gerber 描述铜与阻焊，钻孔描述孔，坐标描述贴片；少一样，工厂就要来问你。", size=12, opacity=.55)


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
    steps = [("钢网", 60), ("印刷", 190), ("贴片", 320), ("回流", 450), ("检验", 580)]
    for i, (lab, x) in enumerate(steps):
        a.circle(x + 40, 120, 26, width=1.8)
        a.text(x + 40, 126, str(i + 1), size=16)
        a.text(x + 40, 172, lab, size=13, opacity=.65)
        if i < 4:
            a.arrow(x + 68, 120, x + 118, 120, width=1.8, head=6)
    a.rect(54, 204, 612, 34, width=1.2, radius=2)
    a.text(360, 227, "印刷 → 贴片 → 回流 → 检验：每一段都要有可追溯的批次与参数", size=11, opacity=.55)
    a.text(360, 278, "手焊和回流不是两件事，而是同一套“热、锡、助焊剂”的不同尺度。", size=12, opacity=.55)


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
    a.text(360, 34, "上电后先测这三段，再插 ISP", size=14, opacity=.6)

    # USB-C input
    a.rect(28, 92, 74, 60, width=2.0, radius=4)
    a.text(65, 118, "USB-C", size=11)
    a.text(65, 136, "VBUS/GND", size=10, opacity=.55)
    a.line(102, 116, 160, 116, width=2.0)

    # VBUS test point
    a.circle(166, 116, 5, width=1.4)
    a.line(166, 111, 166, 98, width=1.0, opacity=.5)
    a.text(166, 80, "VBUS", size=11, opacity=.7)
    a.text(166, 94, "≈5 V", size=10, opacity=.5)

    # fuse
    a.rect(188, 102, 58, 28, width=1.8, radius=2)
    a.text(217, 121, "F1", size=12)
    a.line(171, 116, 188, 116, width=1.8)
    a.line(246, 116, 278, 116, width=2.0)

    # +5V test point
    a.circle(284, 116, 5, width=1.4)
    a.line(284, 111, 284, 98, width=1.0, opacity=.5)
    a.text(284, 80, "+5V", size=11, opacity=.7)
    a.text(284, 94, "≈5 V", size=10, opacity=.5)

    # LDO
    a.rect(326, 84, 98, 64, width=2.0, radius=3)
    a.text(375, 112, "U2", size=13)
    a.text(375, 132, "LDO", size=10, opacity=.5)
    a.line(289, 116, 326, 116, width=1.8)
    a.line(424, 116, 458, 116, width=2.0)

    # +3V3 test point
    a.circle(464, 116, 5, width=1.4)
    a.line(464, 111, 464, 98, width=1.0, opacity=.5)
    a.text(464, 80, "+3V3", size=11, opacity=.7)
    a.text(464, 94, "3.3 V", size=10, opacity=.5)

    # load
    a.rect(514, 84, 156, 64, width=2.0, radius=3)
    a.text(592, 112, "ATtiny85", size=12)
    a.text(592, 132, "+ LED", size=10, opacity=.5)
    a.line(469, 116, 514, 116, width=1.8)

    # ground rail and symbol
    a.line(52, 192, 650, 192, width=2.0)
    for x, y0 in ((65, 152), (375, 148), (592, 148)):
        a.line(x, y0, x, 192, width=1.2, opacity=.7)
    a.line(360, 192, 360, 204, width=2.0)
    a.line(344, 204, 376, 204, width=1.6)
    a.line(350, 210, 370, 210, width=1.4)
    a.line(356, 216, 364, 216, width=1.2)
    a.text(386, 214, "GND", size=10, anchor="start", opacity=.5)

    # three measurement cards
    cards = (
        (40, "VBUS → GND", "≈5 V", "无：查 USB-C / 线缆"),
        (250, "F1 后 → GND", "≈5 V", "无：查 F1 / 焊点"),
        (460, "+3V3 → GND", "3.3 V", "无：查 LDO / EN / 负载"),
    )
    for x, lab, val, hint in cards:
        a.rect(x, 232, 192, 82, width=1.2, radius=3, opacity=.7)
        a.text(x + 96, 252, lab, size=10, opacity=.55)
        a.text(x + 96, 282, val, size=22, opacity=.85)
        a.text(x + 96, 302, hint, size=10, opacity=.45)
    a.text(360, 332, "黑笔固定 GND，红笔逐点；先断电再换档。", size=11, opacity=.5)


# ---- chapter 13 --------------------------------------------------------
def ch13_sim(a):
    # source - resistor - cap
    a.circle(90, 120, 20, width=2.0)
    a.text(90, 126, "V1", size=11)
    a.line(110, 120, 170, 120, width=1.8)
    a.poly([(170, 106), (180, 134), (190, 106), (200, 134), (210, 106), (220, 120)], width=1.8)
    a.line(220, 120, 280, 120, width=1.8)
    a.line(280, 104, 280, 136, width=2.2)
    a.line(292, 104, 292, 136, width=2.2)
    a.line(292, 120, 350, 120, width=1.8)
    a.circle(350, 120, 3.0, width=1.2)
    a.line(90, 140, 90, 190, width=1.8)
    a.line(90, 190, 350, 190, width=1.8)
    a.line(350, 120, 350, 190, width=1.8)
    a.text(360, 100, "Vout", size=10, anchor="start", opacity=.6)
    # plot
    a.rect(400, 54, 270, 150, width=1.2, radius=2)
    a.line(420, 180, 650, 180, width=1.0, opacity=.3)
    a.line(420, 180, 420, 70, width=1.0, opacity=.3)
    a.path("M420 180Q470 70 520 100T650 120", width=1.8)
    a.text(535, 224, "t", size=10, opacity=.5)
    a.text(405, 70, "V", size=10, anchor="end", opacity=.5)
    a.text(535, 250, "DC / AC / TRAN", size=12, opacity=.6)
    a.text(360, 280, "仿真是“在铜之前问问题”：工作点、瞬态、频率响应，各有各的用途。", size=12, opacity=.55)


def ch13_wave(a):
    a.line(70, 190, 660, 190, width=1.6)
    a.line(70, 190, 70, 60, width=1.6)
    a.path("M70 190C160 190 180 80 300 80C420 80 440 190 660 190", width=2.2)
    for x, lab in ((70, "0"), (250, "τ"), (430, "2τ"), (610, "3τ")):
        a.line(x, 190, x, 198, width=1.0, opacity=.4)
        a.text(x, 214, lab, size=10, opacity=.55)
    a.line(250, 80, 250, 190, width=1.0, opacity=.3, dash="2 4")
    a.line(430, 80, 430, 190, width=1.0, opacity=.3, dash="2 4")
    a.text(360, 52, "V(t) = V0 (1 - e^(-t/RC))", size=14, opacity=.65)
    a.text(360, 242, "时间常数 τ = R × C：它决定“多快算稳定”，不是“最终到多少”。", size=12, opacity=.55)


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


figs = {
    "kicad-learning-path": (720, 260, learning_path),
    "kicad-ch01-flow": (720, 260, ch01_flow),
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
    "kicad-ch07-diffpair": (720, 280, ch07_diff),
    "kicad-ch08-pour": (720, 300, ch08_pour),
    "kicad-ch08-antenna": (720, 300, ch08_antenna),
    "kicad-ch08-return-path": (720, 300, ch08_return_path),
    "kicad-ch09-drc": (720, 300, ch09_drc),
    "kicad-ch09-dfm": (720, 280, ch09_dfm),
    "kicad-ch09-three-gates": (720, 300, ch09_three_gates),
    "kicad-ch10-fab-package": (720, 300, ch10_pkg),
    "kicad-ch10-cli": (720, 300, ch10_cli),
    "kicad-ch11-order": (720, 300, ch11_order),
    "kicad-ch11-assembly": (720, 300, ch11_assembly),
    "kicad-ch12-bringup": (720, 280, ch12_bringup),
    "kicad-ch12-power": (720, 340, ch12_power),
    "kicad-ch12-debug": (720, 280, ch12_debug),
    "kicad-ch13-sim": (720, 300, ch13_sim),
    "kicad-ch13-wave": (720, 260, ch13_wave),
    "kicad-ch14-library": (720, 280, ch14_library),
    "kicad-ch14-git": (720, 300, ch14_git),
    "kicad-ch15-automation": (720, 280, ch15_ci),
    "kicad-ch15-plugin": (720, 280, ch15_plugin),
}
for name, (w, h, fn) in figs.items():
    fig(name, w, h, fn)
print("figures:", len(figs))
