# Round 5 评审（独立复核）

评审对象：`yuyu-book/dist/kicad-book-zh-round5.pdf`（211 页）、`yuyu-book/dist/kicad-book-zh.html`、全部源 `.md`、`yuyu-book/screenshots/`（27 张 + README 来源表）、`yuyu-book/sources.json`、三张 OSS 工作流 SVG。评审方式：通读新增截图所在章节上下文，逐张比对新增截图像素与 caption，抽查 PDF 文本/页码/书签/来源页，核对登记与图号。全文以阅读证据为准；未运行 `tools/` 回归脚本（任务书列为可选）。

## Overall

Score: 6/10（5–6 档：存在影响读者正确理解操作的问题，不属“小瑕疵可合并”档）
Verdict: Almost

Round 5 在来源登记、许可边界、图号连续性与版式整洁度上达到可出版水准：27 张截图均有官方 URL、访问日期与许可说明，27 行登记与正文引用一一对应；78 个图号在 HTML 与 PDF 中唯一且无占位 caption；PDF 无空白页、书签指向正确；三张 OSS 工作流图的 MIT / AGPL 边界表述清楚，且未把示意图冒充实测参数。但两张新增正文截图的 caption 与图像内容直接矛盾：7.4 节把“两根走线同时调谐”的截图写成“单线蛇形”，恰好颠倒了本节差分对等长教学的关键点；13.4 节把仿真器的左右布局写反。按任务书“只要存在与承诺不符的问题，不得给出 Accept”的口径，本轮不能判 Accept；两处均为 caption 级修正，改动量小，故判 Almost 而非 BLOCK 档位（合并结论见末节）。

## Strengths（ranked）

1. **截图来源与许可登记完整、可逐张追溯。** `yuyu-book/screenshots/README.md` 为 27 张截图逐条给出 `docs.kicad.org/10.0/...` 官方 URL，文首声明“CC BY 3.0 或 GPLv3+”，文末记录访问日期 2026-11-26 与版本 10.0.8；`yuyu-book/sources.json` 的 `kicad-docs` 条目（第 3–11 行）明确“正文 8 张与附录 A.7 19 张界面截图均取自官方文档图片”，并按 eeschema / pcbnew / kicad / cli 分册记录深链接范围。全文没有把官方截图说成本地 GUI 捕捉的表述。
2. **6/8 张新增正文截图的 caption 与像素一致。** 图 3-3（`第一部分-入门篇/03-…` 对应 `eeschema-erc-single-marker.png`，PDF 第 37 页）确为 ERC 报告列表 + 带标记的 schematic 并排；图 4-4（`eeschema-cvpcb-main-window.png`，第 43 页）确为三栏 Assign Footprints 窗口；图 5-2（`pcbnew-board-setup-layers.png`，第 53 页）确为 Board Editor Layers 页；图 9-3（`pcbnew-drc-rule-editor.png`，第 93 页）确为规则树 + 表单 + Syntax help；图 10-3（`pcbnew-drill-files.png`，第 101 页）的 Origin 确为 Absolute，caption 明说“本书命令用 --drill-origin plot”，未把 GUI 与 CLI 混为一谈；图 15-3（`kicad-pcm-repository.png`，第 158 页）确为 Repository 页、左侧可见 InteractiveHtmlBom/KiKit、详情面板选中 KiBuzzard。
3. **图号体系干净。** 源稿 `图 N-M` 按章连续；HTML 中 78 个图号唯一、无重复、无空/占位 caption；PDF 中同样 78 个唯一图号，未见重复或错位；27 张截图全部实际嵌入（HTML 共 37 个 `<img>`）。
4. **三张 OSS 工作流插图事实与边界正确。** `yuyu-book/illustrations/kicad-ch11-ibom.svg`、`kicad-ch11-kikit.svg`、`kicad-ch15-kibot.svg` 的流程分别与上游一致：IBOM 产出自包含只读 HTML；KiKit 含 rails/array/fiducials 且写明“间距先问工厂”；KiBot 是 YAML 流水线、固定 commit/镜像 digest、失败时保留 artifact。MIT（IBOM、KiKit、jlcpcb-tools）与 AGPL-3.0（KiBot v1.9.1，commit `8a5106ec…`，Action `5c78b746…`，镜像 digest `sha256:96e75f88…`）在 `第四部分-进阶篇/15-自动化与插件.md` §15.7 及 PDF 第 204、208 页来源表中边界明确，未把社区工具误写成实测或工艺参数。
5. **版式与导航无回归。** PDF 211 页、25 项目录、0 空白页；书签抽样 p7 前言、p13 第一篇、p14 第 1 章、p32 第 3 章、p153 第 15 章、p169 附录 A、p203 来源与许可，指向均正确；新增截图未见裁掉关键信息或模糊到不可读（如等长调谐图 918×336 仍可辨走线）。

## Weaknesses（ranked CRITICAL > MAJOR > MINOR）

**1) MAJOR — 图 7-4 把“双线同时调谐”的截图说成“单线蛇形”，颠倒本节差分对等长的核心教学点**

- Severity: MAJOR（唯一影响读者正确理解操作的问题；非 CRITICAL，因紧随其后的正文步骤本身正确）
- Location: `第二部分-设计篇/07-布线.md` §7.4，图 7-4（源文件第 196–197 行；PDF 第 75 页）；截图 `yuyu-book/screenshots/pcbnew-length-tuning.png`
- Evidence: caption 原文“图示为单线蛇形；差分对要两根一起调”。截图像素中可见**两条并行走线同时被蛇形调谐**（多次独立视读一致确认；标签细节有 Txx / P、N 两种读法，但“两条走线”无争议）。同节正文紧接着给出差分对布线与调谐热键 8/9 的正确步骤，故错误集中在 caption 而非操作说明。
- Why it matters: 本节专门讲差分对“等长、等距、两根一起调”，caption 却把演示图说成单线，读者会误以为图中展示的是可只调一根的通用蛇形段，恰恰与本节强调的“差分对要两根一起调”相反；这是“图题与承诺不符”，按评分口径不能给 Accept。
- Smallest actionable fix: 只改这一句 caption，例如“图示为两根并行走线（差分对）同时蛇形调谐；单线等长时才只调一根”，其余正文与截图均不动。

**2) MINOR — 图 13-3 把仿真器左右布局写反**

- Severity: MINOR（描述性错误，不影响命令与仿真设置）
- Location: `第四部分-进阶篇/13-仿真与电路验证.md` §13.4，图 13-3（源文件第 174–175 行；PDF 第 138 页）；截图 `yuyu-book/screenshots/eeschema-simulator.png`
- Evidence: caption 原文“左侧管理信号与测量，右侧显示波形”。截图中大幅 AC 增益/相位波形图位于**左侧**（约占 2/3 宽），Signals 列表在右上、Measurement/Cursor 表在右下。同章 §13.4 正文第 3–4 步说“游标差值会直接显示在右侧的 cursor 表格里”，与截图一致、与 caption 相反。
- Why it matters: 按 caption 指引去左侧找 Signals 面板会找不到，削弱“真实界面截图对照操作步骤”的意图；同时形成同章正文与图题互相矛盾。
- Smallest actionable fix: 将 caption 中方位词对调为“左侧显示波形，右侧管理信号与测量”，其余文字保留。

未发现 CRITICAL 问题。另：图 10-3 caption 的“操作时切到 Plot / Drill / Place”为文字指引，截图本身显示的是 Generate Drill Files 对话框，未能在静态图中验证该切换动作，列入未确定项而非缺陷。

## Missing or wrong-context references

- 来源登记：`README.md` 27 行 URL 覆盖正文 8 张 + 附录 A.7 19 张；`check_book.py` 的截图契约要求每个嵌入文件都有 `| \`file\` | http(s)://… |` 行，抽样比对未见缺行、错链或本地捕捉声明；许可表述“CC BY 3.0 或 GPLv3+”与 `sources.json` 中 `GPL-3.0-or-later / CC BY 3.0` 一致，快照 10.0.8 / rev `8acc7624`、访问日期 2026-11-26 一致。
- 截图许可：官方界面截图仅作教学标识与说明，未把第三方截图冒充官方、也未把官方截图冒充本书案例；图 13-3 明说“官方文档的 AC 扫描示例，不是本板 RC 结果”，处理正确。
- 图号：正文与构建产物均为 78 个唯一图号，无重复编号、无占位/空 caption；上述两处属于 caption 内容与截图语境不符，不是来源登记或编号错误。
- OSS 边界：IBOM/KiKit 的 MIT 与 KiBot 的 AGPL-3.0 在来源表与 §15.7 均正确；书中说明“调用上游 action 不改变本书许可；复制进自己仓库再分发需按 AGPL 履行义务”，边界无误。

## Visual review

- 抽样页面：PDF 第 37（图 3-3）、43（图 4-4）、53（图 5-2）、75（图 7-4）、93（图 9-3）、101（图 10-3）、110–116（第 11 章工作流图）、138（图 13-3）、158（图 15-3）、203–211（来源与许可）页。
- 版式/裁剪：截图所在页未见溢出、压字、空白占位；图 7-4 为 918×336 的画布裁剪图（无窗口边框），细节仍可辨认；其余新增截图尺寸足以辨认面板文字。
- 图题/截图一致性：8 张新增截图中 6 张 caption 与像素吻合（详见 Strengths 2），2 张不符（详见 Weaknesses 1、2）。
- 图号/目录/导航：PDF 25 项目录、0 空白页、书签页码抽样正确；HTML 27 张截图全部嵌入、78 图号唯一。
- 来源页：第 204 页记录 KiBot 固定版本与 AGPL-3.0，第 208 页列 IBOM/KiKit/jlcpcb-tools 均为 MIT，第 209 页说明社区材料“仅引用事实，不复用代码/截图”。

## Remaining uncertainties

- 未运行 `tools/` 下的回归脚本（任务书标明可选）；本评审结论完全来自静态阅读与图像核对。
- 未访问 `docs.kicad.org` 验证 27 条 URL 是否仍可解析（任务书限制不下载大文件）；来源表内部一致性已核对。
- 图 7-4 中走线标签是 `T01/T02…` 还是含 P/N 标记，不同次视觉读取结论不一致；但“两条并行走线同时调谐”这一事实多次一致，缺陷判定不依赖标签读法。
- 仅对 8 张新增正文截图做了逐像素 caption 比对；附录 A.7 的 19 张只核对了登记与抽样呈现，未逐张做像素级比对。
- PDF 未做全页逐页渲染目视检查（以文本抽取、页面计数、书签与抽样页为依据）。

## Merge verdict: BLOCK

独立结论：本轮**不可合并**。两张新增截图的 caption 与图像内容直接矛盾，其中图 7-4 颠倒了差分对等长教学的关键点，触发任务书“与承诺不符即不得 Accept”的判定线；虽均为一行文字修正、工作量极小，但在修正前合并会把错误图题带入出版产物。修正图 7-4、图 13-3 两处 caption 并复核后，可改判 ACCEPT；其余部分（来源、许可、图号、版式、OSS 边界）无合并障碍。
