# Book Improvement Log

## Score Progression

| Round | Score | Verdict | Key Changes |
| --- | --- | --- | --- |
| Round 0 (original) | — | — | Baseline: 194 pages, 25 bookmarks |
| Round 1 | 6/10 | Almost / BLOCK | Fixed the LED net contract, added breathing firmware and toolchain prerequisites, aligned CLI origins, narrowed the impedance claim, locked component selection, repaired source classification |
| Round 2 | 6/10 | Almost / BLOCK | Reviewer (fresh, independent): Round-1's five MAJORs all closed; new MAJOR = duplicated figure numbers on 6 PDF pages from photo captions; 2 MINORs |
| Round 3 | 8/10 | Accept / ALLOW | Closed the deferred baseline-duplication MINOR (preface table + ch7/8/13 compression); added §15.7 KiBot direct reuse (pinned action + schema-validated config + version/AGPL boundaries); 0 MAJOR, 2 MINOR fixed post-review |
| Round 4 | 9/10 | Accept / ALLOW | Fresh review found 1 MAJOR (STRUCTURE HTML limit `< 1MB` vs 5.6MB artifact) and 3 MINOR; fixed the MAJOR, refreshed stats, made source captions sequential, added artifact gates; recheck closed the MAJOR, 1 new gate-hardening MINOR fixed, reference-depth MINOR deferred |
| Round 5 | 9/10 | Accept / ALLOW | Added 8 official KiCad screenshots to body chapters (27 total with Appendix A.7), 3 OSS workflow diagrams, screenshot provenance gates and figure-number ordering fix; fresh review found 2 caption/pixel mismatches (1 MAJOR, 1 MINOR), both fixed; recheck 9/10 with 0 MAJOR, 0 MINOR |
| Round 6 | 9/10 | Accept / ALLOW | Fresh technical/reproducibility audit of the 211-page artifact: all CLI flags, DRC semantics, menu paths and 19 Appendix A.7 screenshots verified against KiCad 10.0.8; 0 MAJOR, 1 MINOR (Ch7 omitted the 0.20 mm Default netclass from its 86–138 Ω claim), fixed with an explicit ~146 Ω statement and a new SI mutation; A-19 caption tightened |
| Round 7 | 9 → 6 → 9 | Accept / ALLOW → BLOCK → Accept / ALLOW | Raster audit of all 211 pages of the Round 6 PDF; fixed the lone Ch6 bridge page, the lone appendix-B caveat page, B.2 filename splits and the empty bordered row fragment; initial review 9/10 with 2 MINOR, both fixed; recheck found a new MAJOR (removing `<wbr>` from ~250 inline code tokens created justified-prose rivers on five pages), fixed by restoring soft breaks while keeping B.2 filenames nowrap; river gate added; independent follow-up on the final artifact accepted the fix with 0 MAJOR / 0 MINOR; a CI-only Ch8 orphan was then fixed and the PR rerun passed |

## Vividness Pilot — Chapter 10

- Scope: Chapter 10 opening only. Added a concrete factory-acceptance scene and a hand-drawn “验包台” illustration; kept all commands, technical claims, warnings and section order. Existing Chapter 10 figures were renumbered sequentially to 10-1…10-5.
- Visual contract: the new SVG uses `currentColor`, contains no script/style/id/href/url, and stays below the 24 KB inline limit. README asset counts now report 66 SVGs / 41 teaching illustrations.
- Rebuilt artifact: local PDF remains 210 pages / 25 bookmarks; the scene is on p97 and the new Figure 10-2 on p98; the builder reports 79 plates. Baseline and rebuilt PDFs were compared on the same reading path.
- Verification: `test_claims`, `test_book_metadata`, `test_readme_links`, `check_book`, builder `--check`, and `test_pdf_layout` pass. `task_verify run` remains unverified (`project-or-git-baseline-unavailable`, `checks=[]`).
- Boundary: this is a writing/illustration pilot, not a KiCad GUI or factory-line execution test; the illustration is explicitly labeled as a process schematic.
- Causality correction: the scene now says same-origin Gerber and drill keep holes aligned with pads; only the POS exported with a new origin displaces component placement centers. Rebuilt p97 contains the corrected wording and no longer contains the old “安装孔整体偏离了焊盘” sentence.

## PDF Navigation — Section Bookmarks

- Evidence: the 210-page baseline had 25 bookmarks for 203 article H2 headings. Readers could jump to a chapter but not directly to sections such as “3.6 ERC 的处理循环”.
- Change: `render_unit()` heading IDs now feed `app.assemble_book()` and `PrintManifest.outline`; H2 sections become bookmarks, H3/H4 stay out of the sidebar, and collected editions may nest them at level 4. Unlinked section destinations resolve from their 15.36 pt printed heading blocks. Running heads retain the existing chapter-level labels.
- Verification: old-red/new-green bookmark regression passes (25 → 228; all 203 section labels verified on their heading pages). All 210 rendered pages are pixel-identical to the baseline at 72 dpi. In the actual PDF viewer, expanding Chapter 3 exposes its sections and clicking 3.6 opens p36. `test_claims`, `test_book_metadata`, `test_pdf_cleanup`, `check_book`, `test_pdf_layout`, builder `--check`, and `git diff --check` pass.
- Review hardening: heading-text recovery now receives the explicit H2 `section_ids` set. A probe that removes `kicad-front` leaves it missing while all 203 H2 sections still resolve; an end-to-end `build_pdf()` fixture with a missing non-section anchor raises `no destination found`. The previous fallback silently repaired the removed front anchor.
- Native-outline experiment: installed Chromium 158 reports `CSS.supports("bookmark-level", "1") == false`, and `page.pdf(outline=True)` produces an empty outline on a minimal H1/H2 fixture. The text-position fallback remains necessary, but is no longer allowed to mask missing chapter/part/appendix destinations.
- Boundary: no manuscript text, figure, command, warning, page geometry, version or release artifact changed; generated PDF/HTML remain local and uncommitted.

## Illustration Clarity — Chapter 8 Copper Pour

- Evidence: `kicad-ch08-pour` was the largest teaching SVG but had only two text labels; the dashed zone, 80 stitching-via circles and thermal-relief symbol had no in-figure key.
- Change: added the title “GND 铺铜与缝合过孔” and a three-item symbol key for the copper boundary, stitching vias and thermal pad. Board geometry, via array, MCU, thermal spokes, caption, figure number and 720×300 viewBox are unchanged.
- Budget: the first 20,100-byte build exceeded the renderer’s 20,000-byte inline-plate limit. Shortening the title/key labels and simplifying the legend’s thermal sample reduced the deterministic output to 19,926 bytes; the full PDF build now passes.
- Verification: regenerating twice is byte-identical; only `kicad-ch08-pour.svg` changes. The rebuilt PDF remains 210 pages / 228 bookmarks, and a 72-dpi whole-book comparison isolates the sole render change to p80. `test_claims`, `test_book_metadata`, `check_book`, `test_pdf_layout`, builder `--check`, and `git diff --check` pass.
- Boundary: no manuscript text, technical value, command, warning, section order, version or release artifact changed; generated PDF/HTML remain local and uncommitted.

## Prose De-AI Passes (after Round 7)

### First Pass

- Scope: 12 chapter sources, 28 sentence-level edits. Technical claims, numbers, commands, figures, section order and page structure are unchanged.
- Removed the repeated `不是 X，而是 Y` rhetorical frame (25 occurrences to 0), plus one `真正的` and one `一套完整`; the remaining text states the claim and its condition directly.
- Verification after the edit: content checks OK; local PDF 210 pages, 25 bookmarks, 0 blank pages; `test_pdf_layout.py` OK; builder `--check` OK.

### Second Pass (full book)

- Scope: preface, chapters 1–15 and appendix B; 17 source files, 85 changed lines. Section numbering and page structure are unchanged.
- Removed the remaining contrast frames and emphatic modifiers (`不是 X，而是 Y`, `不是 X，是 Y`, `真正的`, `一套完整`), renamed headings that used those frames, and replaced stage, reservoir and contract metaphors with direct technical statements.
- Kept negations that distinguish real failure modes, including plain-text versus binary project files, optional 3D models, two-layer boards without impedance control, and DRC exclusions that do not repair geometry.
- Verification after the edit: pattern scan 0; content checks OK; local PDF 210 pages, 25 bookmarks, 0 blank pages; `test_pdf_layout.py` OK; builder `--check` OK.

## Round 7 Cross-Checks (before review)

- **Scope**: print layout only. The Round 6 artifact was rasterized into fourteen 4×4 contact sheets and every page was inspected; suspect pages were re-rendered at 110–140 dpi. No new technical, electrical or sourcing claims were added.
- **Old artifact**: `kicad-book-zh-round6.pdf`, 211 pages, MD5 `1d75b07c951fcdc08e5914595fc6c7bd`.
- **Lone tail pages (accepted defects)**: page 68 carried only the Ch6 bridge sentence plus the closing mark; page 192 carried only the final "未决问题" bullet of appendix B. Both left more than 85% of the sheet blank.
- **B.2 table (accepted defects)**: the first column was squeezed until `.kicad_pro`, `.kicad_sch`, `.kicad_pcb`, `sym-lib-table`, `fp-lib-table` and `.kicad_sym` printed as two lines. Page 186 also ended with an empty bordered row strip before the next sheet.
- **Intentional short pages (not defects)**: cover, version page, reading paths, TOC tail, part doors (13/49/96/132), photo and screenshot plates, chapter-end citation cards (31/58/77/129/142/151/167), and the final colophon page. Their previous page had no room for the whole block; splitting the citation card or padding with filler would be worse.
- **False positives rejected**: pages 76→77 and 104→105 first looked like split tables on the contact sheet; 140 dpi renders showed complete rows and repeated headers. B.2 already had a repeated `<thead>`; the defect was column width, not a missing header.
- **Gate**: `tools/test_pdf_layout.py` fails the untouched Round 6 PDF with all four checks: `pages with a lone body sentence/bullet: [68, 192]`, B.2 split/missing filename tokens, a missing complete row/header structure, and `appendix B.2 empty card strips: [(186, 39.9)]`. It passes the rebuilt PDF. The gate runs after the PDF build because it reads the artifact, not the sources; an optional path argument allows the same check against the old fixture.
- **Gate hardening after review**: the gate now asserts one B.2 header and one complete row per filename, measures the bordered card against its last text row (20 pt tolerance; the old fragment was 39.9 pt), narrows the image exemption to images covering at least 20% of the page, and exempts citation pages only when the citation block starts the page.

## Round 7 Review

Full raw review, verbatim: [round-7-review.md](round-7-review.md).

- **Initial fresh review: 9/10, Accept / ALLOW, 0 MAJOR, 2 MINOR, confidence 0.88.**
- Independently confirmed no content loss: the Ch6 bridge moved from old p68 to new p67 and the appendix-B caveat from old p192 to new p185; the bridge and closing mark do not collide. B.2 prints as a header + 8 rows on p185 and a header + 6 rows on p186, with all 14 filenames intact and no empty band.
- MINOR 1: the new layout gate guarded only two of the four repaired defects. It did not assert per-card header/row counts, an empty bordered strip, chapter-end crowding, or rows after B.3; its image and citation exemptions were broad.
- MINOR 2: moving the caveat dropped `未决问题：`, `每种文件的`, and precision in the `.pretty/` and `.kicad_dru` cells. The meaning and placement were still correct.

### Fixes After the Round-7 Review (same session)

1. **Layout-gate coverage (MINOR 1)** — `tools/test_pdf_layout.py` now requires exactly one B.2 header per card, all 14 complete filename rows, and measures the bordered card to its last text row (20 pt tolerance; the old strip was 39.9 pt). The image exemption requires an image covering at least 20% of the page; the citation exemption requires the citation block to start the page. The old Round 6 PDF still fails the strengthened gate.
2. **Caveat precision (MINOR 2)** — restored `未决问题：`, `每种文件的`, `.pretty/` as `目录（含 .kicad_mod 文件）`, and `.kicad_dru` as `针对某个 .kicad_pcb 的自定义设计规则`. Literal restoration alone reproduced a lone `）` line and split `自定义` into `自` / `定义`; the final wording adds the noun `文件` and marks `自定义` with a print-only nowrap span. The B.2 filenames remain `<code class="nw">`.

### Round 7 Recheck

Full recheck, verbatim: [round-7-recheck.md](round-7-recheck.md).

- **6/10, BLOCK, 1 new MAJOR, 0 new MINOR, confidence 0.90.** Both original MINORs were accepted as fixed, including the gate's old-red/new-green behavior and the restored caveat wording.
- The recheck's artifact was the **blocked** build `7c185ac33d9400fc07865b9f391fa43b` (210 pages, `14,855,636 B`), not the final artifact below.
- New MAJOR root cause: adding `"code"` to `_NAME_BREAK_SKIP` stopped `soften_long_names()` from inserting `<wbr>` into roughly 250 inline code URLs/paths. Chromium could no longer break those tokens, so it pushed them to the next line and stretched the preceding justified CJK prose. The recheck measured holes of 96.6 pt and 43.5 pt and saw the defect on p142, p148, p149, p156 and p191. Round 6 did not have this regression.
- The recheck also noted that the gate had no assertion for this river class, so a green gate did not prove the prose was clean.

### Fixes After the Round-7 Recheck

1. **Restore soft breaks (MAJOR)** — removed `"code"` from `_NAME_BREAK_SKIP`; inline code again receives `<wbr>`. B.2 filenames still stay on one line because their table-specific `<code class="nw">` plus print CSS wins. No B.2 token regressed.
2. **End-to-end river assertion** — `tools/test_pdf_layout.py` now clusters PyMuPDF `rawdict` line fragments by baseline, skips filled table-card containers, and fails prose lines whose fragment gaps exceed 3.5 pt. On the blocked build it reports exactly the five affected pages; on the final build it reports none. A synthetic spaced-CJK page fails and a contiguous-CJK page passes, proving the detector can fire rather than merely staying silent.
3. **Rebuild** — final build completed in 58.69 s; 210 pages, 25 bookmarks, 0 blank pages, 78 unique captions. The layout gate and all source/content gates pass. `p191` keeps `三份核心文件同时创建、备份目录：` together and breaks the URL at `/` instead of stretching the lead-in.

### Round 7 Follow-up Recheck

Full follow-up report, verbatim: [round-7-recheck-2.md](round-7-recheck-2.md).

- **9/10, Accept / ALLOW, 0 new MAJOR, 0 new MINOR, confidence 0.90.** The follow-up independently verified the final artifact hash, not the blocked build.
- The river MAJOR is closed: an independently reimplemented baseline-cluster detector found zero prose clusters on pp142/148/149/156/191, glyph advances are 10.2–11.98 pt (blocked build ~21 pt), and 140-dpi A/B renders show normal prose on the final pages versus stretched blocked pages. Whole-book candidates were confined to filled table cards.
- Both original MINORs remain fixed: B.2 has one 5-column header + 8 rows on p185 and one header + 6 rows on p186, all 14 filenames on one line, no lone closing parenthesis, and a 9.6 pt card padding strip versus the historical 39.9 pt gap.
- The new gate is meaningful: final PDF rc=0, Round 6 rc=1 with the expected old defects, synthetic spaced-CJK fires at 22/25/30 pt gaps and contiguous CJK does not. No assertion was weakened. CI runs the gate after the build.
- Normalized text ratio against Round 6 is 0.9996; no content deletion. Residual detector blind spots are documented in the report and are not merge blockers.

### Round 7 CI Follow-up

- PR [#11](https://github.com/zhuguang-ZFG/kicad-book-zh/pull/11) first run `45771597642` failed only in `test_pdf_layout.py`: `pages with a lone body sentence/bullet: [85]`. On Ubuntu with `fonts-noto-cjk`, Ch8's transition sentence and the closing mark occupied CI p85 alone (89 extracted characters); the local Windows/Chrome build kept the whole Ch8 tail on one page and passed.
- The gate was correct, not a false positive. `.ch-close` glues the bridge paragraph and ornament with `break-inside:avoid`; on CI p84 the preceding acceptance list's trailing margin plus the paragraph leading made the 39 pt pair a few points too tall for the 51 pt left below the last text.
- Repair: `.chapter-body > :has(+ .ch-close){margin-bottom:0}` and `.ch-close p:first-child{margin-top:0}`. The closing mark keeps its size; no content, short-page exemption, threshold or test assertion was changed.
- Rebuilt local artifact: **210 pages, 25 bookmarks, 0 blank pages, 78 unique captions**, `14,863,999 B`, MD5 `a0d5f4529c511bce31d2f7cc2a241e48`; HTML `6,622,216 B`. The full local gate set passes. Pages 67, 85, 142 and 191 were re-rendered at 110–130 dpi; the closing marks remain separate from the preceding text and the intentional short pages are unchanged.
- CI rerun `45776337209` succeeded. Its artifact has **209 pages**, 25 bookmarks and 0 blank pages (the CI font stack absorbs the former p85, while the archived Chrome build stays at 210); Ch8 now closes on CI p84 and B.2 occupies pp184–185. The same layout gate passes, so the repair is verified against both font stacks.
- The pre-repair `4ee2494704c2f2135901fc47849ed284` build is the 210-page artifact independently accepted by the follow-up. This repair only removes the margin before the closing mark; the river and B.2 evidence remains valid and the follow-up report intentionally retains the old hash.

## Round 7 Artifacts

- Final local artifact: `yuyu-book/dist/kicad-book-zh-round7.pdf` — **210 pages, 25 bookmarks, 0 blank pages, 78 unique captions**, `14,863,999 B`, MD5 `a0d5f4529c511bce31d2f7cc2a241e48`.
- HTML: `6,622,216 B`, 20 units, 78 plates, 44 cited links.
- CI artifact from rerun `45776337209`: **209 pages, 25 bookmarks, 0 blank pages**, `26,378,991 B`, MD5 `1689331ed1266d3479b449f0bffdefe4`; Ubuntu Noto CJK pagination, same sources and gates.
- The earlier `7c185ac33d9400fc07865b9f391fa43b` build is the blocked recheck artifact; it was replaced in the archive after the river fix. The recheck report intentionally retains that historical hash.
- Local archive: Ch6 closes on page 67; B.2 occupies pages 185–186 as two table cards split at the core/optional boundary; appendix B ends on page 191, and appendix C starts on page 192. CI pagination is one page shorter: B.2 on pp184–185.
- Gates: `test_claims`, `test_usb_diagnostics`, `test_readme_links`, `test_book_metadata`, `test_pdf_cleanup`, `test_si_numbers` (17 mutations), `check_book`, `test_pdf_layout`, and builder `--check` all OK.
- `task_verify run` returned `unverified` / `project-or-git-baseline-unavailable`; no operator-configured check was executed. The commands above are the recorded manual evidence.
- Build used the installed Chrome; 70.63 s for the repaired local PDF.

## Round 6 Cross-Checks (before review)

- **Scope**: independent technical/reproducibility audit of the 211-page Round 5 artifact, not a new editorial expansion. Priorities: quantitative claims, KiCad 10.0.8 CLI/menu correctness, acceptance observability, pixel-level screenshot captions, and source/license boundaries.
- **Quantitative audit**: recomputed IPC-2221 widths, 30 mm/0.30 mm voltage drop, 2 A/3 A temperature extrapolations, `BW=0.35/RT` thresholds, microstrip impedances, 3h/3w rules, θJA and the Ch13 bias values; all matched except the cross-chapter impedance range below.
- **KiCad 10.0.8 operation**: every CLI flag used in the book exists in `tools/_cli10.txt`; `--exit-code-violations` semantics, `--refill-zones`/`--save-board` pairing, DRC menu paths and appendix hotkeys match the official 10.0 manuals.
- **Acceptance sections**: all 15 chapters have observable acceptance items that work with a reader-built project; none depends on shipped KiCad project files.
- **Appendix A.7 screenshots**: all 19 captions were pixel-compared against the images (title, tab, panels, values); zero mismatches. A-19's "走线角度" wording was noted as broader than the visible grayed `Free angle mode`, but the checkbox is angle-related, so it was not counted as a defect.
- **Sources/license**: `sources.json` and `screenshots/README.md` agree on the KiCad 10.0.8 snapshot, access date, and CC BY 3.0 / GPLv3+ boundary; no license mixing with the MIT/AGPL OSS tools.

## Round 6 Review

Full raw review, verbatim: [round-6-review.md](round-6-review.md).

- **Initial fresh review: 9/10, Accept / ALLOW, 0 MAJOR, 1 MINOR, confidence 0.82.**
- MINOR (confidence 0.65): Ch7 §7.3 and the summary claimed the board's ordinary tracks are 86–138 Ω, but Ch5 §5.4's `Default` netclass is 0.20 mm. The table starts at 0.25 mm, so the 0.20 mm default was outside the stated range; the same microstrip estimate gives ~146 Ω.
- The review explicitly did not re-adjudicate the Round 5 §7.4/§13.4 caption items and did not do a 211-page raster pass; those remain stated verification gaps, not new failures.

### Fixes After the Round-6 Review (same session)

1. **Ch7 default-width inconsistency (MINOR)** — §7.3 now says the 0.25–1.0 mm table corresponds to 86–138 Ω, while §5.4's 0.20 mm `Default` netclass is ~146 Ω under the same approximation; the summary states the same split. `check_si_numbers()` now recomputes the 0.20 mm / 1.5 mm value and rejects a mismatch; `test_si_numbers.py` adds a `146 → 50 Ω` mutation, raising the suite to 17 mutations.
2. **A-19 caption precision (advisory)** — the caption now names `Highlight collisions` / `Shove` / `Walk around` and says `Free angle mode` is grayed because `Shove` is selected, matching the screenshot instead of the broader "走线角度" wording.

### Round 6 Recheck

- **9/10, Accept / ALLOW, 0 MAJOR, 0 MINOR, confidence 0.92.**
- F1 fixed: independent recomputation gives 0.20 mm → 146.23 Ω, 0.25 mm → 137.78 Ω, 0.5 mm → 111.69 Ω, 1.0 mm → 86.15 Ω; both the §7.3 prose and the summary now separate the 0.20 mm default from the 0.25–1.0 mm range, and the PDF text layer carries the new sentence on pages 74 and 78.
- A-19 fixed: the caption matches the screenshot (three Mode choices, `Shove` selected, `Free angle mode` grayed) and the KiCad 10 manual entry; no stale "走线角度" claim remains.
- Artifact: 211 pages, 25 bookmarks, 0 blank pages, 78 unique captions; `round6.pdf` MD5 matches the built PDF.
- The recheck noted a robustness gap: the new gate used `re.search` and only validated the first `0.20 mm … Ω` occurrence. `check_si_numbers()` now uses `re.findall` and validates every occurrence, so the body and summary cannot drift apart; both gate runs stay green and the 17-mutation suite still passes.

## Round 6 Artifacts

- Final artifact: `yuyu-book/dist/kicad-book-zh-round6.pdf` — **211 pages, 25 bookmarks, 0 blank pages, 78 unique captions**, `14,886,118 B`.
- HTML: `6,617,230 B`, 20 units, 78 plates, 44 cited links.
- New Ch7 text is on PDF page 74 (§7.3) and page 78 (summary); A-19 is on page 184.
- Gates: `test_claims`, `test_usb_diagnostics`, `test_readme_links`, `test_book_metadata`, `test_pdf_cleanup`, `test_si_numbers` (17 mutations), `check_book`, and builder `--check` all OK.
- Build used the installed Chrome; 66.56 s.

## Round 5 Cross-Checks (before review)

- **Scope**: Round 5 adds real UI recognition to the body chapters and three workflow illustrations for GitHub-hosted open-source tools; it does not add a new electrical claim or a new manufacturing step.
- **Official screenshots**: 8 body screenshots inserted (Ch3 ERC marker, Ch4 CvPcb, Ch5 Board Setup layers, Ch7 length tuning, Ch9 DRC rule editor, Ch10 drill dialog, Ch13 simulator, Ch15 PCM repository); Appendix A.7 keeps its 19 screenshots. Total 27, each with a `screenshots/README.md` source row, access date 2026-11-26, and the official docs license note (CC BY 3.0 / GPLv3+).
- **Captions are checked against the pixels**: the drill screenshot still shows `Origin: Absolute`, so the caption explicitly tells the reader to switch to `Plot / Drill / Place` for `--drill-origin plot`; the simulator screenshot is an official AC-sweep example, not this board's RC result; the PCM screenshot's detail pane is KiBuzzard while iBOM/KiKit are visible in the list. No screenshot is presented as a local capture.
- **OSS workflow illustrations**: `kicad-ch11-ibom` (MIT), `kicad-ch11-kikit` (MIT), and `kicad-ch15-kibot` (AGPL-3.0) are hand-drawn diagrams, not screenshots; captions state the license and that KiKit spacing/array is illustrative, not a process parameter. KiBot is still schema-validated only because no local Docker was available.
- **Figure-number regression**: a raw HTML screenshot or Markdown photo between two `ill` fences shifted later diagram numbers. `render.py` now calls `renumber_figures()` before `absorb_ill_captions()` via `finalize_figures()`; without this, an H2 placeholder caption stayed in the figure and the real caption became a duplicate paragraph.
- **New gates**: `check_book.py` parses `<span class="fig-no">` captions in source order and verifies every embedded screenshot exists, is non-empty, has a provenance row, and that no shipped screenshot is unreferenced. Three regressions cover the HTML-only numbering hole, the provenance row requirement, and caption absorption after a photo/screenshot shift.
- **Stats**: README refreshed to 15.8 万字符 / 6.2 万汉字, 65 SVG assets, 40 teaching illustrations, 10 photos, 27 screenshots, HTML ~6.6 MB, PDF 211 pages / ~14.9 MB; `STRUCTURE.md` HTML ceiling stays `< 8MB`.

## Round 5 Review

Full raw review, verbatim: [round-5-review.md](round-5-review.md).

- **Initial fresh review: 6/10, Almost / BLOCK, 1 MAJOR, 1 MINOR, confidence 0.88.**
- MAJOR: Ch7 图 7-4 caption said "图示为单线蛇形；差分对要两根一起调", but the official screenshot actually shows **two parallel traces meandering together** — the caption reversed the section's differential-pair lesson. The body steps were correct.
- MINOR: Ch13 图 13-3 caption reversed the simulator layout: the waveform is on the left; Signals is top-right and Cursor/Measurement bottom-right. The same chapter's body already said the cursor table is on the right.
- Independently confirmed the other 6 body screenshots, 27 provenance rows, 78 unique captions, 211 pages / 25 bookmarks / 0 blanks, and the MIT/AGPL boundaries. No screenshot was presented as a local capture.

### Fixes After the Round-5 Review (same session)

1. **MAJOR — differential-pair tuning caption** — Ch7 图 7-4 now says "图示为两根并行走线同时蛇形调谐，即差分对；单端才只调一根". Screenshot and body unchanged.
2. **MINOR — simulator layout** — Ch13 图 13-3 no longer makes a left/right claim; it now says "界面同屏显示波形、信号列表与测量表" and still explicitly labels the image as the official AC-sweep example, not this board's RC result.

### Round 5 Recheck

- **9/10, Accept / ALLOW, 0 MAJOR, 0 MINOR, confidence 0.92.** Full recheck: [round-5-recheck.md](round-5-recheck.md).
- Verified both corrected captions word-for-word against the rebuilt PDF p75/p138 and the screenshot pixels; the simulator caption now makes no left/right claim, so it cannot contradict the image or the chapter's "cursor table on the right" sentence.
- Reconfirmed 211 pages / 25 bookmarks / 0 blank pages and 78 unique built captions (including appendix `图 A-N`). No screenshot files changed; provenance, licenses and MIT/AGPL boundaries still hold.

## Round 5 Artifacts

- Final artifact: `yuyu-book/dist/kicad-book-zh-round5.pdf` — **211 pages, 25 bookmarks, 14,883,630 B**; 0 blank pages; 78 unique built captions.
- HTML: `6,616,941 B`, 20 units, 78 plates, 44 cited links.
- Verified pages: 37 (new ERC marker), 43 (CvPcb), 53 (Board Setup layers), 75 (length tuning), 93 (DRC rule editor), 101 (drill dialog), 114 (iBOM), 116 (KiKit), 139 (simulator), 158 (PCM), 162 (KiBot).
- Gate: `test_claims`, `test_usb_diagnostics`, `test_readme_links`, `test_book_metadata`, `test_pdf_cleanup`, `test_si_numbers` (16 mutations), `check_book`, and builder `--check` all OK.

### Post-merge Advisory Corrections

- **Ch5 图 5-2 layer count** — the caption said layer count was defined on Board Editor Layers. Official KiCad 10 `pcbnew` docs put the copper-layer count on **Physical Stackup** (upper left); Board Editor Layers only manages layer type, name and enable state. Caption corrected; the screenshot's `F.Cu` / `In1.Cu…In4.Cu` / `B.Cu` rows are described as the current layer list, not as proof that the stackup is complete.
- **Ch13 图 13-3 placement** — the screenshot is an `Analysis 1 - AC` sweep, so it was moved out of §13.4 (TRAN) into §13.5 (AC). The caption now says the official AC example is not this board's RC result and reads "波形、Signals 与 Cursor 同屏"; no left/right claim remains. Final PDF page 139.
- **Regression scope** — `test_figure_caption_absorbs_after_photo_shift` already builds two preceding photo figures, an `ill` placeholder numbered 5-2 whose real caption says 5-3, calls `finalize_figures`, and asserts the real caption is inside `figcaption` with the duplicate paragraph gone. No test change was needed.
- Rebuilt after the corrections: **211 pages, 25 bookmarks, 0 blank pages, 78 unique captions**; all gates green.

## Round 4 Review

Full raw review, verbatim: [round-4-review.md](round-4-review.md). Post-fix recheck: [round-4-recheck.md](round-4-recheck.md).

- **Initial fresh review: 8/10, Almost / BLOCK, 1 MAJOR, 3 MINOR, confidence 0.84.**
- MAJOR: `STRUCTURE.md:95` claimed the HTML build was `< 1MB`; the actual single-file artifact was `5,599,223 B` (~5.6MB) and README already claimed ~5.6MB. The claim was false and had no regression check.
- MINOR: README word counts were stale (`14.9 万字符 / 6.0 万汉字` vs measured `154,676 / 61,094`); source hand-written figure numbers were duplicated/out of order in ch4/6/10/12 although the renderer renumbered them; technical references remained mostly docs-level.
- Independently verified the shipped artifact: 205 pages, 25 bookmarks, 0 blank pages, 13,971,714 B; then found `manifest.json` still said `v0.1.3 / 2026-11-25` while the PDF imprint and README said the 2026-11-26 build.

### Fixes After the Round-4 Review (same session)

1. **HTML size claim (MAJOR)** — `STRUCTURE.md` now says `HTML 构建大小 < 8MB（当前约 5.6MB）`; `tools/check_book.py` checks the README claim against both the STRUCTURE limit and the actual artifact; `tools/test_book_metadata.py` asserts the claim is below the limit.
2. **Stale stats (MINOR)** — README now says `约 15.5 万字符（6.1 万汉字`; `check_readme_stats()` now counts exactly the 20 manifest-ordered book sources via `book_sources()`, so `.tmp`, `docs/`, and `book-improvement` cannot inflate the count.
3. **Source figure numbers (MINOR)** — ch4 BOM `图 4-3` → `图 4-4`; ch6 floorplan/decoupling/antenna `6-1/6-2/6-3` → `6-2/6-3/6-4`; ch10 CLI `10-2` → `10-3`; ch12 bring-up/voltage/fault-tree `12-1/12-2/12-3` → `12-2/12-3/12-5`. Added `source_figure_number_problems()` + regression so source captions must be `1..N` per chapter even though the renderer renumbers.
4. **Edition metadata** — `yuyu-book/manifest.json` bumped to `0.1.4 / 2026-11-26`; rebuilt PDF/HTML show the new imprint.
5. **Gate hardening after recheck (MINOR)** — `check_artifact_claims()` now errors when README claims an HTML size but STRUCTURE has no limit or `dist/` has no HTML artifact; both cases have regressions.

### Round 4 Recheck

- **9/10, Accept / ALLOW, 0 MAJOR, 2 MINOR, confidence 0.90.**
- Confirmed `STRUCTURE.md` limit 8MB > README claim 5.6MB > actual 5.59965MB; PDF 204 pages / 25 bookmarks / 0 blank pages; manifest and PDF imprint both `v0.1.4 / 2026-11-26`; 67 unique built figure numbers (48 numeric + 19 appendix) with zero duplicates; README stats match 154,676 chars / 61,094 han.
- One new low-priority MINOR (HTML gate silently passed when the artifact or STRUCTURE limit was missing) was fixed after the recheck; the third original MINOR (technical-reference depth) remains deferred because no concrete factual error was found.

## Round 4 Artifacts

- Final artifact: `yuyu-book/dist/kicad-book-zh-round4.pdf` — **204 pages, 25 bookmarks, 14.0 MB**; 0 blank pages; 67 unique figure numbers (48 numeric + 19 appendix), 0 duplicate captions.
- Page count moved 205 → 204 because making source captions match the renderer let the caption-absorption pass remove a duplicate caption paragraph; all chapters, appendices, and bookmarks remain.
- HTML: `5,599,650 B` (~5.6MB), 20 units, 67 plates, 44 cited links.
- Final gate: `test_claims`, `test_usb_diagnostics`, `test_readme_links`, `test_book_metadata`, `test_si_numbers` (16 mutations), `check_book`, and builder `--check` all OK.
- Build used the installed Chrome via `--browser "C:/Program Files/Google/Chrome/Application/chrome.exe"`; 71.77 s.

### Post-merge Correction (PDF browser cleanup)

- `yuyu_book/pdf.py:_print_pdf()` now closes the launched browser in a `finally` block. Previously `launched.close()` ran only after a successful `page.pdf()`; a print failure left Chromium alive, which matches the observed `Page.printToPDF: Printing failed` followed by a hung retry.
- Added `tools/test_pdf_cleanup.py`: a fake Playwright page raises from `pdf()` and asserts the browser still closes; wired into CI and the STRUCTURE pre-commit list.
- Success path re-verified after the change: PDF 204 pages, 25 bookmarks, 0 index folios; all checks green.

## Round 3 Cross-Checks (before review)

- **Baseline duplication (deferred Round-2 MINOR #3)**: added `## 基线范围与可选扩展` to `00-前言.md` as the single table for schematic/PCB/manufacturing/verification baseline vs optional extensions; compressed the reading path and restatements in `07-布线.md`, `08-铺铜与电磁兼容.md` §8.5–8.7, and `13-仿真与电路验证.md` §13.6. Kept every safety, negative-relation and measurement-boundary sentence, including §8.7's "本板无射频模块，此项不适用".
- **GitHub OSS reuse (KiBot)**: pinned upstream facts by direct fetch, not by memory: KiBot `v1.9.1` annotated tag → commit `8a5106ecdbdaa0057255496fe768766df493221d`; GitHub Action `v2_k10` annotated tag → commit `5c78b746f9076d54242aeeeae7f364f360e21f30`; action inputs `config`/`schema`/`board`/`dir` confirmed in `action.yml`; action Dockerfile still uses `ghcr.io/inti-cmnb/kicad10_auto_full:latest`; image `/etc/kiauto_tag` = `1.9.1-2_k10.0.5_d13.2_b4.2.4LTS` (KiCad 10.0.5, not the book's 10.0.8); index digest `sha256:96e75f885b15617c6b38aef11db7856a93f4367cab7a0b6c2b30465557619330`.
- **Config validation**: extracted the chapter's `.kibot.yaml` and validated it against the official KiBot v1.9.1 schema with `jsonschema` Draft7 → 0 errors; workflow YAML parses; `${QUANTITY}` confirmed against upstream `ColumnList.COL_QUANTITY`. No Docker locally, so the pipeline was **not** executed; the book states this boundary explicitly.
- **Stats gate**: `tools/check_book.py` `md_files()` now excludes `.tmp`, so downloaded CLI/reference Markdown cannot inflate the manuscript word count; README refreshed to 205 pages / 14.0 MB / 16 SI mutation cases.

## Round 3 Review

Full raw review, verbatim: [round-3-review.md](round-3-review.md).

- **Score: 8/10**, **Verdict: Accept**, **Merge: ALLOW**, 0 MAJOR, 2 MINOR, confidence 0.88.
- Independently confirmed the Round-2 figure-number MAJOR stays closed in the shipped 205-page PDF (48 unique figure numbers, 0 duplicates), and that the baseline de-duplication preserved all safety/negative/measurement boundaries.
- Independently verified the KiBot action tag/SHA, inputs, schema strictness (bogus-key injection), image tag and AGPL wording.

### Fixes After the Round-3 Review (same session)

1. **KiBot `dir` is a prefix (MINOR)** — action input changed from `dir: fab` to `dir: .`; the prose now says it is an output prefix concatenated with each output's `dir`, so `fab/gerbers` and `fab/` stay as documented instead of becoming `fab/fab/...`.
2. **Ch2 still restated the baseline (MINOR)** — `02-原理图第一笔.md` now points to the preface table and keeps only the chapter-local instruction ("本章只画最小系统") plus the optional-expansion note.

### Post-merge Correction (zone-fill semantics)

- An aggregated advisory flagged that the mapping bullet conflated two KiBot preflights. Upstream v1.9.1 source confirms it: `pre_check_zone_fills.py` fills zones in memory, leaves the original PCB unchanged, and does **not** fail on fill changes (the `CheckZoneFill` internal template is the gate); `pre_fill_zones.py` refills and saves the board. The bullet now maps `fill_zones` to `--refill-zones --save-board` and states that `check_zone_fills` is not a gate; `CheckZoneFill` is not enabled in this config.
- The same advisory batch repeated an ENTRYPOINT warning already corrected upstream: the base `kicad10_auto_full` image has `Entrypoint: null`, `Cmd: ["bash"]`, so the book's `docker run … bash -lc` version check is valid. `/entrypoint.sh` belongs to the action's derived image, not this command. No change made.
- Rebuilt the PDF after the correction: 205 pages, 25 bookmarks, 14.0 MB; 0 blank pages; 0 duplicate figure numbers; all checks green.

## Round 3 Artifacts

- Final artifact: `yuyu-book/dist/kicad-book-zh-round3.pdf` — **205 pages, 25 bookmarks, 14.0 MB**, rebuilt after both MINOR fixes.
- PDF text-layer re-check: **0 blank pages**; 48 unique figure numbers, **0 duplicate numbers**, including the Round-2 regression set.
- Preface baseline table on page 9; Ch2 pointer on page 21; Ch7 pointer on page 67; KiBot `dir: .` and "输出前缀" explanation on page 157.
- HTML: 5.6 MB, 20 units, 67 plates, 44 cited links — unit/plate counts unchanged from Round 2.
- Final gate: `test_claims`, `test_usb_diagnostics`, `test_readme_links`, `test_book_metadata`, `test_si_numbers` (16 mutations), `check_book`, and builder `--check` all OK.
- Build note: the bundled Chromium raised `Page.printToPDF: Printing failed` once and then hung on retry; the final build used the installed Chrome via `--browser "C:/Program Files/Google/Chrome/Application/chrome.exe"` and completed in 107 s.

## Round 2 Cross-Checks (before review)

- **zlib reference book**: keyword search was denied by the z-library EAPI endpoint on four domains with and without proxy (quota/rate limit); downloads, history and `most-popular`/`recommended` stayed functional. Followed the alternative-evidence rule: downloaded Stephen H. Hall, Garrett W. Hall et al., *High-Speed Digital System Design — A Handbook of Interconnect Theory and Design Practices* from the `recommended` list (z-lib ID `526825:e26d15`) into the gitignored `.tmp/reference-books/` (reference use only, never distributed with the book).
- **Propagation-delay figures (ch 7/8)**: Hall gives FR4 stripline ≈ 174 ps/in (≈ 6.85 ps/mm) and microstrip ≈ 142.6 ps/in for εr = 4.2; the book's "FR4 上约 6.7 ps/mm" is the same family, already labeled an estimate — no correction needed.
- **CLI origin flags (§10.2–10.4, §15.2, §15.6)**: KiCad 10.0.8 source (`kicad/cli/command_pcb_export_drill.cpp` in the GitHub mirror) confirms `pcb export drill --drill-origin` accepts `absolute` (default) | `plot` — the book's `--drill-origin plot` is valid; official KiCad 10 CLI docs confirm `pcb export gerbers --use-drill-file-origin` and `pcb export pos --use-drill-file-origin`. The Round 1 CLI fix is correct, not a regression.

## Round 2 Review

Full raw review, verbatim: [round-2-review.md](round-2-review.md).

### Fixes After the Round-2 Review (same session)

1. **Duplicated figure numbers (MAJOR)** — root cause: `photo_figures()` in `yuyu-book/yuyu_book/render.py` stripped hand-written caption numbers with `^图(?:[A-Za-z]|\d+)-\d+`, which does not tolerate the space in captions like `图 12-1：…`; the printed figure then showed the fig-no span AND the caption number. Fix: strip regex now tolerates the space (`^图\s*(?:[A-Za-z]|\d+)-\d+`). `tools/test_book_metadata.py::test_photos_share_document_order_figure_numbers` extended with two assertions that fail on the old behavior (spaced caption number must be stripped from fig-cap). Affected pages 42/58/98/116/119/124 (图4-3/6-1/10-2/12-1/12-4/12-6) re-verified after rebuild.
2. **upload-artifact v4/v7 conflicting registry entries (MINOR)** — the chapter only uses `@v7`; the uncited `github-actions-upload-artifact` (v4) entry was removed from `sources.json`; the v7 entry already covers the v5/v6 version notes the chapter cites.
3. **Cross-chapter repeated baseline reminders (MINOR)** — editorial scope (baseline table in preface + per-chapter de-duplication pass); deliberately left for the next round rather than half-implemented.

## Round 2 Artifacts

- After Round 1 fixes (state at review time): 201 pages (+2 vs Round 1, breathing-firmware and selection-lock additions), 25 bookmarks.
- After the figure-number fix and rebuild (final Round 2 artifact): `yuyu-book/dist/kicad-book-zh-round2.pdf` — 200 pages, 25 bookmarks (one page shorter: duplicated caption text no longer printed). Text-layer re-check: 图4-3/6-1/10-2/12-1/12-4/12-6 each appear on exactly one page (42/58/98/116/119/124), no same-page duplicates.
- HTML: 5.6 MB, 20 units, 67 plates, 43 cited links — identical unit/plate/link counts to Round 1, no layout regression.

## Round 1 Review

Full raw review, verbatim: [round-1-review.md](round-1-review.md).

### Fixes Implemented

1. **LED net contract** — removed the LED branch from `+3V3`; `LED` now explicitly joins PB3 and the series resistor. Added `led_net_problems()` and a regression test.
2. **Breathing project deliverable** — kept `blink.c` as bring-up diagnostics, added a 64-level software-PWM `breath.c`, nominal frequency/period calculation, build/flash commands, and visual acceptance criteria. Added toolchain installation/version checks and a firmware contract gate.
3. **CLI coordinate origin** — added `--use-drill-file-origin` to the §15.2 Gerber command and `--drill-origin plot` to the drill command. Added a three-command origin contract test.
4. **Impedance claim calibration** — changed “two-layer boards are not 50 Ω” to “these board line widths are not 50 Ω”; documented that two-layer boards can reach a target impedance with suitable width/dielectric/process.
5. **Reproducibility prerequisites** — added a pre-layout selection-lock table for USB-C, fuse, LDO, LED and MCU; README now says the workflow is reproducible while critical part selection is locked by the reader.
6. **Source integrity** — added ATtiny25/45/85, AVRDUDE 8.1 and AVR GCC sources; moved KiCad official libraries and KLC into a new “官方库与指南” group instead of “社区材料（非规范）”.
7. **Statistics scope** — excluded `docs/book-improvement/` from book-source counts so review logs cannot inflate manuscript statistics.

## Round 1 Artifacts

- Baseline: `yuyu-book/dist/kicad-book-zh-round0.pdf` — 194 pages.
- After Round 1: `yuyu-book/dist/kicad-book-zh-round1.pdf` — 199 pages, 25 bookmarks.
- HTML: 5.6 MB; PDF: 13.9 MB.

## Reviewer Transport

The upstream ARIS skill targets Claude Code/Codex MCP. This Pi run used fresh read-only `reviewer` subagents with the same independence rule: primary artifacts only, no executor summary, no prior review, no fix list. Actual model identity was not independently verified; no cross-family acceptance is claimed.
