# Round 7 — Independent Print-Layout Review

- **Score: 9/10**
- **Verdict: Accept / ALLOW** — no MAJOR defect; two MINOR issues, both non-blocking.
- **MAJOR: 0** · **MINOR: 2**
- **Confidence: high (0.88)** on layout, gate honesty and content preservation; moderate (0.7) on the purely visual contact-sheet sweep (see Verification gaps).

Artifact judged (not the author's summary): `yuyu-book/dist/kicad-book-zh.pdf` == `kicad-book-zh-round7.pdf`, **210 pages, 14,855,572 B, MD5 `a75f748b020352e8b83794aaac5f4feb`, 25 bookmarks, PDF 1.4, zero blank pages**. Baseline `kicad-book-zh-round6.pdf`: 211 pages, 14,886,118 B, MD5 `1d75b07c951fcdc08e5914595fc6c7bd`.

## Findings

### MINOR 1 — The new layout gate guards only two of the four repaired defects

`tools/test_pdf_layout.py:54-88` checks underfilled pages and `tools/test_pdf_layout.py:95-113` checks B.2 token splits/missing tokens. It does **not** check (a) repeated headers / exactly 14 distinct rows per card, (b) the empty bordered band at a card boundary, (c) chapter-end crowding introduced by the global `.ch-close p` / `.ch-rut` change, or (d) pages that become underfilled *because* they carry an image or the string `引用链接` (both are exempted at lines 66-70). `b2_pages()` (lines 79-88) stops at the first `B.3 一个原理图文件的开头` heading, so any B.2 row pushed past that heading would escape both B.2 checks.

This is a robustness gap, not a current artifact failure: all four defects are clean in this build. Precision of the two implemented checks is acceptable — `SPLIT_TOKEN_LINES` (lines 22-23) matches only standalone fragments, and no line anywhere in the 210-page new PDF matches it; `B2_TOKENS` (lines 27-32) covers all 14 filenames and each occurs once on a single line.

**Concrete fix:** add a row-count/header-count assertion for the two B.2 cards, and a "table rule below all text" check near the B.2 page break; narrow the `get_images()` / `引用链接` exemptions to pages whose body is already long enough to be a real page.

### MINOR 2 — Caveat rewritten in a way that drops its "unresolved" status signal

`附录/B-文件格式与工程结构.md:40` changes the relocated caveat from
`未决问题：官方文件表给出扩展名与用途，但没有逐项规定每种文件的精确格式名；本附录“格式”列…`
to
`官方文件表给出扩展名与用途，但没有逐项规定精确格式名；下表“格式”列…`
The subject matter is preserved and the new position (before B.2) is correct, but removing `未决问题：` turns an explicitly flagged documentation gap into a plain descriptive remark, and dropping `每种文件的` slightly widens the claim. The same passage also has two small precision losses in B.2: `.pretty/` format `目录（含 …）` → `目录，内含 …` and `.kicad_dru` content `针对某个 .kicad_pcb 的自定义设计规则` → `某个 .kicad_pcb 的自定义设计规则` (`附录/B-文件格式与工程结构.md:50,53`). No factual error results; all three are cosmetic/precision edits.

**Concrete fix:** restore `未决问题：` (or `需要说明：`, if "open issue" is no longer intended) and `每种文件的`; optionally restore `针对` in the `.kicad_dru` row. None of these changes affects line breaking at the current column widths, so they are safe to make.

## Verified clean

1. **No content loss.** Only `附录/B-文件格式与工程结构.md` changed among book sources (`git diff` on all other source paths empty). The old p68 bridge sentence occurs **exactly once** in the new PDF, on **p67** — moved, not deleted. It sits 16 pt after the last 验收 bullet (y=705.5 → 721.5) with the closing mark 18 pt below (y=768); no orphan.
2. **Old p192 caveat relocated to new p185, before the B.2 table** (verified by text search and page order); the source-list bullet it replaced at the old location is preserved as the new caveat text.
3. **B.2 high-DPI layout.** New p185 card 1: header + 8 rows (`.kicad_pro`, `.kicad_sch`, `.kicad_pcb`, `sym-lib-table`, `fp-lib-table`, `.kicad_sym`, `.pretty/`, `.kicad_mod`). New p186 card 2: header + 6 rows (`.kicad_dru`, `.kicad_wks`, `.kicad_jobset`, `.kicad_prl`, `fp-info-cache`, `<工程名>-backups/`). 14 unique rows, each header once per card, split exactly at `.kicad_mod` / `.kicad_dru`. No token split, no clipping, no overlap. p185's last table rule is at y=758.2 and the last row text at y=749.3 — **no empty bordered band**.
4. **Full-PDF mechanical scan (210 pages):** zero text blocks crossing the horizontal trim, zero text below y=821 (other than folios), zero standalone token fragments, no blank/near-empty pages, and no new "table rule below all text" cases (the five flagged pages are unchanged from the old PDF's corresponding pages).
5. **Global CSS side effects bounded.** `table td code.nw`, `table tr,table td{break-inside:avoid}`, `.table-scroll{overflow:visible}` and `.file-table` fixed widths produce no overflow anywhere; `.ch-close p{margin-bottom:.2rem}` / `.ch-rut{margin-top:.5rem}` reduce the closing gap by ~13 pt only on p20, p38 and p77/old p78, with gaps still positive (16.9 / 18.4 / 35.3 pt) and no collisions. `class="page-break"` occurs exactly once in source (`附录/B-文件格式与工程结构.md:52`) and once in the built HTML.
6. **Gate honesty, first-hand.** New PDF: `PDF layout: OK`, exit 0. Old PDF (run by monkeypatching the module's `PDF` global; the file was not modified): exit 1 with `pages with a lone body sentence/bullet: [68, 192]`, 12+ split-token samples on p186, and all 14 B.2 filenames "not on one line".
7. **CI/docs wiring.** `.github/workflows/ci.yml:55` runs the layout gate after the PDF build and before `builder --check`; `STRUCTURE.md:43,67` lists it; `README.md:68,72,77` correctly says 210 pages, 25 bookmarks, 17 SI mutation cases.
8. **Prose of touched passages.** The relocated caveat, `.pretty/` and `.kicad_dru` edits and the README number changes contain no `不是…而是…` cadence, forced triad, em-dash pile-up or empty summary sentence. The `不是…而是…` bridge sentence is pre-existing text (unchanged in source) that merely reflowed onto p67, so it is outside this round's prose scope.
9. Bookmarks: 25 in both PDFs; every TOC title identical, only page numbers shift by −1 from old p69 onward.

## Rejected hypotheses

- **"The Ch6 bridge sentence was deleted to save a page."** Rejected: it appears verbatim on new p67 (`@@ -2278,2 +2279,4 @@` in the full line diff) and nowhere on old p67; the page reduction comes from tighter close spacing plus removal of the near-empty old p68.
- **"The caveat was dropped with old p192."** Rejected: `官方文件表给出扩展名与用途` is found on new p185 only, immediately before the B.2 header.
- **"B.2 lost rows when split into two cards."** Rejected: 8 + 6 = 14 distinct rows, verified in both the text layer and the 140 dpi raster.
- **"The global row `break-inside:avoid` created new empty bands."** Rejected: the five rule-below-text pages are identical (modulo renumbering) in old and new PDFs; none occurs in B.2.
- **"The gate might pass the old PDF by accident."** Rejected by direct execution against `kicad-book-zh-round6.pdf` (exit 1, all three failure classes reported).
- **"Old p186 already had a correct repeated header; the split was only a header problem."** Rejected: old p186 has the header once but prints `.kicad_` / `pro` / `mod` as separate lines; the defect was column width, fixed by `.file-table` fixed widths plus `code.nw`.
- **"The half-page gap reported by an automated visual captioner under the Ch6 bridge is a defect."** Rejected by vector geometry: last acceptance text ends y=749.7, closing mark begins y=761.0, folio y=807.2 — the blank area is the normal remainder of a chapter-end sheet.

## Verification gaps

- Direct vision reads of the 14 final contact sheets returned no output in this reviewer's environment, so the all-210-pages raster sweep rests on the earlier raster audit plus the deterministic geometry scan above, not on an independent visual re-read here. Colour, image-plate cropping and subtle typographic weight were therefore not independently re-verified.
- None on the gate set: a first invocation failed only because `/tmp` does not exist on this Windows host; the rerun with a valid temp path gave rc=0 for all six regression tests (`claim`, `USB diagnostic`, `README link`, `book metadata`, `PDF cleanup`, `SI number` with 17 mutations), `check_book` (`CONTENT CHECK OK`) and builder `--check` (`CHECK OK`), in addition to `test_pdf_layout` (exit 0). No source, test, artifact, state file or log was modified by this review.
