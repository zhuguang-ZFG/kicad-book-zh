"""A tiny hand-drawn SVG kit: wobbly ink lines, serif labels, no ids."""
from __future__ import annotations

import hashlib
import html


def _n(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s or "0"


def _jitter(seed: str, lo: float, hi: float) -> float:
    h = int(hashlib.sha1(seed.encode("utf-8")).hexdigest()[:8], 16)
    return lo + (h / 0xFFFFFFFF) * (hi - lo)


class Ink:
    def __init__(self, w: int, h: int, label: str = ""):
        self.w, self.h = w, h
        self.label = label
        self.parts: list[str] = []

    # -- primitives -----------------------------------------------------
    def raw(self, s: str):
        self.parts.append(s)

    def line(self, x1, y1, x2, y2, width=2.2, amp=0.7,
             dash=None, opacity=None, cap="round"):
        seed = f"{x1},{y1},{x2},{y2},{width}"
        dx, dy = x2 - x1, y2 - y1
        length = max((dx * dx + dy * dy) ** 0.5, 1)
        nx, ny = -dy / length, dx / length
        a = _jitter(seed + "a", -amp, amp)
        b = _jitter(seed + "b", -amp, amp)
        c1x, c1y = x1 + dx / 3 + nx * a, y1 + dy / 3 + ny * a
        c2x, c2y = x1 + 2 * dx / 3 + nx * b, y1 + 2 * dy / 3 + ny * b
        d = f"M{_n(x1)} {_n(y1)}C{_n(c1x)} {_n(c1y)} {_n(c2x)} {_n(c2y)} {_n(x2)} {_n(y2)}"
        self.path(d, width=width, dash=dash, opacity=opacity, cap=cap)

    def path(self, d, width=2.2, dash=None, opacity=None, fill="none",
             cap="round", join="round"):
        attrs = [f'd="{d}"', f'stroke-width="{_n(width)}"']
        if fill != "none":
            attrs.append(f'fill="{fill}"')
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{_n(opacity)}"')
        if cap != "round":
            attrs.append(f'stroke-linecap="{cap}"')
        if join != "round":
            attrs.append(f'stroke-linejoin="{join}"')
        self.parts.append("<path " + " ".join(attrs) + "/>")

    def rect(self, x, y, w, h, width=2.2, amp=0.6, dash=None, opacity=None,
             radius=0.0):
        if radius:
            self.line(x + radius, y, x + w - radius, y, width, amp, dash, opacity)
            self.line(x + w, y + radius, x + w, y + h - radius, width, amp, dash, opacity)
            self.line(x + w - radius, y + h, x + radius, y + h, width, amp, dash, opacity)
            self.line(x, y + h - radius, x, y + radius, width, amp, dash, opacity)
            self.path(f"M{_n(x)} {_n(y+radius)}Q{_n(x)} {_n(y)} {_n(x+radius)} {_n(y)}",
                      width=width, dash=dash, opacity=opacity)
            self.path(f"M{_n(x+w-radius)} {_n(y)}Q{_n(x+w)} {_n(y)} {_n(x+w)} {_n(y+radius)}",
                      width=width, dash=dash, opacity=opacity)
            self.path(f"M{_n(x+w)} {_n(y+h-radius)}Q{_n(x+w)} {_n(y+h)} {_n(x+w-radius)} {_n(y+h)}",
                      width=width, dash=dash, opacity=opacity)
            self.path(f"M{_n(x+radius)} {_n(y+h)}Q{_n(x)} {_n(y+h)} {_n(x)} {_n(y+h-radius)}",
                      width=width, dash=dash, opacity=opacity)
        else:
            self.line(x, y, x + w, y, width, amp, dash, opacity)
            self.line(x + w, y, x + w, y + h, width, amp, dash, opacity)
            self.line(x + w, y + h, x, y + h, width, amp, dash, opacity)
            self.line(x, y + h, x, y, width, amp, dash, opacity)

    def circle(self, cx, cy, r, width=2.0, opacity=None, fill="none", dash=None):
        # a slightly imperfect circle made from four arcs
        k = r * 0.5523
        d = (f"M{_n(cx)} {_n(cy-r)}"
             f"C{_n(cx+k)} {_n(cy-r)} {_n(cx+r)} {_n(cy-k)} {_n(cx+r)} {_n(cy)}"
             f"C{_n(cx+r)} {_n(cy+k)} {_n(cx+k)} {_n(cy+r)} {_n(cx)} {_n(cy+r)}"
             f"C{_n(cx-k)} {_n(cy+r)} {_n(cx-r)} {_n(cy+k)} {_n(cx-r)} {_n(cy)}"
             f"C{_n(cx-r)} {_n(cy-k)} {_n(cx-k)} {_n(cy-r)} {_n(cx)} {_n(cy-r)}Z")
        self.path(d, width=width, opacity=opacity, fill=fill, dash=dash)

    def dot(self, cx, cy, r=3.0):
        self.circle(cx, cy, r, width=1.0, fill="currentColor")

    def text(self, x, y, s, size=18, anchor="middle", weight="normal",
             opacity=None, rotate=None, family="Noto Serif CJK SC, Songti SC, SimSun, serif"):
        attrs = [f'x="{_n(x)}"', f'y="{_n(y)}"', f'font-size="{_n(size)}"',
                 f'text-anchor="{anchor}"', f'font-family="{family}"',
                 'fill="currentColor"', 'stroke="none"']
        if weight != "normal":
            attrs.append(f'font-weight="{weight}"')
        if opacity is not None:
            attrs.append(f'opacity="{_n(opacity)}"')
        if rotate is not None:
            attrs.append(f'transform="rotate({_n(rotate)} {_n(x)} {_n(y)})"')
        self.parts.append("<text " + " ".join(attrs) + ">" + html.escape(str(s)) + "</text>")

    def arrow(self, x1, y1, x2, y2, width=2.0, amp=0.5, head=7):
        self.line(x1, y1, x2, y2, width=width, amp=amp)
        dx, dy = x2 - x1, y2 - y1
        length = max((dx * dx + dy * dy) ** 0.5, 1)
        ux, uy = dx / length, dy / length
        px, py = -uy, ux
        for s in (-1, 1):
            hx = x2 - ux * head + px * head * 0.55 * s
            hy = y2 - uy * head + py * head * 0.55 * s
            self.line(x2, y2, hx, hy, width=width, amp=0.25)

    def poly(self, pts, width=2.0, amp=0.5, close=False):
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            self.line(x1, y1, x2, y2, width=width, amp=amp)
        if close and len(pts) > 2:
            self.line(pts[-1][0], pts[-1][1], pts[0][0], pts[0][1], width=width, amp=amp)

    def hatch(self, x, y, w, h, step=10, angle=45, opacity=0.18):
        # clipped-looking diagonal strokes inside a rectangle (drawing only)
        import math
        if angle == 45:
            start = -h
            while start < w:
                x1 = x + max(start, 0)
                y1 = y + max(-start, 0)
                x2 = x + min(start + h, w)
                y2 = y + min(h, h + (start + h - w if start + h > w else 0))
                # simpler: use line from top edge to right edge
                start += step
            # simple horizontal-ish hatching that stays inside
            yy = y + step / 2
            while yy < y + h:
                self.line(x + 2, yy, x + w - 2, yy, width=0.7, amp=0.3, opacity=opacity)
                yy += step

    def svg(self) -> str:
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'fill="none" stroke="currentColor" stroke-width="2.2" '
                f'stroke-linecap="round" stroke-linejoin="round"'
                + (f' role="img" aria-label="{html.escape(self.label)}"' if self.label else "")
                + ">")
        return head + "".join(self.parts) + "</svg>"


def save(ink: Ink, path, limit=6000):
    data = ink.svg()
    raw = data.encode("utf-8")
    if len(raw) > limit:
        raise SystemExit(f"{path}: {len(raw)} bytes over {limit}")
    path.write_text(data, encoding="utf-8")
    return len(raw)
