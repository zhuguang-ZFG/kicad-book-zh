# Round 6 修正复核（只读 recheck）

复核对象：分支 `zhuguang-ZFG/round-6-audit` @ `92d389f`（base `origin/main`）上针对 `round-6-review.md`（9/10、Accept、ALLOW、0 MAJOR / 1 MINOR）的修复。产物 `yuyu-book/dist/kicad-book-zh.pdf`（与 `kicad-book-zh-round6.pdf` MD5 同为 `1d75b07c951fcdc08e5914595fc6c7bd`）。只复核指定五项；未运行完整构建，仅运行 `python tools/check_book.py` 与 `python tools/test_si_numbers.py`。

## Overall

- **Score: 9/10**（与 Round 5 recheck 同档：无缺陷级问题、可合并；未按 211 页栅格级视觉验收，故不满分）
- **Verdict: Accept**
- **Merge: ALLOW**
- **Counts: MAJOR 0 / MINOR 0**（Round 6 的唯一 MINOR 已关闭；无新增缺陷）
- **Confidence: 0.92**

## 逐项结论

| 项 | 状态 | 证据 |
| --- | --- | --- |
| F1：0.20 mm 默认网类阻抗与 86–138 Ω 冲突 | **FIXED** | `第二部分-设计篇/07-布线.md:175`、`:271`；`tools/check_book.py:537-550`；`tools/test_si_numbers.py:38`；PDF 第 74、78 页文本层 |
| A-19 图注过宽的“走线角度” | **FIXED** | `附录/A-快捷键与界面速查.md:228`；截图 `yuyu-book/screenshots/pcbnew-router-settings.png`；`tools/_pcbnew10.txt:1885-1887` |

### 1. F1 复查：独立重算 + 双位置文本

按 `tools/check_book.py:582-591` 的 Hammerstad–Jensen 闭式（含 `u<=1` 分支，`er=4.3`，`h=1.5 mm`）独立重算，与书中数字逐项吻合：

| 线宽 | u=w/h | 重算 Z0 | 书中值 |
| --- | --- | --- | --- |
| 0.20 mm | 0.1333 | **146.23 Ω → 146** | 约 146 Ω ✓ |
| 0.25 mm | 0.1667 | 137.78 → 138 | 约 138 Ω ✓ |
| 0.5 mm | 0.3333 | 111.69 → 112 | 约 112 Ω ✓ |
| 1.0 mm | 0.6667 | 86.15 → 86 | 约 86 Ω ✓ |

- §7.3 正文（`07-布线.md:171-175`）保留 0.25/0.5/1.0 mm 表（138/112/86 Ω），新句把 0.25–1.0 mm 区间与 0.20 mm 默认值分开：“0.25–1.0 mm 线宽对应 86–138 Ω；而 §5.4 的 `Default` 网类默认 0.20 mm，按同一近似式约 146 Ω。本板的普通走线按网类取 0.20 mm，因此实际更接近 146 Ω……”。
- 章小结（`07-布线.md:271`）同步：“本板普通走线按 §5.4 取 0.20 mm，微带近似约 146 Ω；0.25–1.0 mm 对应 86–138 Ω，都不是 50 Ω……”。
- 全书 Markdown 扫描（排除 `docs/book-improvement/` 的历史记录）已无“本板这些普通走线实际在 86–138 Ω”一类over-broad 断言；`PAPER_IMPROVEMENT_LOG.md` 中的旧表述是对修复过程的历史描述，不是正文主张。
- 对照 `第二部分-设计篇/05-板框与叠层.md:123`：`Default`（普通 GPIO、LED）确为 **0.20 mm**。
- PDF 文本层：第 74 页含 §7.3 新句，第 78 页含章小结新句，均含“146 Ω / 0.20 mm / 86–138 Ω”。

### 2. Gate 回归：新检查确实会变红，且树恢复后为绿

- `tools/check_book.py:537-550` 新增 0.20 mm/1.5 mm 分支：`re.search(r"0\.20\s*mm[^。]{0,60}?约\s*([0-9]+)\s*Ω", ch07)`，与 `microstrip_z0(0.20, 1.5)=146.23` 比较，容差 `max(3.0, want*0.05)`。
- `tools/test_si_numbers.py:38-39` 新增变异 `0.20 mm default impedance 146 -> 50 ohm`（把 §7.3 的“约 146 Ω”改成“约 50 Ω”）。
- 实测：`python tools/check_book.py` → `CONTENT CHECK OK`（exit 0）；`python tools/test_si_numbers.py` → `SI number regression: OK (17 mutations detected)`（exit 0，比修复前多 1 条）。该脚本对每条变异都会在子进程中运行 gate 并要求非零退出且出现 `ch07:`/`ch08:` 错误，最后校验恢复后的树为绿——因此 146→50 变异被检出即为“改错值会失败”的证据。
- 变异脚本用 `try/finally` 恢复源文件；测试后 `git diff --numstat` 显示 `07-布线.md` 仍为 2/2、`08-铺铜与电磁兼容.md` 未被修改，无行尾重写或残留污染。

### 3. A-19 图注 vs 截图

- `附录/A-快捷键与界面速查.md:228` 现为：“Mode 里选 Highlight collisions、Shove 或 Walk around，右侧控制过孔推挤、冗余走线清理等选项；自由角度模式只在 Highlight collisions 下可用，图中因选中 Shove 而灰显。”已改为 Mode 选项 + 灰显状态，不再有“走线角度”的over-broad 表述（两文件全文检索 `走线角度` 为 0 命中）。
- 视觉读取 `pcbnew-router-settings.png`：Mode 单选确为 Highlight collisions / Shove / Walk around，**Shove 被选中**，Free angle mode **灰显且未勾选**；右侧可见 Shove vias ✓、Remove redundant tracks ✓ 等，与图注一致。
- “只在 Highlight collisions 下可用”亦符合一手资料：`tools/_pcbnew10.txt:1885-1887` 写明 Shove/Walk Around 只能产生 H/V/45 段，非 H/V/45 角度“must use Highlight Collisions mode and enable the Free Angle Mode option in the Interactive Router Settings dialog”。
- A-7 截图组仍为 19 张（`附录/A-快捷键与界面速查.md` 中 `图 A-1`…`图 A-19` 共 19 个 fig-no），未改动任何截图文件。

### 4. 产物完整性

- PDF：211 页；书签（`get_toc()`）25 条；空白页 0；新 Ch7 句在文本层第 74、78 页（见上）。
- HTML：`yuyu-book/dist/kicad-book-zh.html` 共 **78 个 `fig-no` span、78 个唯一值、0 重复**（此前按“图 数字-数字”统计漏掉 19 个 `图 A-N`，口径已校正：59+19=78）。
- `kicad-book-zh.pdf` 与 `kicad-book-zh-round6.pdf` MD5 一致（同上），评审对象即当前交付件。

### 5. 无回归（Round 5 修复与 A.7 截图组）

- 图 7-4（`07-布线.md:197`）仍为“两根并行走线同时蛇形调谐，即差分对；单端才只调一根”，Round 5 的修正保留。
- 图 13-3（`第四部分-进阶篇/13-仿真与电路验证.md:187`）仍为“官方文档的 AC 扫描示例，不是本板 RC 结果”“波形、Signals 与 Cursor 同屏”，已无“左侧/右侧”方位陈述。
- 图 5-2（`05-板框与叠层.md:81`）仍写明“铜层数量在 Physical Stackup 左上角设置”，Round 5 合并后修正保留。
- `screenshots` 目录 27 张图片齐全，`check_book.py` 报 `screenshots referenced: 27; files: 27`；未重新做 19 张像素比对（按约束）。

## 非缺陷 / 未覆盖说明（不计入 MAJOR/MINOR）

1. **Gate 覆盖口径**：`check_book.py:543` 用 `re.search` 只校验 ch07 中第一处“0.20 mm … 约 N Ω”（即 §7.3 正文）。章小结第 271 行的同一 146 Ω 主张目前靠文本复核、未被独立断言。当前树两处均正确，故非缺陷；如需硬化，可把 `re.search` 改为 `re.findall` 并要求所有匹配值一致。
2. 未按 211 页栅格级逐页视觉目检；本复核的视觉证据仅限 A-19 截图与 Round 5 既有结论。
3. 复核期间 `docs/book-improvement/PAPER_IMPROVEMENT_LOG.md` 与 `state.json` 被另一进程修改（非本复核写入，不在五项验证范围内）；未对其做任何改动。

## 独立合并结论

Round 6 的唯一 MINOR（F1）与附带提出的 A-19 图注措辞均已按最小改动修复，数值经独立重算、gate 经变异测试证明会变红、恢复树为绿；产物页数/书签/空白页/图号计数与新增句子文本层全部符合。未发现新的 MAJOR 或 MINOR。**Score 9/10；Verdict Accept；Merge ALLOW。**
