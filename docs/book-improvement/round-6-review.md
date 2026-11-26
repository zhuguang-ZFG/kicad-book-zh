# Round 6 独立复核（只读审计）

- 对象：`yuyu-book/dist/kicad-book-zh.pdf`（211 页，25 书签，14,883,630 B），分支 `zhuguang-ZFG/round-6-audit` @ `92d389f`（= `origin/main`，工作区干净）。
- 方法：PyMuPDF/源 Markdown 逐项取证；19 张附录 A.7 截图逐张以视觉问答对照标题/页签/面板/值；CLI 参数对照 `tools/_cli10.txt`，快捷键与菜单对照 `tools/_eeschema10.txt`、`tools/_pcbnew10.txt`。未运行构建（按约束）。

## Score: 9/10
## Verdict: Accept
## Merge: ALLOW
## Counts: MAJOR 0 / MINOR 1（另见“非缺陷不确定性”）

## 已逐项核验且无缺陷的领域

1. **定量与可复现性。** 独立重算全部关键数字，与书中一致：`07-布线.md:38-83` IPC-2221 线宽（外 0.5/1/2/3 A → 0.12/0.30/0.78/1.4 mm，内 → 0.30/0.78/2.0/3.6 mm）；30 mm/0.30 mm/1 oz ≈ 49 mΩ（1 A ≈ 40 mV），0.5 mm ≈ 30 mΩ；2 A ≈ 48 °C、3 A ≈ 121 °C 的 ΔT 外推并明确标为“数量级警告”；§7.3 `BW=0.35/RT` 表（20 ns→18 MHz/600 mm；2 ns→175 MHz/60 mm；0.5 ns→700 MHz/15 mm；0.1 ns→3.5 GHz/3 mm）；§7.5 微带 0.25/0.5/1.0 mm → 138/112/86 Ω；`05-板框与叠层.md:91` 1.6 mm 两层板 50 Ω≈3 mm、四层 0.2 mm 介质→0.3 mm 线宽；`06-布局.md` θJA 167/159 °C/W；第 2 章 P_LDO≈32.7 mW、待机 9–10 mA；`13-仿真与电路验证.md:101-112` 3.3 V/2.0 V/330 Ω → 3.9 mA、1 kΩ → 1.3 mA。传播时延 170 ps/inch≈6.7 ps/mm 亦自洽。
2. **KiCad 10.0.8 操作正确性。** `tools/_cli10.txt` 中书里使用的全部参数均存在：`--subtract-soldermask`、`--use-drill-file-origin`、`--no-protel-ext`、`--no-x2`、`--generate-map`/`--map-format`、`--excellon-separate-th`、`--bottom-negate-x`、`--exclude-dnp`、`--subst-models`、`--no-dnp`、`--schematic-parity`、`--exit-code-violations`、`--severity-all`/`--severity-exclusions`、`--refill-zones`、`--save-board`、`--group-by`、`--precision`、`--drill-origin`、`--excellon-units`；`jobset run` 子命令存在。语义核对：`--exit-code-violations` 无违规 0/有违规 5（书 §9 一致）；`--refill-zones` 不自动保存，`--save-board` 需配合 `--refill-zones`（一致）。菜单路径与热键与官方手册逐条吻合：Ctrl+F1=List Hotkeys、`_eeschema10.txt:17057` F1=Zoom In at Cursor、`_eeschema10.txt:4629-4633` Ctrl+G=Search panel、`_eeschema10.txt:17120` Ctrl+F=Find、`_eeschema10.txt:16484` S=Draw Hierarchical Sheets、`_pcbnew10.txt:9894/9936` PgDn/PgUp=B.Cu/F.Cu 且 +/- 为 Next/Previous Layer、`_pcbnew10.txt:10517` B=Fill All Zones、`_pcbnew10.txt:10165/10180/10212` Ctrl+Shift+C/L/T、`_pcbnew10.txt:10271-10273` R/Shift+R=逆/顺时针。A.6 菜单路径（File→Board Setup、Tools→Update PCB from Schematic(F8)、File→Fabrication Outputs→Gerbers/Drill Files/Component Placement、Tools→Generate BOM 等）均与手册目录一致。
3. **验收可观测性。** 15 章“验收”均为读者自有工程中可观察项（连通性、DRC、文件清单、Gerber 对齐、测量记录、仿真复现、CI 产物），无依赖“本书附带的工程文件”的条款；与 `README.md:9,79`、`STRUCTURE.md:8-9` 的“不随书附带成品 KiCad 工程文件、读者自建 `usb_breath_led/`”契约不冲突。第 12 章呼吸功能验收与 §12.3 `breath.c` 的 1.23 s 名义周期对应，并明确“不要求精确秒数”。
4. **附录 A.7 全 19 张截图逐张像素核对（本轮重点）。** A-1 ERC（左按类型分组、底部 Show/Run ERC/Delete）✓；A-2 Schematic Setup→Violation Severity（Error/Warning/Ignore）✓；A-3 Board Setup→Physical Stackup（6 层、0.035/0.0152 mm、板厚 1.5296 mm）✓；A-4 Constraints（最小线宽/间距/孔等）✓；A-5 Copper Zone Properties（GND、0.12 mm、Thermal reliefs、Remove islands=Always）✓；A-6 Track & Via Properties（Net /SCL、0.25 mm、0.8/0.4 via、F.Cu/B.Cu）✓；A-7 Design Rules Checker→Violations（Exclusions 勾选、Save…、Run DRC）✓；A-8 Board Setup→Violation Severity（Error/Warning/Ignore 单选）✓；A-9 Choose Symbol（左侧树+右侧符号与封装双预览+OK）✓；A-10 Symbol Properties→Footprint 字段（`footprints:TDFN-8_…`）✓；A-11 Schematic Setup→Net Classes（含 Wire Thickness 列与下方 Netclass Assignments）✓；A-12 Board Setup→Net Classes（Track Width/Via/DP Width/DP Gap）✓；A-13 Update PCB from Schematic（Changes to Be Applied + Update PCB）✓；A-14 Plot（Gerber、Output directory、Include Layers）✓；A-15 3D Viewer（已贴装板、连接器可见）✓；A-16/17 Schematic/PCB Editor 总览（数字标注为官方标注）✓；A-18 Footprint Chooser（引脚数筛选+右侧焊盘与 3D 预览）✓；A-19 Interactive Router Settings（Highlight/Shove/Walk around、Free angle mode、Shove vias）✓。**无标题、页签、左右布局、设置项或数值与图注矛盾。**
5. **来源与许可边界。** `yuyu-book/sources.json`（schema 1）记录 kicad-docs 快照 10.0.8 / rev 8acc7624、访问日 2026-11-26、GPL-3.0-or-later / CC BY 3.0；`yuyu-book/screenshots/README.md` 逐张映射 27 条来源，19 条对应附录 A.7；A.7 图注明确 CC BY 3.0 / GPLv3+，未见把 MIT（KiBot）与 AGPL-3.0 混用的误述。

## Findings

### F1 (MINOR, confidence 0.65) — 第 7 章“普通走线 86–138 Ω”与第 5 章默认网类 0.20 mm 不自洽
- **位置：** `第二部分-设计篇/07-布线.md:171,175,271` 对照 `第二部分-设计篇/05-板框与叠层.md:123`。
- **证据：** Ch7 表格只列 0.25/0.5/1.0 mm → 138/112/86 Ω，随后两处断言“本板这些普通走线实际在 86–138 Ω”；而 Ch5 的 `Default` 网类（普通 GPIO、LED）线宽为 **0.20 mm**，比表首 0.25 mm 更窄，按同一微带近似外推约 145 Ω，落在所述区间之外。
- **为何重要：** 这是跨章的定量结论与本章唯一网类默认值冲突；读者用书中默认值布线后，按书中同一公式算出的阻抗不在书中给出的区间内，削弱“数字可复现”的承诺。不影响本板电气正确性（边沿慢、不做阻抗控制）。
- **最小修复：** 在 §7.3 表格增加 0.20 mm 行（≈145 Ω），或把两处“实际在 86–138 Ω”改为“按 0.25–1.0 mm 估算为 86–138 Ω；默认 0.20 mm 更窄、阻抗更高，本板均不作阻抗控制”。

## 非缺陷不确定性（不计入 MAJOR/MINOR，建议记录但不阻断）
- A-19 图注的“走线角度”在截图中仅体现为灰显的 `Free angle mode`；KiCad 10 的 45°/90° 全局角度选项在 Preferences→PCB Editor，不在该对话框。因复选框确属角度相关设置，未判为图文不符，但图注措辞略宽。
- A-11 图注的“成员”由表格下方 Netclass Assignments 区呈现，而非表格独立列；截图包含该区，判为一致。
- Round 5 曾标注 §7.4 蛇形图注与 §13.4 模拟器左右布局两处图文矛盾；本轮未把它们作为新发现重复报告，也未重新裁定其是否已修复——如需确认请在 Round 7 单独取证。
- 本轮未做 211 页栅格级逐页目检；除上述 19 张 A.7 截图与 Round 5 已核的 8 张正文截图外，不宣称全页视觉验收通过。

## 独立合并结论
Rounds 1–5 的阻断项（LED 网络、CLI 原点、阻抗措辞、重复图号、HTML 体积声明、KiBot 目录、截图图注）在本轮取证中均未见回归；五个优先级逐项过检后仅余一处可复现性措辞 MINOR（F1），不影响读者完成任一章验收或制造交付。**Score 9/10；Verdict Accept；Merge ALLOW**——建议合并，F1 作为下一轮编辑项处理即可。
