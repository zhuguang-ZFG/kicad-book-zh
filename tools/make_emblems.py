import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from ink import Ink, save

OUT = Path(r"D:/Users/kkicad/yuyu-book/illustrations")
OUT.mkdir(parents=True, exist_ok=True)


def emblem(name, draw):
    a = Ink(64, 64)
    draw(a)
    save(a, OUT / f"{name}.svg", limit=6000)


def front(a):
    a.path("M10 20q11-4 21 1v27q-10-5-21-1zM34 21q11-5 20-1v27q-9-4-20 1z", width=2.0)
    a.line(15, 27, 26, 29, width=1.1, opacity=.5)
    a.line(15, 33, 26, 35, width=1.1, opacity=.5)
    a.line(38, 29, 49, 27, width=1.1, opacity=.5)
    a.line(38, 35, 49, 33, width=1.1, opacity=.5)
    a.rect(23, 39, 18, 12, width=1.2, radius=1)
    a.line(27, 43, 37, 43, width=.9, opacity=.6)
    a.line(27, 47, 33, 47, width=.9, opacity=.6)
    a.circle(20, 23, 1.4); a.circle(44, 23, 1.4)


def ch01(a):
    # five sheets fanned, one chip on top
    for i, dx in enumerate((-12, -6, 0, 6, 12)):
        a.rect(20 + dx, 18 + abs(dx) * .3, 22, 28, width=1.5, radius=2, opacity=.65)
    a.rect(22, 20, 22, 28, width=2.0, radius=2)
    a.rect(26, 24, 8, 7, width=1.1)
    a.line(27, 27, 33, 27, width=.8)
    a.line(27, 30, 31, 30, width=.8)
    a.line(38, 25, 40, 25, width=1.1)
    a.line(38, 29, 40, 29, width=1.1)
    a.line(38, 33, 40, 33, width=1.1)
    a.line(26, 38, 39, 38, width=1.0, opacity=.55)
    a.line(26, 42, 35, 42, width=1.0, opacity=.55)


def ch02(a):
    a.line(8, 32, 17, 32, width=2.0)
    a.poly([(17, 26), (21, 38), (25, 26), (29, 38), (33, 26), (37, 38), (41, 26), (45, 32)], width=1.8)
    a.line(45, 32, 57, 32, width=2.0)
    a.circle(45, 32, 2.4, width=1.4)
    a.line(10, 44, 54, 44, width=1.2, opacity=.35, dash="2 5")
    a.text(20, 55, "R1", size=9, opacity=.7)


def ch03(a):
    a.path("M32 8q12 4 20 5v17q0 16-20 26Q12 46 12 30V13q8-1 20-5z", width=2.0)
    a.path("M22 32l7 7 14-15", width=2.6)
    a.circle(32, 30, 20, width=.8, opacity=.2, dash="2 6")


def ch04(a):
    a.rect(10, 14, 44, 36, width=1.0, opacity=.35, radius=2)
    for x in (17, 27, 37, 47):
        a.rect(x, 18, 6, 7, width=1.4, radius=1)
        a.rect(x, 39, 6, 7, width=1.4, radius=1)
    a.rect(22, 27, 20, 12, width=1.2, opacity=.5)
    a.circle(32, 33, 2.2, width=1.0)
    a.text(32, 58, "SOIC-8", size=8, opacity=.65)


def ch05(a):
    for i, dy in enumerate((30, 22, 14)):
        a.path(f"M12 {dy+8}l20-7 20 7-20 7z", width=1.5, opacity=.8 - i * .12)
        a.line(12, dy + 8, 12, dy + 12, width=1.2, opacity=.5)
        a.line(52, dy + 8, 52, dy + 12, width=1.2, opacity=.5)
        a.line(12, dy + 12, 32, dy + 19, width=1.0, opacity=.4)
        a.line(52, dy + 12, 32, dy + 19, width=1.0, opacity=.4)
    a.line(32, 20, 32, 48, width=2.0, dash="3 3", opacity=.6)
    a.circle(32, 20, 2.0); a.circle(32, 48, 2.0)


def ch06(a):
    a.rect(10, 10, 44, 44, width=2.0, radius=2)
    a.rect(16, 16, 14, 12, width=1.2, opacity=.65)
    a.rect(34, 16, 14, 10, width=1.2, opacity=.65)
    a.rect(16, 32, 10, 16, width=1.2, opacity=.65)
    a.rect(30, 30, 18, 18, width=1.2, opacity=.65)
    a.circle(49, 49, 2.2, width=1.0)
    a.circle(15, 15, 2.2, width=1.0)
    a.text(23, 24, "PWR", size=6.5, opacity=.6)
    a.text(41, 23, "MCU", size=6.5, opacity=.6)
    a.text(21, 42, "IO", size=6.5, opacity=.6)
    a.text(39, 40, "RF", size=6.5, opacity=.6)


def ch07(a):
    a.circle(12, 48, 3.0, width=1.2)
    a.line(14, 46, 28, 32, width=3.0)
    a.line(28, 32, 40, 32, width=3.0)
    a.line(40, 32, 52, 20, width=3.0)
    a.circle(52, 20, 2.6, width=1.2)
    a.circle(40, 32, 2.2, width=1.0)
    a.line(18, 18, 26, 26, width=1.0, opacity=.3, dash="2 4")
    a.text(30, 55, "45°", size=9, opacity=.65)


def ch08(a):
    a.rect(8, 10, 48, 44, width=1.0, opacity=.3, radius=2)
    for y in (20, 30, 40, 50):
        for x in (16, 26, 36, 46):
            a.circle(x, y, 1.4, width=.8, opacity=.55)
    a.path("M8 18q6-5 12 0t12 0 12 0 12 0", width=2.0)
    a.line(8, 46, 54, 46, width=1.0, opacity=.3, dash="2 5")
    a.text(32, 60, "GND", size=8, opacity=.6)


def ch09(a):
    a.circle(27, 27, 16, width=2.2)
    a.line(38, 38, 52, 52, width=4.0)
    a.circle(27, 27, 9, width=1.0, opacity=.3, dash="2 5")
    a.path("M21 21l12 12M33 21l-12 12", width=2.0)
    a.circle(25, 24, 1.2)
    a.circle(30, 29, 1.2)


def ch10(a):
    for i, dy in enumerate((8, 16, 24)):
        a.rect(10, dy, 32, 7, width=1.3, opacity=.75 - i * .12)
    a.path("M48 10v22l-5 6h10l-5-6", width=2.0)
    a.line(48, 38, 48, 48, width=2.0)
    a.line(43, 48, 53, 48, width=1.4)
    a.circle(48, 52, 3.0, width=1.0)
    a.text(26, 55, "GTO", size=8, opacity=.55)
    a.text(26, 48, "DRL", size=8, opacity=.55)


def ch11(a):
    a.line(8, 42, 56, 42, width=2.4)
    a.circle(16, 48, 5, width=1.4); a.circle(34, 48, 5, width=1.4); a.circle(52, 48, 5, width=1.4)
    a.rect(18, 16, 26, 18, width=2.0, radius=1)
    a.path("M24 22h10v6H24z", width=1.2)
    a.line(45, 25, 56, 25, width=1.0, opacity=.4)
    a.text(31, 12, "PCB", size=8, opacity=.55)


def ch12(a):
    a.path("M10 48l24-24 6 6-24 24z", width=2.2)
    a.path("M34 24l7-7 6 6-7 7z", width=1.8)
    a.line(40, 17, 50, 8, width=2.0)
    a.circle(50, 8, 2.0)
    a.path("M12 50q6 4 12 0", width=1.0, opacity=.3, dash="2 4")
    a.circle(44, 38, 3.0, width=1.0, opacity=.5)
    a.circle(50, 44, 1.8, width=1.0, opacity=.4)


def ch13(a):
    a.rect(8, 14, 48, 34, width=2.0, radius=2)
    a.line(12, 18, 12, 44, width=1.0, opacity=.4)
    a.line(12, 31, 52, 31, width=1.0, opacity=.3)
    a.path("M12 34q6-16 12 0t12 0 12 0", width=1.8)
    a.circle(51, 40, 1.6)
    a.line(16, 52, 48, 52, width=1.2, opacity=.4)


def ch14(a):
    a.rect(10, 12, 44, 40, width=2.0, radius=2)
    for dy in (22, 34, 46):
        a.line(10, dy, 54, dy, width=1.2, opacity=.55)
        a.circle(44, dy - 5, 1.4, width=.9, opacity=.6)
    a.path("M20 18l8 0 4 4-4 4-8 0z", width=1.2, opacity=.7)
    a.line(20, 30, 34, 30, width=1.0, opacity=.4)
    a.line(20, 42, 32, 42, width=1.0, opacity=.4)


def ch15(a):
    a.rect(8, 12, 48, 34, width=2.0, radius=2)
    a.line(8, 20, 56, 20, width=1.0, opacity=.5)
    a.text(18, 31, ">_", size=10, anchor="start")
    a.line(18, 38, 38, 38, width=1.0, opacity=.5)
    a.line(18, 43, 30, 43, width=1.0, opacity=.5)
    a.circle(48, 48, 6, width=1.2)
    a.line(48, 44, 48, 48, width=1.4)
    a.line(48, 48, 51, 50, width=1.2)


def apxa(a):
    a.rect(8, 18, 48, 28, width=2.0, radius=2)
    for x in (14, 23, 32, 41, 50):
        a.rect(x, 24, 6, 6, width=1.0, radius=.8)
    a.rect(20, 36, 24, 5, width=1.0, radius=.8)


def apxb(a):
    a.line(14, 12, 14, 52, width=1.6)
    for y in (18, 28, 38, 48):
        a.line(14, y, 30, y, width=1.2, opacity=.6)
    a.rect(22, 14, 24, 8, width=1.2, opacity=.65)
    a.rect(22, 24, 30, 8, width=1.2, opacity=.65)
    a.rect(22, 40, 22, 8, width=1.2, opacity=.65)
    a.line(30, 18, 36, 18, width=.8, opacity=.5)
    a.line(30, 28, 38, 28, width=.8, opacity=.5)


def apxc(a):
    a.path("M32 8L56 52H8z", width=2.2)
    a.line(32, 22, 32, 38, width=2.8)
    a.circle(32, 45, 1.8, width=1.0, fill="currentColor")


def apxd(a):
    a.path("M10 18q10-4 20 1v30q-10-5-20-1zM34 19q10-5 20-1v30q-10-4-20 1z", width=2.0)
    a.text(21, 34, "A", size=13, opacity=.65)
    a.text(44, 34, "中", size=13, opacity=.65)
    a.line(15, 41, 27, 43, width=.9, opacity=.4)
    a.line(38, 43, 49, 41, width=.9, opacity=.4)


for name, fn in {
    "kicad-front": front, "kicad-ch01": ch01, "kicad-ch02": ch02, "kicad-ch03": ch03,
    "kicad-ch04": ch04, "kicad-ch05": ch05, "kicad-ch06": ch06, "kicad-ch07": ch07,
    "kicad-ch08": ch08, "kicad-ch09": ch09, "kicad-ch10": ch10, "kicad-ch11": ch11,
    "kicad-ch12": ch12, "kicad-ch13": ch13, "kicad-ch14": ch14, "kicad-ch15": ch15,
    "kicad-apxa": apxa, "kicad-apxb": apxb, "kicad-apxc": apxc, "kicad-apxd": apxd,
}.items():
    emblem(name, fn)
print("emblems:", len(list(OUT.glob('kicad-*[0-9a-z].svg'))))
