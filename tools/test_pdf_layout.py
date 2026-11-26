#!/usr/bin/env python3
"""Print-layout regressions that need the built PDF.

Two failures found in the Round 7 raster audit are cheap to detect from the
text layer, so they become gates instead of one-off observations:

* a page whose visible body is a lone sentence or bullet (a tail page that
  should have stayed with the block before it);
* a table cell code token split across lines in appendix B.2, which is what
  happened when Chromium squeezed the first column to a few characters.

Run after the PDF build; the CI workflow does that explicitly.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import cast

import fitz

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "yuyu-book" / "dist" / "kicad-book-zh.pdf"

# A real page of this book carries far more than two lines. Captions, chapter
# notes and plates are exempted below because they are intentionally short.
MIN_BODY_CHARS = 120

# Code tokens that must stay on one line in the appendix B.2 table. A trailing
# underscore or a bare `pro`/`sch`/`table` line means the column collapsed.
SPLIT_TOKEN_LINES = re.compile(
    r"^(?:\.kicad_|sym-|lib-|fp-|table|info-|cache|pro|sch|pcb)$")

# Every filename in the B.2 table. The old layout broke several of these at
# the underscore or hyphen, so an exact-line match is the regression.
B2_TOKENS = [
    ".kicad_pro", ".kicad_sch", ".kicad_pcb", "sym-lib-table",
    "fp-lib-table", ".kicad_sym", ".pretty/", ".kicad_mod", ".kicad_dru",
    ".kicad_wks", ".kicad_jobset", ".kicad_prl", "fp-info-cache",
    "<工程名>-backups/",
]

B2_HEADER = ("扩展名", "内容", "格式", "谁生成", "分发")

# A table card may extend below its last row while fragmenting across pages.
# The old B.2 continuation appended about 40 pt of empty bordered card; after
# the fix the gap is under 10 pt.
B2_CARD_MAX_GAP = 20.0

# A justified CJK line normally advances each glyph by about 12 pt (10.2 pt
# glyph plus 1.8 pt tracking). When Chromium pushes an unbreakable code token
# to the next line, it stretches the lead-in: the observed regression left
# gaps of 10.2-21.3 pt between fragments of one visual line. A 3.5 pt gap is
# already a third of the glyph advance and does not occur in normal set text.
# Table cards use wide column gaps too, so filled card containers are skipped.
RIVER_MAX_GAP = 3.5


def body_text(page: fitz.Page) -> str:
    """Text inside the trim, without the running head and footer folio."""
    parts = []
    for block in page.get_text("blocks"):
        y0, y1 = float(block[1]), float(block[3])
        if y1 < 50 or y0 > 780:
            continue
        parts.append(str(block[4]))
    return "\n".join(parts).strip()


def underfilled_pages(doc: fitz.Document) -> list[int]:
    """Pages after the preface whose body is only a sentence or a bullet."""
    first_body = doc.get_toc()[0][2] - 1
    bad = []
    for index in range(first_body, doc.page_count):
        page = doc[index]
        if page.rect.width > page.rect.height:
            continue  # landscape plate sheet
        image_area = 0.0
        for info in page.get_image_info():
            x0, y0, x1, y1 = info["bbox"]
            image_area += max(0.0, x1 - x0) * max(0.0, y1 - y0)
        if image_area > 0.2 * page.rect.width * page.rect.height:
            continue  # photo or screenshot plate, not a tiny icon
        text = body_text(page)
        if text.lstrip().startswith("引用链接"):
            continue  # chapter-end citation block
        if text.startswith("图 ") or text.startswith("图\u00a0"):
            continue  # figure or screenshot caption
        if len(text) < MIN_BODY_CHARS:
            bad.append(index + 1)
    return bad


def _line_box(line: dict) -> tuple[float, float, float, float]:
    x0, y0, x1, y1 = (float(value) for value in line["bbox"])
    return x0, y0, x1, y1


def _same_baseline(a: dict, b: dict) -> bool:
    _, ay0, _, ay1 = _line_box(a)
    _, by0, _, by1 = _line_box(b)
    overlap = min(ay1, by1) - max(ay0, by0)
    return overlap > 0.6 * min(ay1 - ay0, by1 - by0)


def _card_containers(page: fitz.Page) -> list[fitz.Rect]:
    """Large filled cards that hold tables, not body prose."""
    cards = []
    for drawing in page.get_drawings():
        fill = drawing.get("fill")
        if drawing["type"] != "f" or not fill:
            continue
        if all(float(channel) > 0.98 for channel in fill):
            continue  # page background
        rect = fitz.Rect(drawing["rect"])
        if (rect.width >= 0.8 * page.rect.width and rect.height > 60
                and rect.y0 > 50 and rect.y1 < 790):
            cards.append(rect)
    return cards


def justified_rivers(doc: fitz.Document) -> list[tuple[int, float, float, str]]:
    """Justified prose lines whose fragments are spread across the column.

    Chromium emits every stretched CJK glyph (and unbreakable code run) as its
    own text line, so PyMuPDF's per-line gaps do not show the defect. Cluster
    fragments by baseline, measure the gaps between their boxes, and ignore
    fragments inside filled table cards.
    """
    bad = []
    for index in range(doc.page_count):
        page = cast(fitz.Page, doc[index])
        candidates = []
        raw = cast(dict, page.get_text("rawdict"))
        for block in cast(list[dict], raw["blocks"]):
            if block["type"] != 0:
                continue
            clusters: list[list[dict]] = []
            for line in cast(list[dict], block["lines"]):
                for cluster in clusters:
                    if _same_baseline(cluster[0], line):
                        cluster.append(line)
                        break
                else:
                    clusters.append([line])
            for lines in clusters:
                if len(lines) < 5:
                    continue
                text = "".join(
                    str(char["c"]) for line in lines
                    for span in line["spans"] for char in span["chars"]
                )
                if sum(1 for char in text if "\u4e00" <= char <= "\u9fff") < 5:
                    continue
                if "\u25c6" in text or "\u2192" in text:
                    continue  # diagram legend, not a paragraph
                ordered = sorted(lines, key=lambda line: _line_box(line)[0])
                gaps = [
                    _line_box(ordered[pos + 1])[0] - _line_box(ordered[pos])[2]
                    for pos in range(len(ordered) - 1)
                ]
                gap = max(gaps)
                if gap > RIVER_MAX_GAP:
                    candidates.append((ordered, text, gap))
        if not candidates:
            continue
        cards = _card_containers(page)
        for ordered, text, gap in candidates:
            if any(
                all(card.x0 <= (_line_box(line)[0] + _line_box(line)[2]) / 2 <= card.x1
                    and card.y0 <= (_line_box(line)[1] + _line_box(line)[3]) / 2 <= card.y1
                    for line in ordered)
                for card in cards
            ):
                continue
            bad.append((index + 1, round(_line_box(ordered[0])[1], 1),
                        round(gap, 1), text[:40]))
    return bad


def page_text(page: fitz.Page) -> str:
    """Plain text for one page, narrowed from PyMuPDF's overload union."""
    return cast(str, page.get_text("text"))


def b2_pages(doc: fitz.Document) -> range:
    start = None
    end = doc.page_count
    for index in range(doc.page_count):
        text = page_text(doc[index])
        if start is None and "B.2 核心文件速查" in text:
            start = index
        elif start is not None and "B.3 一个原理图文件的开头" in text:
            end = index + 1  # B.3 can start below the table's last rows
            break
    return range(start, end) if start is not None else range(0, 0)


def appendix_b_token_splits(doc: fitz.Document) -> list[tuple[int, str]]:
    """Lines in B.2 that are only a fragment of a code token."""
    if not b2_pages(doc):
        return [(0, "B.2 heading not found")]
    bad = []
    for index in b2_pages(doc):
        for line in page_text(doc[index]).splitlines():
            line = line.strip()
            if SPLIT_TOKEN_LINES.match(line):
                bad.append((index + 1, line))
    return bad


def appendix_b_missing_tokens(doc: fitz.Document) -> list[str]:
    """B.2 filenames that never appear as one complete line."""
    lines = set()
    for index in b2_pages(doc):
        lines.update(line.strip() for line in page_text(doc[index]).splitlines())
    return [token for token in B2_TOKENS if token not in lines]


def appendix_b_structure(doc: fitz.Document) -> list[str]:
    """Each B.2 card has one header and each filename row appears once."""
    problems = []
    counts = {token: 0 for token in B2_TOKENS}
    for index in b2_pages(doc):
        lines = [line.strip() for line in page_text(doc[index]).splitlines()]
        rows = [token for token in B2_TOKENS if token in lines]
        headers = lines.count("扩展名")
        if rows and headers != 1:
            problems.append(f"page {index + 1}: {headers} B.2 table headers")
        if not rows and all(label in lines for label in B2_HEADER):
            problems.append(f"page {index + 1}: B.2 table header has no rows")
        for token in rows:
            counts[token] += 1
    for token, count in counts.items():
        if count > 1:
            problems.append(f"B.2 filename appears {count} times: {token}")
    return problems


def appendix_b_card_gaps(doc: fitz.Document) -> list[tuple[int, float]]:
    """Empty bordered strip below the last text row of a B.2 table card."""
    bad = []
    seen = set()
    for index in b2_pages(doc):
        page = doc[index]
        blocks = page.get_text("blocks")
        header_y = [
            float(block[1]) for block in blocks
            if "扩展名" in str(block[4])
        ]
        if not header_y:
            continue
        for drawing in page.get_drawings():
            rect = drawing["rect"]
            fill = drawing.get("fill")
            if rect.width < 400 or rect.height < 100 or not fill:
                continue
            if fill[0] > 0.95:  # page background or a bright callout
                continue
            if not (rect.y0 <= min(header_y) < rect.y1):
                continue
            inside = [
                float(block[3]) for block in blocks
                if rect.y0 <= float(block[1]) and float(block[3]) <= rect.y1
            ]
            if not inside:
                continue
            gap = rect.y1 - max(inside)
            key = (index + 1, round(gap, 1))
            if gap > B2_CARD_MAX_GAP and key not in seen:
                seen.add(key)
                bad.append(key)
    return bad


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else PDF
    if not target.exists():
        print(f"PDF layout: missing {target}")
        return 1
    doc = fitz.open(target)
    try:
        problems = []
        short = underfilled_pages(doc)
        if short:
            problems.append(f"pages with a lone body sentence/bullet: {short}")
        rivers = justified_rivers(doc)
        if rivers:
            problems.append(
                f"spaced-out justified prose lines (fragment gap >{RIVER_MAX_GAP:g} pt): "
                f"{rivers[:12]}")
        splits = appendix_b_token_splits(doc)
        if splits:
            problems.append(f"appendix B.2 split code tokens: {splits[:12]}")
        missing = appendix_b_missing_tokens(doc)
        if missing:
            problems.append(f"appendix B.2 filenames not on one line: {missing}")
        structure = appendix_b_structure(doc)
        if structure:
            problems.append(f"appendix B.2 table structure: {structure[:12]}")
        gaps = appendix_b_card_gaps(doc)
        if gaps:
            problems.append(f"appendix B.2 empty card strips: {gaps[:12]}")
        if problems:
            print("PDF LAYOUT CHECK FAILED")
            for problem in problems:
                print(" -", problem)
            return 1
        print("PDF layout: OK")
        return 0
    finally:
        doc.close()


if __name__ == "__main__":
    sys.exit(main())
