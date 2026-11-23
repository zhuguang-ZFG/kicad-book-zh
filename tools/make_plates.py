import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from ink import Ink, save

OUT = Path(r"D:/Users/kkicad/yuyu-book/illustrations")

def p1(a):
    # drafting table with a schematic sheet
    a.line(60, 200, 660, 200, width=3)
    a.line(110, 200, 95, 232, width=3); a.line(610, 200, 625, 232, width=3)
    a.rect(150, 36, 420, 150, width=2.0, radius=3)
    a.text(360, 62, "原理图 / SCHEMATIC", size=18, opacity=.55)
    a.line(170, 74, 550, 74, width=1.0, opacity=.3)
    # resistor and capacitor
    a.poly([(190, 112), (205, 100), (220, 124), (235, 100), (250, 124), (265, 112)], width=2.0)
    a.line(170, 112, 190, 112, width=1.8); a.line(265, 112, 300, 112, width=1.8)
    a.line(300, 100, 300, 124, width=2.2); a.line(310, 100, 310, 124, width=2.2)
    a.line(310, 112, 345, 112, width=1.8)
    # IC
    a.rect(370, 94, 70, 46, width=2.0, radius=2)
    a.line(380, 88, 380, 94, width=1.6); a.line(395, 88, 395, 94, width=1.6)
    a.line(410, 88, 410, 94, width=1.6); a.line(425, 88, 425, 94, width=1.6)
    a.line(380, 140, 380, 146, width=1.6); a.line(395, 140, 395, 146, width=1.6)
    a.line(410, 140, 410, 146, width=1.6); a.line(425, 140, 425, 146, width=1.6)
    a.text(405, 122, "MCU", size=13, opacity=.55)
    a.line(345, 112, 370, 112, width=1.8)
    a.line(440, 112, 480, 112, width=1.8)
    a.circle(480, 112, 3.0, width=1.2)
    a.line(480, 112, 480, 88, width=1.4, opacity=.5)
    a.line(470, 88, 490, 88, width=1.2, opacity=.5)
    # pencil and ruler
    a.path("M585 185l52-70 8 7-52 70z", width=2.0)
    a.path("M637 115l8-11 8 7-8 11z", width=1.6)
    a.line(570, 196, 640, 188, width=2.0)
    a.text(612, 214, "先画意图", size=14, opacity=.55)
    a.text(100, 62, "01", size=30, opacity=.18, weight="600")

def p2(a):
    # PCB top view with traces and a caliper
    a.rect(120, 44, 430, 150, width=2.4, radius=8)
    a.text(335, 28, "PCB / 布局与布线", size=17, opacity=.55)
    # chips
    a.rect(180, 76, 78, 58, width=2.0, radius=2)
    a.rect(300, 66, 54, 42, width=2.0, radius=2)
    a.rect(390, 90, 66, 34, width=2.0, radius=2)
    a.rect(480, 70, 40, 62, width=2.0, radius=3)
    a.text(219, 110, "MCU", size=13, opacity=.55)
    a.text(327, 91, "SENSOR", size=9, opacity=.5)
    a.text(423, 111, "LDO", size=11, opacity=.5)
    a.text(500, 105, "USB-C", size=9, opacity=.5)
    # traces
    a.path("M180 100L150 100L140 90L140 70", width=2.6)
    a.path("M258 100L280 100L290 90L300 90", width=2.0)
    a.path("M354 90L372 90L382 100L390 100", width=2.0)
    a.path("M456 106L470 106L480 96", width=2.0)
    a.path("M180 126L160 126L150 136L150 160", width=1.8)
    a.path("M258 126L300 126L320 146L440 146", width=1.8)
    a.path("M352 108L352 140L390 140", width=1.8)
    # vias
    for x, y in [(150, 70), (290, 90), (382, 100), (470, 96), (150, 160), (440, 146)]:
        a.circle(x, y, 2.2, width=1.0)
        a.circle(x, y, .8, width=.8, fill="currentColor")
    # mounting holes
    for x, y in [(140, 64), (530, 64), (140, 174), (530, 174)]:
        a.circle(x, y, 5.0, width=1.4)
        a.circle(x, y, 2.0, width=.8, opacity=.4)
    # caliper
    a.line(575, 60, 575, 190, width=2.0)
    a.line(565, 60, 585, 60, width=2.0)
    a.line(565, 190, 585, 190, width=2.0)
    a.line(590, 100, 620, 100, width=2.2)
    a.line(590, 140, 620, 140, width=2.2)
    a.text(650, 105, "mm", size=12, opacity=.5)
    a.text(650, 145, "0.1", size=12, opacity=.5)
    a.text(100, 30, "02", size=30, opacity=.18, weight="600")

def p3(a):
    # assembly line: stencil, squeegee, conveyor, oven
    a.line(60, 170, 660, 170, width=3.0)
    for x in (120, 220, 320, 420, 520, 620):
        a.circle(x, 180, 7, width=1.6)
        a.circle(x, 180, 2, width=.8)
    a.rect(120, 62, 150, 90, width=2.2, radius=2)
    a.rect(132, 74, 126, 66, width=1.0, opacity=.3)
    a.text(195, 112, "钢网", size=15, opacity=.6)
    a.path("M145 52L250 52L265 62L158 62Z", width=2.0)
    a.line(202, 60, 202, 78, width=4.0)
    a.rect(310, 84, 90, 58, width=2.0, radius=3)
    a.text(355, 118, "PCB", size=14, opacity=.55)
    a.rect(420, 60, 130, 94, width=2.2, radius=4)
    a.text(485, 105, "回流焊", size=15, opacity=.6)
    a.path("M438 80q20 8 40 0t40 0", width=1.4, opacity=.35)
    a.path("M438 130q20 8 40 0t40 0", width=1.4, opacity=.35)
    a.line(550, 110, 620, 110, width=2.0)
    a.arrow(550, 110, 620, 110, width=2.0)
    a.text(585, 100, "首件", size=12, opacity=.5)
    a.text(80, 44, "03", size=30, opacity=.18, weight="600")

def p4(a):
    # bench: scope, board, probe, laptop
    a.line(60, 195, 660, 195, width=3.0)
    a.rect(100, 54, 190, 110, width=2.4, radius=4)
    a.rect(114, 68, 120, 82, width=1.2, opacity=.35)
    a.path("M120 108q10-26 20 0t20 0 20 0 20 0 20 0", width=1.8)
    a.line(250, 68, 250, 130, width=1.0, opacity=.3)
    for y in (78, 92, 106, 120):
        a.circle(265, y, 4, width=1.2)
    a.text(190, 180, "示波器", size=13, opacity=.55)
    a.rect(340, 110, 150, 60, width=2.0, radius=4)
    a.text(415, 145, "DUT", size=14, opacity=.55)
    a.circle(360, 128, 3.0, width=1.0); a.circle(470, 128, 3.0, width=1.0)
    a.line(360, 128, 330, 100, width=1.8)
    a.path("M330 100l-12-6 4 12z", width=1.4)
    a.text(315, 88, "探头", size=11, opacity=.5)
    a.rect(520, 70, 110, 76, width=2.0, radius=5)
    a.rect(530, 80, 90, 56, width=1.0, opacity=.3)
    a.text(575, 112, "日志", size=13, opacity=.5)
    a.line(540, 92, 610, 92, width=1.0, opacity=.4)
    a.line(540, 102, 600, 102, width=1.0, opacity=.4)
    a.line(540, 112, 605, 112, width=1.0, opacity=.4)
    a.text(80, 40, "04", size=30, opacity=.18, weight="600")

def cover(a):
    # a large board with USB-C, MCU, sensor, antenna, traces; drafting frame
    a.rect(40, 36, 640, 300, width=1.2, opacity=.25, radius=4)
    a.rect(70, 66, 580, 240, width=2.8, radius=10)
    # USB-C
    a.rect(92, 150, 44, 72, width=2.2, radius=8)
    a.rect(100, 160, 28, 52, width=1.0, opacity=.4, radius=4)
    a.text(114, 240, "USB-C", size=12, opacity=.55)
    # power path
    a.path("M136 186L190 186L210 166", width=2.4)
    a.circle(210, 166, 3.0, width=1.2)
    # LDO
    a.rect(220, 140, 56, 48, width=2.0, radius=2)
    a.text(248, 168, "LDO", size=12, opacity=.55)
    # MCU
    a.rect(310, 120, 96, 88, width=2.4, radius=3)
    for i in range(5):
        a.line(322 + i * 16, 112, 322 + i * 16, 120, width=1.4)
        a.line(322 + i * 16, 208, 322 + i * 16, 216, width=1.4)
    a.text(358, 170, "MCU", size=16, opacity=.55)
    # sensor
    a.rect(440, 130, 64, 58, width=2.0, radius=3)
    a.text(472, 164, "SENSOR", size=9, opacity=.5)
    # antenna
    a.path("M540 120q20-20 40 0t40 0", width=2.0)
    a.line(540, 120, 540, 150, width=1.4, opacity=.5)
    a.line(620, 120, 620, 150, width=1.4, opacity=.5)
    a.text(580, 106, "ANT", size=11, opacity=.5)
    # traces
    a.path("M276 164L310 164", width=2.2)
    a.path("M406 150L440 150", width=2.2)
    a.path("M406 182L440 182", width=1.8)
    a.path("M248 188L248 220L300 220L320 240", width=1.8)
    a.path("M358 208L358 240L400 260", width=1.8)
    a.path("M472 188L472 220L520 220L540 200", width=1.8)
    a.path("M136 210L180 210L200 230L280 230", width=1.8)
    # vias and mounting holes
    for x, y in [(190, 166), (300, 220), (400, 260), (520, 220), (280, 230)]:
        a.circle(x, y, 2.4, width=1.0)
        a.circle(x, y, .9, width=.8, fill="currentColor")
    for x, y in [(90, 86), (630, 86), (90, 286), (630, 286)]:
        a.circle(x, y, 6, width=1.4)
        a.circle(x, y, 2.4, width=.8, opacity=.4)
    # corner marks
    for x, y, dx, dy in [(70, 66, 1, 1), (650, 66, -1, 1), (70, 306, 1, -1), (650, 306, -1, -1)]:
        a.line(x, y + dy * 18, x, y, width=1.2, opacity=.5)
        a.line(x, y, x + dx * 18, y, width=1.2, opacity=.5)
    # a pencil at lower right
    a.path("M560 300l52-70 8 6-52 70z", width=1.8)
    a.line(612  -0, 300, 620, 290, width=1.4)

for name, fn in {"part-kicad-p1": p1, "part-kicad-p2": p2, "part-kicad-p3": p3, "part-kicad-p4": p4, "cover-kicad": cover}.items():
    a = Ink(720, 380 if name == "cover-kicad" else 240, label=name)
    fn(a)
    save(a, OUT / f"{name}.svg", limit=20000)
print("plates done")
