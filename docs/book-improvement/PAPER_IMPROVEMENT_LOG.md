# Book Improvement Log

## Score Progression

| Round | Score | Verdict | Key Changes |
| --- | --- | --- | --- |
| Round 0 (original) | — | — | Baseline: 194 pages, 25 bookmarks |
| Round 1 | 6/10 | Almost / BLOCK | Fixed the LED net contract, added breathing firmware and toolchain prerequisites, aligned CLI origins, narrowed the impedance claim, locked component selection, repaired source classification |
| Round 2 | 6/10 | Almost / BLOCK | Reviewer (fresh, independent): Round-1's five MAJORs all closed; new MAJOR = duplicated figure numbers on 6 PDF pages from photo captions; 2 MINORs |

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
