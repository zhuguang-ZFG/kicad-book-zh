# Round 4 修复复核（fresh-context recheck）

复核对象：分支 `zhuguang-ZFG/round-4-improvements`，HEAD `f740f0c`；修复提交 `fc20cbd`。
复核方式：只读复核当前工作树与已构建产物，未信任上一轮结论；工作树在复核前后均为 clean。

## 结论

- **MAJOR 已关闭**：`STRUCTURE.md` 的 HTML 体积上限（8MB）高于 README 声明（约 5.6MB），且实测产物 5,599,650 B（5.59965 MB 十进制）与声明差 0.00035MB（远小于闸门 0.15MB 容差），并低于上限。
- 原 MINOR 2（README 字数陈旧）与原 MINOR 3（源稿图号重复/乱序）均已修复并有回归保护。
- 保留 1 个新发现的低优先级 MINOR（闸门在产物缺失时的静默放行），以及原第三个 MINOR（技术引用深度）作为已知延期项；未发现其中存在具体事实错误。
- 三个窄检查全部通过；未重建 HTML/PDF（无需重建）。

```json
{"score": 9, "verdict": "Accept", "merge": "ALLOW", "major_count": 0, "minor_count": 2, "confidence": 0.9}
```

## 1. MAJOR 关闭证据（HTML 体积契约）

| 项 | 值 | 证据 |
| --- | --- | --- |
| STRUCTURE 上限 | `< 8MB（当前约 5.6MB）` | `STRUCTURE.md:95` |
| README 声明 | `约 5.6MB` | `README.md:76` |
| 实测产物 | `5,599,650` B = `5.59965` MB（十进制，5.34 MiB） | `wc -c yuyu-book/dist/kicad-book-zh.html` |
| 声明↔产物偏差 | `abs(5.59965 - 5.6) = 0.00035` MB < 0.15MB 容差 | `tools/check_book.py:672-676` |
| 上限↔声明 | `8 > 5.6` | `tools/check_book.py:665-669` |

闸门实现：`tools/check_book.py:653-676` `check_artifact_claims()`，由 `main()`（`:735`）调用；回归在 `tools/test_book_metadata.py:134-141` `test_structure_html_limit_covers_readme_claim()`，断言 `float(claim) < float(limit)`。上一轮的 `< 1MB` 表述已在当前 `STRUCTURE.md` 中全部消失（`grep -n 'HTML 构建大小' STRUCTURE.md` 只返回第 95 行的 8MB）。

### 闸门能否静默放行（题目要求判定）

用 `unittest.mock.patch` 做纯内存实验，不改动任何文件：

1. **产物缺失**：把 `check_book.BOOK` 指向空临时目录后调用 `check_artifact_claims()`，返回 `errors: []`。原因：所有体积检查都包在 `if html.exists():`（`tools/check_book.py:670-671`）内部，而本函数只有 PDF 存在性检查（`:660-662`），**没有 HTML 存在性检查**。因此删除 HTML 后 `python tools/check_book.py` 仍会打印 `CONTENT CHECK OK`。
2. **上限缺失**：把 `STRUCTURE.md` 的读取打桩为空串后调用同一函数，返回 `errors: []`（README 的 5.6 声明仍能解析，但与产物的偏差检查通过，且 `limit` 为 `None` 使两处上限比较被跳过）。因此 `check_book.py` 单体会静默放行。
3. **但回归测试能挡住第 2 种情况**：对 `test_structure_html_limit_covers_readme_claim()` 做同样打桩后，测试按预期失败：`AssertionError: README/STRUCTURE must state the HTML size and limit`。`STRUCTURE.md:39-47` 把该测试列为提交前必跑项，因此上限缺失不会进入合并。

判定：`check_book.py` 单体对两种缺失都会静默放行；测试套件覆盖“上限缺失”，**不覆盖“产物缺失”**。这是新增闸门的硬化缺口（低优先级），不是本轮修复引入的回归，也不阻塞合并。

## 2. 窄检查（按要求运行，全部通过）

```
$ python tools/test_book_metadata.py
metadata-regression-zh.html: 0.1 MB, 0 units, 0 plates, 0 cited links, ...
book metadata regression: OK          EXIT=0

$ python tools/test_readme_links.py
README link regression: OK            EXIT=0

$ python tools/check_book.py
illustrations referenced: 37; files: 62
photographs referenced: 10; files: 10
CONTENT CHECK OK                      EXIT=0
```

运行后 `git status --short` 为空（测试产物未污染工作树）。

## 3. 产物元数据

- `yuyu-book/manifest.json`：`"version": "0.1.4"`、`"date": "2026-11-26"`（较上轮 0.1.3 / 2026-11-25 正确提升）。
- PDF（PyMuPDF 1.28.0）：`doc.page_count = 204`，`get_toc() = 25` 书签，`blank pages = []`；metadata `title=KiCad 从原理到制板`、`author=KKiCad 教学组`、`keywords=v0.1.4 2026-11-26`、`creator=producer=yuyu-book`。
- PDF 首页 imprint 文本含 `v0.1.4 · 2026-11-26 · CC BY-NC-SA 4.0`；全文含 `KiCad 从原理到制板`、`KKiCad`、`技术试读版`。
- HTML 含 `v0.1.4` 与 `2026-11-26`，与 manifest 一致。
- README：`README.md:72` 写 204 页 / 25 书签 / 0 空白页，`:77` 写 PDF 204 页 / 25 书签 —— 与实测一致（上一轮的 205 页由本轮新构建 PDF 更新为 204）。

## 4. 图号（源稿与成书）

- `source_figure_number_problems()`（在 `tools/check_book.py:65-96`）对 `book_sources()` 的结果返回 `[]`。逐行核对：
  - ch4：`图 4-1/4-2/4-3/4-4`（`04-从符号到封装.md:63,80,84,124`）
  - ch6：`图 6-1..6-4`（`06-布局.md:35,86,109,159`）
  - ch10：`图 10-1..10-3`（`10-输出制造文件.md:38,78,235`）
  - ch12：`图 12-1..12-6`（`12-焊接调试与返修.md:40,82,99,103,242,284`）
  - 均为每章 1..N 连续、无重复；`*` 前缀的照片图题也被正则覆盖。
- 成书 HTML：解析 `<figcaption>` 得 67 个图题，`图 N-M` 编号 67 个全部唯一、零重复。其中**数字章前缀恰好 48 个**（0-1；1-1..1-2；2-1..2-5；3-1..3-2；4-1..4-4；5-1..5-3；6-1..6-4；7-1..7-3；8-1..8-3；9-1..9-3；10-1..10-3；11-1..11-3；12-1..12-6；13-1..13-2；14-1..14-2；15-1..15-2），与上一轮报告的 48 完全一致；另有 19 个附录图题 `A-1..A-19`，上一轮按数字前缀扫描未计入。
- 成书 PDF：逐页抽取得到 67 个独立成行的 `图 N-M` 编号，67 个唯一、零重复；数字前缀 48 个、字母前缀 `A-1..A-19` 19 个，与 HTML 一致。
- “重复”需区分：PDF 文本层另有 8 处同一编号同时出现为独立编号行与“编号+图题正文”行（如 `图 4-4` 与 `图 4-4 符号字段导出为 BOM...`），这是 PyMuPDF 换行抽取导致的同一图题被读两次，**不是重复图题**；HTML DOM 中每个编号仅出现一次，可证伪。正文中的散文式引用（如“见图 4-3”）不带 `<span class="fig-no">`，不计入图题。

## 5. 字数闸门与排除项

- `book_sources()`（`tools/check_book.py:36-42`）按 manifest 顺序给出 20 个文件：前言 1 + 第 1–15 章 15 + 附录 4。
- 独立复算：`chars = 154,676`（15.468 万）、`han = 61,094`（6.109 万）；README `:9` 与 `:56` 两处均声明 15.5 万 / 6.1 万，偏差分别为 0.21% 与 0.15%，远小于 `check_readme_stats()`（`:635-648`）的 5% 容差。
- 排除生效：`md_files()` 共 23 个文件，其中 `docs/README.md`、`README.md`、`STRUCTURE.md` 不在 `book_sources()` 中；`.tmp/`（5 个 md）和 `docs/book-improvement/`（5 个 md）被 `md_files()` 的 `".tmp" in p.parts` / `"book-improvement" in p.parts`（`:27-31`）排除，且 manifest 路径从不指向它们。新闸门与旧实现在本仓库统计结果一致（旧实现按文件名跳过 README.md/STRUCTURE.md，同样跳过 docs/README.md），无统计回归。

## 6. 残余风险与 MINOR

1. **MINOR 1（新，低优先级）**：`check_artifact_claims()` 在 HTML 产物缺失或 STRUCTURE 上限缺失时于 `check_book.py` 单体中静默放行（证据见第 1 节）。建议后续给 HTML 增加与 PDF 对称的存在性检查，并把 `claim`/`limit` 缺失改为显式 error（目前仅由测试兜住上限缺失）。不影响当前契约正确性。
2. **MINOR 2（延期，已知）**：原第三个 MINOR（技术引用深度：上游 LICENSE、Tektronix/Microchip/ngspice/KiCad 文档正文未联网核对）本次仍为文档级引用；未发现具体事实错误，按约定作为 deferral 保留。
3. 未做视觉栅格化检查（版式、字体回退、断行、SVG 对比度、暗色模式）；结论只覆盖文本层与结构层。
4. 本机未重跑完整构建；产物为提交时已构建的 `Nov 26 09:37` 版本，其元数据/页数/体积已逐项实测并与文档一致，未发现需要重建的矛盾。

## 7. 未能验证 / 验证缺口

- 未联网抓取上游 LICENSE 与技术文档正文（环境/范围限制），相关断言仅文档级。
- 未在 KiBot 容器内执行 `.kibot.yaml`（无 Docker），沿用书稿中已声明的验证边界。
- 未对渲染结果做人工视觉检查。
