# Round 4 Review — 《KiCad 从原理到制板》

## Overall

- Score 8/10
- Verdict Almost
- Merge BLOCK
- MAJOR 1
- MINOR 3
- confidence 0.84

结论：书稿内容、技术叙述与构建产物整体可靠，205 页 PDF / 25 书签 / 0 空白页、SVG/插图/照片/截图计数及 CLI 参数均可独立复核。阻塞点是交付规范与交付产物互相矛盾：`STRUCTURE.md` 仍写“HTML 构建大小 < 1MB”，而 README 与实际 HTML 均为约 5.6MB。该问题一行即可修复，但修复前不能按现有交付标准放行。

## Strengths (ranked)

1. 可独立复核的产物指标：实测 Markdown 23 个文件、非 README/STRUCTURE 字符 154,676（15.468 万）、汉字 61,094（6.109 万）；SVG 资产 62、教学插图引用 37、实物照片 10、官方截图 19，与 README 逐项一致。PDF 实测 205 页、25 书签、0 空白页，13,971,714 B（约 14.0MB）；HTML 5,599,223 B（约 5.6MB）。
2. 命令与 CLI 标志不是凭记忆写的：`kicad-cli` 手册存档（`.tmp/kicad-cli.md:172,193,1066,1085`）确认 `--severity-all`、`--exit-code-violations`（退出码 5）、`--schematic-parity`、`--refill-zones`、`--use-drill-file-origin`、`--generate-map` 等参数存在且语义与书中一致。
3. 版本边界主动披露而非掩盖：正文按 KiCad 10.0.8 写，KiBot 镜像实际为 10.0.5，已在 `第四部分-进阶篇/15-自动化与插件.md:408,421` 和 `yuyu-book/sources.json:515` 明确说明，并给出严格复现路径。
4. 渲染层图号自动重排且有回归保护：`yuyu-book/yuyu_book/render.py:307,344` 与 `tools/test_book_metadata.py:90-109` 确保源稿手写重复图号不会在成书里重复；本次 PDF 扫描 48 个图题，按章连续、无重复。
5. 来源登记可追溯：`yuyu-book/sources.json` 对 KiCad、库许可、截图、社区工具、Docker 镜像 digest 均记录了 URL、快照与用途边界；未把“引用性使用”冒充自有授权。
6. 技术表述克制：第 7 章拒绝把高速规则无条件套到慢板，第 12 章把 USB 供电握手失败限定在供电范围并附示波器接地警告，第 13 章明确 `1M`/`1Meg` 的大小写陷阱与“仅二端 R/L/C 推断模型”的边界。

## Weaknesses (ranked)

### MAJOR 1 — 交付标准与产物自相矛盾（HTML 体积）

- severity: MAJOR
- location: `STRUCTURE.md:95`；对照 `README.md:76`
- evidence: `STRUCTURE.md:95` 写“HTML 构建大小 < 1MB，无外部依赖，完全离线可用”。实测 `yuyu-book/dist/kicad-book-zh.html` 为 5,599,223 B（5.34 MiB，十进制 5.60 MB），README 也写“约 5.6MB”。超标约 5.6 倍。
- why it matters: 这是贡献者/构建验收契约，不是读者可见的内容错误；但按文档标准构建永远“不合格”，且 `tools/check_book.py` 与 CI 都不检查这一条，形成纸面标准与真实产物长期分叉。
- smallest actionable fix: 将 `STRUCTURE.md:95` 的阈值改为与实际一致（如“HTML 构建大小 < 8MB，单文件离线可用”），或删掉数字并指向 README；同时新增一个确定性检查，从 `README.md` 与产物大小各取一次值，断言不再出现 1MB 表述。

### MINOR 2 — README 字数/字符数陈旧（仍在容差内）

- severity: MINOR
- location: `README.md:9`、`README.md:56`
- evidence: README 两处写“约 14.9 万字符（6.0 万汉字）”。独立统计 23 个章节/附录 Markdown（排除 README、STRUCTURE）为 154,676 字符（15.468 万）、61,094 汉字（6.109 万）。字符差约 3.8%、汉字差约 1.8%；`tools/check_book.py:604,607` 的 5% 容差使其通过，因此不是构建失败，但公开数字偏低。
- why it matters: 对外统计口径应准确；容差掩盖了缓慢漂移，下一次编辑可能越界。
- smallest actionable fix: 把两处改为“约 15.5 万字符（6.1 万汉字）”，保留现有 5% 回归检查即可。

### MINOR 3 — 源稿中手写图号重复/乱序（成书不可见）

- severity: MINOR
- location: `第一部分-入门篇/04-从符号到封装.md:84,124`；`第二部分-设计篇/06-布局.md:35,86`；`第三部分-制造篇/10-输出制造文件.md:78,235`；`第三部分-制造篇/12-焊接调试与返修.md:40,82,99,103,242,284`
- evidence: 源稿存在“图 4-3”两处、“图 6-1”两处、“图 10-2”两处，第 12 章“图 12-1”重复且“图 12-4”出现在“图 12-3”之前、缺“图 12-5”。但 `yuyu-book/yuyu_book/render.py:307,344` 会按文档顺序重排 `<span class="fig-no">` 并吸收手写图题，PDF 扫描的 48 个图题按章连续、无重复；`tools/test_book_metadata.py:90-109` 对此有回归。
- why it matters: 读者看到的 HTML/PDF 没问题；但直接读 Markdown 的贡献者会看到矛盾编号，且重排机制一旦被改动，这些源稿隐患会立即变成读者可见缺陷。
- smallest actionable fix: 删除上述行里手写的图号（或改成“见本章对应插图”的纯文字描述），并加一个源稿 lint：逐章扫描 `图 N-M` 形式，断言编号严格递增且不重复。

## Missing or wrong-context references

- 版本表述“KiCad 10.0.8 vs KiBot 镜像 10.0.5”不是矛盾：`第四部分-进阶篇/15-自动化与插件.md:408` 明确说明 `v2_k10` 固定代码与 10.x 线而非精确补丁版，`:421` 给出验证边界，`yuyu-book/sources.json:515` 记录 `/etc/kiauto_tag` 与 index digest。属于正确上下文，不需要修改。
- 第 11 章把 InteractiveHtmlBom、KiKit、kicad-jlcpcb-tools 称为 MIT 社区项目；`yuyu-book/sources.json:112-137` 记录相同许可。这是**仅文档/来源页层面**的断言，本次未抓取上游 LICENSE 文件复核，不能升级为“已验证”。
- 第 12 章 Tektronix 探头 primers、Microchip AN2648 §3.1，第 13 章 KiCad 10 eeschema “Value notation” 与 ngspice manual 均为**仅文档引用**；本次只对 `.tmp/kicad-cli.md` 的命令手册做了本地逐条核对，未联网取回这些文档正文。
- 第 7 章 `:126,155,264` 的拐角/残桩 RC 量级与 `:93,95,99,114` 的 `BW=0.35/RT`、`TD>0.2·RT`、6.7 ps/mm 表均自行复算一致；但 RC 数值只有在假定走线特性阻抗一半（约 25 Ω）作为拐角/残桩等效电阻时才成立，该假定未在正文写明。未列为 finding（缺少可引用的明确公式行），列入 uncertainties。
- 第 7 章 `:99` 表格中 0.25 mm 线宽/1.5 mm 介质/er=4.3 的微带线 Z0 与按 Hammerstad 公式复算值存在候选偏差；本次未确认 `check_book.py:check_si_numbers()` 实际解析的是哪一行及其容差，不据此报缺陷，列入 uncertainties。

## Visual review (PDF pages)

- 用 PyMuPDF 对 `yuyu-book/dist/kicad-book-zh.pdf` 逐页抽取：205 页、25 书签、0 空白页；图题扫描 48 个，按章序号连续（0-1；1-1…1-2；2-1…2-5；3-1…3-2；4-1…4-4；5-1…5-3；6-1…6-4；7-1…7-3；8-1…8-3；9-1…9-3；10-1…10-3；11-1…11-3；12-1…12-6；13-1…13-2；14-1…14-2；15-1…15-2），无重复。
- 交付 PDF 与 `kicad-book-zh-round3.pdf` 字节一致；HTML/PDF 元数据均为 v0.1.3、2026-11-25，作者 KKiCad 教学组，generator yuyu-book，与 `yuyu-book/manifest.json` 一致。
- 限制：未把页面栅格化为图像，未人工检查版式、字体回退、断行、SVG 对比度或暗色模式；上述结论只覆盖文本层与结构层。

## Remaining uncertainties

- 本机无 Docker/KiBot 运行时，未在 KiBot 镜像内实际执行 `.kibot.yaml`；书稿 `:421` 已声明这一验证边界。KiCad 容器 CI 示例同样未实跑（`:273` 已声明）。
- `yuyu-book/sources.json:515` 的镜像 tag/digest 是 2026-11-26 静态快照；未重新拉取镜像核对 `/etc/kiauto_tag`。
- 上游 LICENSE 文件与 Tektronix/Microchip/ngspice/KiCad 文档正文未联网抓取；相关技术断言为文档级引用。
- `config_file` 分支的 KiBot schema 校验结果未形成可稳定引用的日志片段，因此本次不把它当作独立的正确性证明；仅确认 YAML 可被解析且键名与官方 schema 的字段名对齐。
- 第 7 章等效阻抗假定、微带 Z0 表值两项候选偏差未完成可引用定位，需补一次带行号的公式复算才能定级。

## Merge verdict

BLOCK（待一处一行修复后转 ALLOW）。内容与技术叙述可放行；唯一阻塞项是 `STRUCTURE.md:95` 的 HTML 体积标准与产物/ README 矛盾。建议同一提交顺手更新 README 两处字数，使公开数字与源稿一致。两项均不要求重建 HTML/PDF，也不需要改动回归测试的判定逻辑（新增源码图号 lint 为可选 hardening）。
{"score":8,"verdict":"Almost","merge":"BLOCK","major_count":1,"minor_count":3,"confidence":0.84}
