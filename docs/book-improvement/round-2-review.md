# Round 2 Review —《KiCad 从原理到制板》

## Overall
- **Score: 6/10**（Almost/BLOCK 档：存在影响读者读图与操作的 MAJOR，合并前应修正）
- **Verdict: Almost**

Round 2 把上一轮阻断合并的五处 MAJOR 全部关闭：§2.1 网络表已把 LED 支路从 `+3V3` 移到 `LED` 行；§2.4–2.6 新增“先把器件选型锁定”表；§12.3 内联 `breath.c` 的软件 PWM 呼吸实现并给出周期验收；§7.3 标题收窄为“本板这些线宽不是 50 Ω”；§15.2 三条导出命令已统一原点参数。定量数字、CLI 参数与附录四篇整体自洽。但交付的 201 页 PDF 中存在**系统性图号重复**：第 42、58、98、116、119、124 页各出现两个编号相同的图，且正文用这些编号作跨图引用，读者无法判断“图 12-1”指烙铁照片还是上电顺序图。这是成品中可见的承诺破损，按口径列为 MAJOR，因此本轮不给出 Accept。

## Strengths（ranked）

1. **Round-1 的五处 MAJOR 全部落地，且不是字面修补。**  
   `第一部分-入门篇/02-原理图第一笔.md` §2.1、§2.4–2.6；`第三部分-制造篇/12-焊接调试与返修.md` §12.3；`第二部分-设计篇/07-布线.md` §7.3；`第四部分-进阶篇/15-自动化与插件.md` §15.2。§15.2 的 Gerber/钻孔/POS 已与 §10.2–10.4、§15.6 使用同一原点基准。

2. **高速数字（SI）段落的数字可独立复算，并区分估算与硬数据。**  
   `第二部分-设计篇/07-布线.md` §7.3：FR4 6.7 ps/mm、0.35/tr 带宽表、600/60/15/3 mm 长度门限、拐角电容与残桩估算、IPC-2221 宽度与温升、微带阻抗表（用 εeff 复算 138/112/86 Ω 均吻合）量级正确，且明确标为估算。

3. **命令行与工具链版本自洽，并设有诚实的验证边界声明。**  
   `第四部分-进阶篇/15-自动化与插件.md` §15.6：`kicad-cli version` 默认只输出版本号（官方 CLI 手册示例 `7.0.7`），`test "$version" = "10.0.8"` 守卫成立；`--refill-zones --save-board --exit-code-violations`、`if: always()` 归档、`on: [push, pull_request]` 与本章安全解释一致；章末明确声明容器示例未在镜像中实跑。

4. **附录四篇把速查与排错做成了可操作索引。**  
   `附录/A` 区分 macOS `Cmd`/`Option` 与 `Ctrl+F1`，注明原理图 `C` 是从总线展开；`附录/B` 说明 `.kicad_prl`、`fp-info-cache`、`-backups/` 不提交；`附录/C` 的 ERC/DRC/制造三段表含 `Track width` 为优选值、`Schematic parity` 仅在启用时检查；`附录/D` 含 fiducial 与 locating hole、absolute maximum rating 等辨析。

5. **来源登记的缺口已补齐。**  
   `yuyu-book/sources.json` 现含 `attiny25-45-85-datasheet` 与 `avrdude-8-1-manual`；`kicad-symbols`、`kicad-footprints`、`klc` 不再被统一归为“社区材料（非规范）”，与前言表述一致。

## Weaknesses（ranked CRITICAL > MAJOR > MINOR）

### 1. Severity: MAJOR
- **Location:** `yuyu-book/dist/kicad-book-zh-round2.pdf` 第 42、58、98、116、119、124 页；源稿 `第一部分-入门篇/04-从符号到封装.md` 第 84/124 行、`第二部分-设计篇/06-布局.md` 第 35/86 行、`第三部分-制造篇/10-输出制造文件.md` 第 78/235 行、`第三部分-制造篇/12-焊接调试与返修.md` 第 40/82/103/284 行。
- **Evidence:** PDF 文本层实测：page-42 出现两个“图 4-3”；page-58 两个“图 6-1”；page-98 两个“图 10-2”；page-116 两个“图 12-1”；page-119 两个“图 12-4”；page-124 两个“图 12-6”。同一编号分别指向照片与示意图/命令行图。正文还用这些编号作指代，例如 `10-输出制造文件.md` 第 235 行“图 10-2 同一条命令在终端、本地和 CI 里行为一致”，`12-焊接调试与返修.md` 第 82 行“图 12-1 首次上电的顺序”。此外图 12-4 出现在图 12-3 之前。
- **Why it matters:** 这不是源稿里的无害冗余，而是成品 PDF 中可见的编号碰撞。读者按正文“见图 12-1”去查找时会同时命中烙铁照片与上电顺序图；图号失去唯一性，图表引用与复习索引均不可靠。虽然 `yuyu-book/yuyu_book/render.py` 的 `renumber_figures`（第 305 行定义、第 510 行调用）旨在按文档顺序重排图号，但实测表明手写照片图注并未纳入该重排，机制未覆盖全部图源。
- **Smallest actionable fix:** 在渲染管线里把照片图注也接入 `renumber_figures`（让 `photo_figures`/`absorb_ill_captions` 输出的 caption 使用统一图号计数器），或从源稿照片图注中移除硬编码“图 X-Y”并统一由构建脚本注入；随后重建 PDF 并复核上述六页无重复编号。

### 2. Severity: MINOR
- **Location:** `yuyu-book/sources.json` 第 199–208 行与第 508–516 行；对照 `第四部分-进阶篇/15-自动化与插件.md` 第 184–186、249、261 行。
- **Evidence:** 同一工具两条登记：`"github-actions-upload-artifact"` 的 `title` 为 `actions/upload-artifact v4`，`scope: "第15章：上传 CI 报告和制造输出"`；`"github-actions-upload-artifact-v7"` 的 `title` 为 `actions/upload-artifact v7`，快照含 v7.0.0 `archive:false`、v6 起默认 Node 24 且要求 runner ≥ 2.327.1。正文实际使用 `@v7`。
- **Why it matters:** 来源页会并列出现两张互相矛盾的同一工具卡片，v4 快照不覆盖正文引用的 v7 行为。
- **Smallest actionable fix:** 删除 v4 条目或把它改标为“历史对照”，并让 `scope` 不再声称“第15章”；正文与来源页只保留 v7 一条登记。

### 3. Severity: MINOR
- **Location:** `第二部分-设计篇/07-布线.md` §7.4/§7.7、`第二部分-设计篇/08-铺铜与电磁兼容.md` §8.5–8.7、`第四部分-进阶篇/13-仿真与电路验证.md` §13.6。
- **Evidence:** “本板不需要阻抗控制/等长/仿真”“本项目没有天线”“本板无数据线”在阅读路径、正文、检查清单、验收与小结中多次整段复述；Round-1 已提出，本轮未见收窄。
- **Why it matters:** 跨章重复会让主线操作被提示框淹没，稀释真正需要保留的版本与安全警告。
- **Smallest actionable fix:** 前言设“基线范围表”，后续章节以“基线不适用，见 §7.3”替代整段重述；保留所有与安全、否定关系、测量边界相关的句子。

## Missing or wrong-context references

- **来源登记重复且标题冲突（对应 Weakness 2）：** `github-actions-upload-artifact`（v4）与 `github-actions-upload-artifact-v7` 并存，前者 `scope` 仍指向第 15 章，应合并为单一 v7 条目。
- **Round-1 指出的两处缺失已修复：** `sources.json` 已含 `attiny25-45-85-datasheet`（HTTPS URL、访问日期、引用范围）与 `avrdude-8-1-manual`，覆盖 §2.4 绝对最大额定值与 §12.3 的 `usbasp`/`t85`/signature 语法。
- **Round-1 的官方库/KLC 分类问题已修复：** `kicad-symbols`、`kicad-footprints`、`klc` 不再统一归入“社区材料（非规范）”。
- 其余登记 URL 均为 HTTPS，多数带 `snapshot`/`accessed`/`license`/`scope`/`normative`；本轮未联网核验实时可达性。
- PB3/PB4 的 OC1B 反相关系仍无专门数据手册 `scope` 条目，见 uncertainties。

## Visual review

- 抽样对象：`yuyu-book/dist/kicad-book-zh-round2.pdf`，独立读取确认 **201 页**（与任务书更正一致）。
- 图号（实测）：文本层抽取给出 page-41→4-1、page-42→4-2/4-3/4-3、page-44→4-4；page-58→6-1/6-1、page-60→6-2、page-61→6-3、page-63→6-4；page-96→10-1、page-98→10-2/10-2、page-103→10-3；page-116→12-1/12-1、page-117→12-2、page-118→12-3、page-119→12-4/12-4、page-123→12-5、page-124→12-6/12-6。重复编号确认为成品缺陷（Weakness 1）。
- 正文/导航：范围为 `00-前言.md` + 01–15 章 + 附录 A–D，无第 16 章；文件清单与任务书一致。
- 表格/公式/来源页：Round-1 抽样过的边沿时间表、走线长度图、阻抗表与 YAML 续页在 Round 2 未见退化证据；但本轮未做全 201 页栅格级视觉复核，不据此宣称全页验收通过。
- 来源页：v4/v7 重复登记会呈现为两张卡片（Weakness 2）；其余来源卡片结构统一。

## Remaining uncertainties

- 未执行构建与六项回归脚本；按任务书“测试仅作辅助”的口径不把任何测试结果当作通过依据。
- 未做全 201 页栅格级视觉复核；page-150 附近的 YAML 续行是否仍存在 Round-1 MINOR #7 未确认。
- `kicad-cli version` 默认输出经官方 CLI 手册（`tools/_cli10.txt` 第 2107 行）确认支持精确字符串比较；但 `kicad/kicad:10.0.8` 镜像是否实际返回无后缀的 `10.0.8`，未在真实容器实跑。
- `upload-artifact` v5“支持 Node 24 但默认 Node 20”未在 `sources.json` 的 v7 快照中逐字覆盖；v6 的 Node 24 / runner ≥ 2.327.1 前提有登记。
- PB3/PB4 与 OC1B 反相关系无独立数据手册快照。
- `sources.json` 快照 commit、发布说明与 GitHub Actions 版本信息未联网核验。

## Merge verdict: BLOCK

五处影响操作的 MAJOR 已关闭，但成品 PDF 中六页存在重复图号且正文用这些编号作跨图引用，属于读者可见的图表索引破损，按评分口径不得 Accept。修正渲染管线的图号注入后重建并复核，可望在下一轮进入 Accept。
