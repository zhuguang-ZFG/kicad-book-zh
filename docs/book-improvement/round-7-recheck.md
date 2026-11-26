# Round 7 — Independent Recheck

- **Score: 6/10** (down from the original review's 9/10, solely because of one new MAJOR regression)
- **Verdict: BLOCK — rework required before acceptance**
- **MAJOR: 1 (new, patch-introduced)** · **MINOR: 0 new** · the two original MINORs: **both FIXED**
- **Confidence: 0.90** on the new MAJOR (minimal reproduction, round6 A/B, vector geometry, and the author's own post-build raster all agree); 0.82 on overall verdict; 0.65 on the exact timing *within* the round when the regression was introduced (see Verification gaps).

Artifact judged first-hand: `yuyu-book/dist/kicad-book-zh.pdf` == `kicad-book-zh-round7.pdf`, **210 pages, 14,855,636 B, MD5 `7c185ac33d9400fc07865b9f391fa43b`**, 25 bookmarks, 0 blank pages. Baseline: `kicad-book-zh-round6.pdf`, 211 pages. No source, test, artifact, state file, log or original review was modified by this recheck.

## Both original MINORs are accepted as fixed

### MINOR 1 (gate robustness) — FIXED, with one residual coverage gap

The original finding required four things; the concrete fix asked for two assertions plus narrowed exemptions. Current state:

- **Header/row-count assertion added.** `tools/test_pdf_layout.py:126-144` (`appendix_b_structure`) asserts exactly one `扩展名` header on each page carrying B.2 rows, and flags a header with no rows. The gate reports `appendix B.2 table structure` on the old PDF (p186/p187 "header has no rows").
- **Empty card-strip assertion added.** `tools/test_pdf_layout.py:146-179` (`appendix_b_card_gaps`) measures the vertical gap from the last row's text to the card's drawn bottom rule, with `B2_CARD_MAX_GAP = 20.0` (`tools/test_pdf_layout.py:49`). Threshold is empirically justified: current p186 gap is **9.6 pt**, round6's is **39.9 pt**, reported as `appendix B.2 empty card strips: [(186, 39.9)]` on the baseline.
- **Exemptions narrowed.** `tools/test_pdf_layout.py:71-81` now exempts a page by *image area* (`> 0.2 · page area`) rather than any image, and only when `body_text()` starts with `引用链接` (citation block) or `图 ` (figure caption), instead of blanket substring matches.
- **Optional old-PDF path argument.** `tools/test_pdf_layout.py:183`: `target = Path(sys.argv[1]) if len(sys.argv) > 1 else PDF`.

Commands and observed exit codes:

```
python tools/test_pdf_layout.py yuyu-book/dist/kicad-book-zh.pdf          -> "PDF layout: OK", rc=0
python tools/test_pdf_layout.py yuyu-book/dist/kicad-book-zh-round6.pdf   -> "PDF LAYOUT CHECK FAILED", rc=1
```

The baseline fails with all relevant classes: underfilled `[68, 192]`; split tokens on p186; all 14 B.2 filenames "not on one line"; "header has no rows" on p186/p187; empty card strip `(186, 39.9)`. That is a genuine regression test — it fails on the old behavior and passes on the new, and no assertion was weakened.

Residual gap: the original finding also mentioned (c) chapter-end crowding from the global `.ch-close p` / `.ch-rut` change, and noted that `b2_pages()` stops at the first B.3 heading. Neither got a dedicated assertion. This is not a defect in the current artifact (geometry was checked independently), so I still call MINOR 1 FIXED as scoped by its own concrete fix, but the gate would not catch a future regression of those two cases.

### MINOR 2 (prose/precision) — FIXED

All three requested restorations are present in source and in the PDF text layer:

- `附录/B-文件格式与工程结构.md:39`: `未决问题：` and `每种文件的` restored verbatim (caveat relocated to p185, before the B.2 table).
- `附录/B-文件格式与工程结构.md:49`: `.pretty/` format is `目录（含 `.kicad_mod` 文件）` — parentheses and `文件` restored; no lone `）` line in the 140 dpi render of p185.
- `附录/B-文件格式与工程结构.md:56`: `.kicad_dru` content is `针对某个 `.kicad_pcb` 的<span class="nw">自定义</span>设计规则` — `针对` restored and `自定义` kept intact on one line (`rev2-186.png`, p186).

B.2 structure remains 1 header + 8 rows on p185 and 1 header + 6 rows on p186 = 14 unique filenames, each once. No token split, no clipping, no empty band. The text-extraction layer breaks `每种文件的` as `每种文`/`件的` only because of CJK line wrapping; the glyphs and source text are intact. No content was deleted to achieve the fixes.

## NEW MAJOR — global loss of `<wbr>` in inline code creates justified "rivers" book-wide

**Expected:** long code/URL tokens get soft break opportunities, so a line containing one wraps at a token boundary and the preceding CJK text keeps its normal ~10 pt character advance. **Actual:** inline `<code>` tokens are now unbreakable, so they are pushed whole to the next line and the preceding short CJK line is justified to the full column, producing visible rivers.

**First divergent boundary.** The round's diff adds `"code"` to `_NAME_BREAK_SKIP` at `yuyu-book/yuyu_book/render.py:117` (HEAD version omits it). `soften_long_names` calls `iter_doc(doc, _NAME_BREAK_SKIP)` at `render.py:161`, so from that call onward no `<wbr>` is inserted inside any of the ~250 inline `<code>` tokens in the book. This is a *different* mechanism from the reviewed `table td .nw` / `table td .nw` selector: the affected lines are ordinary paragraphs/bullets, not tables. The `style_print.py:56` change from `table td code.nw` to `table td .nw` only broadens nowrap inside table cells and is harmless here (the sole non-code `.nw` span is `自定义`; B.2 text ends at x1=533.0 inside a cell ending at x1=547.5 — no overflow).

**Minimal reproduction.** Rendering the same source fragment (`wrap_tables`→`soften_long_names`) with the HEAD skip-set inserts `<wbr>` after `/` in code tokens; with the current skip-set it inserts none. A/B on the two PDFs at identical content:

- round6 p191, y=603.0: `三份核心文件同时创建、备份目录：https://docs.kicad.org/10.0/en/getting_started_in_kicad/` is **one line** (x0=64.3 → x1=547.5), with the URL continuing normally on y=622.3. No stretch.
- current p191, y=141.0: the URL is unbreakable and moves to the next line; the bare lead-in is justified to **16 CJK characters with 21.3 pt gaps** between each (x0=64.3 → 547.5).

**Measured occurrences in the current artifact** (gap = next token x0 − previous token x1, in pt):

| page | y | symptom | worst gap |
|---|---|---|---|
| 142 | 186.0 | 25 CJK chars at ~9.5 pt spacing (≈ one extra character width each) | 9.5 |
| 148 | 64.3 | `路径变量：${KIPRJMOD}…` line at ~9.6 pt spacing | 16.0 |
| 149 | 341.0 | 17 tokens, mixed Latin/CJK, stretched | 22.9 |
| 149 | 540.6 | `/PCB画面符号与封装通常仍.kicad_sch内嵌lib_symbols缓` | **96.6** |
| 156 | 332.0 | `…Python环境和模块；` | **43.5** |
| 156 | 561.5 | `…Windows/macOS在Documents/KiCad/10.0/scripting/plugins，Linux在` | 27.1 |
| 191 | 141.0 | `三份核心文件同时创建、备份目录：` fully tracked out | 21.3 |

Visual confirmation: the author's own post-build render `.tmp/r7/final3-191.png` (13:46, after the 13:42 rebuild) shows the tracked-out line and the unbroken URL. Earlier renders `.tmp/r7/p191.png` (12:33) and `.tmp/r7/new-191.png` (13:01) show the same defect; `new-191.png` and `final3-191.png` are byte-identical (MD5 `7f39fea685e636d29fa12cc6e004ed07`). A separate 140 dpi render of current p148 also shows the stretched `路径变量：` line. A first vision read of p156 reported normal spacing; that was a false negative (it inspected the wrong paragraph) and is superseded by the word geometry above.

**Why MAJOR, not MINOR.** This is a new, book-wide print-typography defect in the exact domain this round set out to fix, visible without magnification on at least seven lines across five pages, and it is invisible to every green gate. It is caused by one speculative global change made while fixing two localized MINORs. Score is therefore reduced from 9 to 6 and acceptance is blocked.

**Required rework (do not weaken any gate).** Remove `"code"` from `_NAME_BREAK_SKIP` so soft break opportunities return, and if the B.2 cells still need unbreakable names, protect only those cells with a targeted mechanism (the existing `wrap_tables()` already adds `class="nw"` to space-free `<code>` tokens inside tables, which is the correct scope). After the change, rebuild and require: `test_pdf_layout.py` still rc=0 on the new PDF and rc=1 on round6, the 14 B.2 tokens still each on one line, and no line in the rebuilt PDF with a >15 pt inter-token gap outside legitimate table columns. Add such a river assertion to `test_pdf_layout.py` so this regression is caught rather than relying on visual review.

## Verified clean (unchanged by the fixes)

- **Artifact integrity:** 210 pages (baseline 211), 14,855,636 B, MD5 `7c185ac33d9400fc07865b9f391fa43b`; `kicad-book-zh.pdf` and `kicad-book-zh-round7.pdf` are the same file; 25 bookmarks with titles unchanged and page numbers shifted −1 from old p69 onward; zero blank pages.
- **No content loss / intentional short pages preserved:** only `附录/B-文件格式与工程结构.md` changed among book sources. The Ch6 bridge sentence occurs once on p67 at y=721.5 after the last acceptance bullet (y≈693.5–705.5), with the closing mark retained below; no orphan.
- **Full gate set:** `test_claims`, `test_usb_diagnostics`, `test_readme_links`, `test_book_metadata`, `test_pdf_cleanup`, `test_si_numbers` (17 mutations), `check_book` (`CONTENT CHECK OK`), `builder --check` (`CHECK OK`), and `test_pdf_layout` all rc=0; layout gate on round6 rc=1.
- **CI/docs wiring:** `.github/workflows/ci.yml` builds HTML+PDF before the check step, which runs `check_book` → `test_pdf_layout` → `builder --check`; `STRUCTURE.md` and `README.md` consistently state 210 pages / 25 bookmarks / 17 SI cases.
- **Doc staleness (non-blocking):** `docs/book-improvement/PAPER_IMPROVEMENT_LOG.md:28` still records the superseded hash `a75f748b…` / `14,855,572 B` instead of the actual `7c185ac3…` / `14,855,636 B`. `state.json` round7 remains `in_progress`, which is expected before a recheck verdict.

## Rejected hypotheses

- **"The p191 river is caused by `table td .nw`."** Rejected: the affected text is a bullet paragraph, not a table cell; a minimal render of the same fragment with/without `"code"` in `_NAME_BREAK_SKIP` changes `<wbr>` presence, and the `table td .nw` selector does not apply to `<p>`.
- **"The stretch was pre-existing and unrelated to this patch."** Rejected by A/B at identical content: round6 keeps the CJK lead-in and URL on one line, current does not; HEAD omits `"code"` from the skip set.
- **"The layout gate passing proves typography is clean."** Rejected: the gate has no river/justification assertion; all gates are green while p149 contains a 96.6 pt hole.
- **"p156 is fine because a visual read said so."** Rejected: word geometry shows 27.1 pt and 43.5 pt holes; the earlier vision answer inspected a different paragraph.
- **"The MINOR 2 fix split `自定义`."** Rejected: the `<span class="nw">自定义</span>` keeps it on one line in `rev2-186.png`; only the PDF *text layer* wraps adjacent CJK.
- **"`break-before:page` or `border-collapse:separate` would fix the empty B.2 band."** Rejected earlier by the author and confirmed unnecessary now: current p186 gap is 9.6 pt and the gate passes.

## Verification gaps

- The exact intermediate artifact judged by the original review (MD5 `a75f748b…`) was overwritten, so I cannot prove from bytes whether the river was already present in *that* build. What is proven: it is absent in round6, present in renders from 12:33 onward, and present byte-identically in the author's 13:01 and 13:46 final renders. The original review did not classify it. Relative to the round6 baseline and the pre-round renderer, it is patch-introduced.
- Visual confirmation was obtained for p191 (three independent renders) and p148; p142, p149 and p156 rest on vector/text geometry, not a fresh visual read of each page.
- No independent visual re-read of all 210 pages was performed; colour and plate cropping remain as in the original review's stated gap.
- `task_verify` cannot establish a project/git baseline for this repo, so only the explicitly executed commands above are evidence.

## Bottom line

Both original MINORs are **FIXED and accepted**; no fix needs to be reworked on its own terms. However, the round as a whole is **BLOCKED**: reverting the global `"code"` skip (and adding a river assertion) is required before this work can be accepted.
