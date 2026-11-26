# Round 7 — Independent Follow-up Recheck (`round-7-recheck-2.md`)

**Score: 9/10. Verdict: Accept / ALLOW — merge.**
**MAJOR: 0 (0 new; the prior recheck's river MAJOR is closed). MINOR: 0 new actionable (both original MINORs are closed).**
**Confidence: 0.90 overall** (0.97 artifact integrity / page+bookmark stats, 0.95 gate source + old-red/new-green behavior, 0.88 river closure from vector geometry + five final renders + two archived blocked renders, 0.70 caption reconciliation).

This is a fresh, independent, read-only recheck. I did not trust the executor's or the prior reviewer's conclusions; every claim below was re-derived from the artifact, the source, or the gate output. Only this report file was written — no source, gate, test, state, log, existing review, or recheck file was modified. No PDF was rebuilt.

## 1. Artifact integrity and stats (first-hand)

| Item | Measured |
|---|---|
| `yuyu-book/dist/kicad-book-zh.pdf` | 14,864,057 B, MD5 `4ee2494704c2f2135901fc47849ed284` |
| `yuyu-book/dist/kicad-book-zh-round7.pdf` | byte-identical to the above (same size/hash) |
| Pages / bookmarks / blank pages | **210 / 25 / 0** |
| TOC first / last | `(1,'前言',7)`, `(1,'第一篇 · 把电路画成图',13)` / `(1,'附录 D　术语表',197)`, `(1,'来源与许可',202)` |
| Round-6 baseline | 211 pages, 14,886,118 B, MD5 `1d75b07c951fcdc08e5914595fc6c7bd` |
| HTML | 6,621,762 B, MD5 `b3a5035526bebfd7bfd9d7dcf464af33` |
| Bookmark titles & levels vs round 6 | identical (25/25, `titles_equal=True`, `levels_equal=True`); page numbers shift by one from old p79 on: `(79,78)`, `(169,168)`, `(203,202)` |
| Caption count | 78 unique `<span class="fig-no">` values in HTML (matches claim of 78 unique captions). A narrow PDF-text pattern `图 N` found only 59 distinct lines — a text-extraction/word-splitting artifact, not evidence of missing captions (see gaps). |

Keyword/page checks (from text extraction): `B.2 核心文件速查` p185, `B.3 一个原理图文件的开头` p186, `附录 B` p184, `附录 C` p192, `未决问题` p142/151/185.

## 2. The river MAJOR is closed

(a) **Independent detector, not the gate's function.** I reimplemented a baseline-clustering gap scan over every line of the final PDF: group words by y-baseline, cluster adjacent same-row fragments, flag `gap > 3.5 pt` with ≥5 fragments on a row and ≥5 CJK chars. Whole-book result: **5 candidates, all with `in_card=True`** — p54 gap 119.1 pt, p185 gaps 92.4/75.2 pt, p186 gaps 92.4/80.2 pt. All are ordinary table-column gaps inside filled cards, not prose. On the five formerly/target pages **142, 148, 149, 156, 191: zero prose clusters** with ≥5 same-baseline fragments.

(b) **Glyph advances are normal.** Mean CJK advance on the previously stretched lines: p191 y=141.0 (the `三份核心文件同时创建、备份目录：https://…` line) **11.98 pt**, p142 y=186.0 **10.96 pt**, p148 y=62.8 **10.9 pt**, p149 y=341.1 **11.82 pt**, p156 y=332.0 **10.2 pt**. The blocked build had ~21 pt tracking on the same lines (prior recheck). No residual letter-spacing regression.

(c) **Visual A/B at 140 dpi.** Final pages 142, 148, 149, 156, 191: no visibly stretched body/bullet lines. Archived blocked renders: **p191 shows a tracked-out lead-in with the URL pushed to the next line**; **p149 shows the stretched `切到 Project Specific 标签，确认…` line**. On final p191 the URL breaks sensibly at a slash: line y=141 ends `…/getting_started_in_kicad/`, next line y=158.8 continues `getting_started_in_kicad.html → First project creations（File → New Project …）`.

(d) **Content preserved, not merely reflowed.** Normalized whole-text comparison against round 6: `NORM_LEN r6 136614 final 136580 ratio 0.9996`, 162 diff ops dominated by folio digits and chapter running-head relocation; all key sentences present (`下一章开始布线…`, `未决问题：官方文件表给出扩展名与用途`, `每种文件的精确格式名`, `针对某个 .kicad_pcb 的自定义设计规则`, `目录（含 .kicad_mod 文件）`). All 14 B.2 filename tokens present. Text overflow scan: 0 lines with x1 > 552, 0 with y > 821.

(e) **Cause removed at source.** `yuyu-book/yuyu_book/render.py:117` `_NAME_BREAK_SKIP = {"svg", "style", "script", "textarea", "pre", "h1"…"h6"}` — **no `"code"`**; `git diff` shows no change here because the fix restored HEAD, exactly as claimed. `soften_long_names` (line 128) is applied via `iter_doc(doc, _NAME_BREAK_SKIP)` (line 161), so `<code>` content can again receive soft breaks instead of being forced into justified rivers. `wrap_tables` adds `<code class="nw">` only for space-free `<code>([^<\s]+)</code>` tokens in tables, keeping filenames on one line.

## 3. Original MINOR 1 (layout gate robustness) — closed

`tools/test_pdf_layout.py` was read end-to-end. Its checks are additive and coherent: `underfilled_pages` (narrowed exemptions), `justified_rivers` (`RIVER_MAX_GAP=3.5`, ≥5 fragments, ≥5 CJK, skips `◆`/`→` rows and text inside filled cards), `appendix_b_structure`, `appendix_b_missing_tokens` (14 tokens), `appendix_b_card_gaps` (`B2_CARD_MAX_GAP=20.0`), `split_token_lines`, and structure checks. `main()` runs all of them. No assertion was weakened: the file is new/untracked, so there is no earlier tracked version to degrade; the current assertions are a strict superset of those described in the initial review.

Old-red / new-green behavior (both re-run read-only):
- `python tools/test_pdf_layout.py yuyu-book/dist/kicad-book-zh.pdf` → **`PDF layout: OK`, rc=0**.
- `python tools/test_pdf_layout.py yuyu-book/dist/kicad-book-zh-round6.pdf` → **rc=1**, with the expected failures: lone pages `[68,192]`; B.2 split tokens on p186 (`.kicad_`, `pro`, …); all 14 filenames not on one line; `page 186/187: B.2 table header has no rows`; `empty card strips: [(186, 39.9)]`. The river class correctly does **not** fire on round 6 (round 6 has no stretched prose; its defect was a different one), so the detector is not merely keyed to hash or page count.

**Detector is non-vacuous (synthetic test).** With spaced CJK glyphs at advance 11/16 pt, 10 pt glyphs give ~1–6 pt gaps → 0 rivers; at advance 22/25/30 pt the same detector reported gaps **12/15/20 pt** and fired. Threshold 3.5 pt is ~1/3 of a normal ~10–12 pt CJK advance and well below the historical 9.5–96.6 pt rivers.

**CI ordering.** `.github/workflows/ci.yml` builds the PDF and then runs `python tools/test_pdf_layout.py` on the built PDF; a gate failure fails the job. Verified the check step follows the build step, not precedes it.

## 4. Original MINOR 2 (appendix B.2 precision) — closed

Source: `第二部-设计篇/08-…md` and `附录/B-文件格式与工程结构.md` now place the caveat `未决问题：官方文件表给出扩展名与用途…` in continuous prose (p185) and mark the two table cards with explicit page breaks. `style_print.py` adds table-cell/page-break/file-table width and `ch-close`/`ch-rut` rules; `<code>` tokens in tables get `class="nw"` (`nowrap`).

PDF evidence:
- **p185**: one header row (5 columns: 扩展名/内容/格式/谁生成/分发) + **8 data rows** `.kicad_pro` … `.kicad_mod` (`.kicad_pro`, `.kicad_pcb`, `.kicad_sch`, `.kicad_wks`, `.kicad_mod`, `.pretty/`, `fp-lib-table`, etc. — all 14 tokens across p185+p186). Filenames are on one line, not split. `.pretty/` cell reads `目录（含 .kicad_mod 文件）`; `自定义` intact; no lone `）` line. The vision read noted a *thin* bordered strip below the last row — this is ordinary cell padding (a few pt, last row text ends y=763.5), far inside the gate's 20 pt tolerance and **not** the historical 39.9 pt defect; no action required.
- **p186**: one header + **6 rows** (`.kicad_dru` … `<工程名>-backups/`), no empty strip, `.kicad_dru` content `自定义设计规则` intact and unsplit. My geometry check found the card at y=72.8–369.0 with last text at y=359.4 → gap **9.6 pt** (round 6 was 39.9 pt).

## 5. Gate blind spots (residual, non-blocking)

1. `justified_rivers` needs ≥5 same-baseline fragments and ≥5 CJK chars, and skips rows containing `◆` or `→`; 3–4 fragment stretches or bullet-led rows would not trip it.
2. Its filled-card exclusion can hide a stretched line *inside* a callout/table card; my scan found 5 such skipped clusters in this build, all genuine table columns.
3. `b2_pages()` uses `end = index + 1`, so its window can include the first B.3 page; harmless today (B.3 header/card counts pass) but worth knowing.
4. `appendix_b_card_gaps` only evaluates a page when a filled card rect is found. On p185 no filled drawing of width > 200 exists in the lower table region, so a future large strip there would not be caught by this particular assertion (p186, where the historical defect lived, is covered).
5. `appendix_b_missing_tokens` counts tokens across the whole B.2 window, not per row; a token could be duplicated and still pass (the `structure` check counts headers but not every row).

These are detector limitations, not defects in this artifact, and do not block merge. The two original MINORs are demonstrably fixed on the shipped build.

## 6. Tooling / verification status

- `task_verify run` → `{"status":"unverified","reason":"project-or-git-baseline-unavailable","checks":[]}`; `task_verify status` → `{"status":"unverified","reason":"no-checks-run"}`. **Not a pass** — reported honestly.
- Manual read-only gates were executed instead: final rc=0, round-6 rc=1 (above).
- GitNexus MCP is available and `list_repos` worked, but **this repository (`glaucus`/`kkicad`) is not among the indexed repos** (grep for `glaucus`/`kkicad` returned nothing). Graph `context`/`impact` was therefore unavailable; I audited callers/consumers with source reads and `rg` instead.
- Documentation consistency: `STRUCTURE.md:43,67` and `README.md:68,72,77` agree with the shipped build (210 pages, ~14.9 MB, 25 bookmarks; 17 mutation cases). `PAPER_IMPROVEMENT_LOG.md:58,60` records the final hash and explicitly explains the historical blocked hash at `:46` and `state.json:173`; the stale `a75f748b` reference from the prior recheck is gone.

## 7. New defects

**None actionable; no new MAJOR or MINOR.** Non-blocking observations are the thin p185 cell padding (§4) and the gate blind spots (§5), neither of which reproduces the two MINORs or introduces a layout regression.

## 8. Verification gaps

- The blocked PDF bytes (`7c185ac3…`, 14,855,636 B) were overwritten; no byte-level gate rerun on that build was possible. Blocked-state evidence is the two archived 140-dpi renders (`p149`, `p191`) plus the synthetic positive test and the source-level cause, not a re-execution on the old binary.
- Direct visual reads covered 7 final pages (142/148/149/156/185/186/191) and 2 archived blocked renders, not all 210 pages; color and crop were not re-verified.
- Caption count 78 is from HTML `fig-no` markup; I did not reconcile every one of the 78 against a raster page (PDF text extraction found 59 narrow-pattern lines).
- `task_verify` returned unverified (no git baseline); gate evidence is from direct invocation only.
- GitNexus graph-based context/impact could not be used (repo not indexed).
- Chapter-ending white space on pp20/38/77 (from the initial review) was not re-measured in this follow-up; whole-book normalized text comparison and overflow scan were clean.

## 9. Recommendation

**Accept / ALLOW — merge.** The river MAJOR and both original MINORs are closed on the shipped artifact; the new gate is meaningful (old-red/new-green, synthetic-positive), CI runs it after the build, and no test was weakened. No rework is required; the residual items above are monitoring notes, not merge blockers.
