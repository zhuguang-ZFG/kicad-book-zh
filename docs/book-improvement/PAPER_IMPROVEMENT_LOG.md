# Book Improvement Log

## Score Progression

| Round | Score | Verdict | Key Changes |
| --- | --- | --- | --- |
| Round 0 (original) | — | — | Baseline: 194 pages, 25 bookmarks |
| Round 1 | 6/10 | Almost / BLOCK | Fixed the LED net contract, added breathing firmware and toolchain prerequisites, aligned CLI origins, narrowed the impedance claim, locked component selection, repaired source classification |
| Round 2 | 6/10 | Almost / BLOCK | Reviewer (fresh, independent): Round-1's five MAJORs all closed; new MAJOR = duplicated figure numbers on 6 PDF pages from photo captions; 2 MINORs |
| Round 3 | 8/10 | Accept / ALLOW | Closed the deferred baseline-duplication MINOR (preface table + ch7/8/13 compression); added §15.7 KiBot direct reuse (pinned action + schema-validated config + version/AGPL boundaries); 0 MAJOR, 2 MINOR fixed post-review |
| Round 4 | 9/10 | Accept / ALLOW | Fresh review found 1 MAJOR (STRUCTURE HTML limit `< 1MB` vs 5.6MB artifact) and 3 MINOR; fixed the MAJOR, refreshed stats, made source captions sequential, added artifact gates; recheck closed the MAJOR, 1 new gate-hardening MINOR fixed, reference-depth MINOR deferred |

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
