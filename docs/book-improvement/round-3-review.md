# Round 3 Review —《KiCad 从原理到制板》

## Overall
- **Score: 8/10**（Accept/ALLOW 档：无 CRITICAL、无 MAJOR；两项 MINOR 均为局部说明性问题，可在一行/一段内修正）
- **Verdict: Accept**

Round 3 关闭了 Round 2 唯一阻断合并的 MAJOR：重建后的 205 页 PDF（`kicad-book-zh.pdf` 与 `kicad-book-zh-round3.pdf` 的 MD5 完全相同，`cd335195…`）文本层共 48 个图号，**零重复、零跨页碰撞**，正文的“见图 X-Y”重新指向唯一图。Round 2 遗留的 MINOR #3 在指定范围内落地：`00-前言.md` 新增“基线范围与可选扩展”表并明确为唯一来源，第 7、8、13 章的整段复述被压缩，安全/否定/测量边界逐句保留。新增 §15.7 的 action SHA、输入名、YAML 语义、版本与许可边界均能独立核验，且明确写出“只做 schema 校验、未在镜像内实跑”。未发现回归。

## Strengths（ranked）

1. **Round 2 的 MAJOR 真正关闭，且是成品级证据。** 独立抽取两个 Round 3 PDF 的全部“图 N-M”标记：48 个唯一编号、0 个重复、0 个跨页冲突；205 页、25 个书签、无空白页。Round 2 第 42/58/98/116/119/124 页的编号碰撞不再出现。`docs/book-improvement/state.json` 指向的 `kicad-book-zh-round3.pdf` 与 README 指向的 `kicad-book-zh.pdf` 是同一文件（MD5 一致），不存在“审了 A、发布 B”的错位。

2. **基线去重按“保留边界句、删掉整段复述”执行，没有误删安全信息。** `00-前言.md` 第 51–60 行的表把原理图/PCB/制造/验证四段基线一次说清；第 7/8/13 章的压缩逐项可核对：`07-布线.md` 第 114 行测量边界“本板不需要阻抗控制、不需要等长、不需要仿真”保留，§7.4 开篇仍写明供电版没有 D+/D- 可跳过；`08-铺铜与电磁兼容.md` 第 132 行选读提示、第 155–159 行逐项适用条件、第 198 行验收句“本板无射频模块，此项不适用”保留；`13-仿真与电路验证.md` 第 219 行改为指向前言表，第 273 行“本板无数据线，不适用”保留。

3. **新 §15.7 的可核验技术细节全部对得上上游。** GitHub API 实测 `v2_k10` 注解标签解引用到 `5c78b746f9076d54242aeeeae7f364f360e21f30`；该 SHA 的 `action.yml` 确有 `config`/`schema`/`board`/`dir` 四个输入，`runs.args` 逐项传入；`actions/checkout@v7` 与 `actions/upload-artifact@v7` 两个 tag 均真实存在。从正文抽取的 `.kibot.yaml` 用缓存的 KiBot v1.9.1 `schema.json` 以 Draft7 校验为 **0 error**；并通过注入伪键证明校验器对各层均严格（preflight 顶层、erc/drc 嵌套、伪键都报错），所以“0 error”不是空校验。`${QUANTITY}` 与上游 `COL_QUANTITY` 一致，`output: '%f-bom.%x'` 与上游默认 `'%f-%i%I%v.%x'` 的占位符体系一致。

4. **版本与许可边界写得诚实，没有把静态检查冒充实跑。** `15-自动化与插件.md` 第 408–421 行逐条说明：`v2_k10` 只固定代码、Dockerfile 仍用 `ghcr.io/inti-cmnb/kicad10_auto_full:latest`；写作时镜像 `/etc/kiauto_tag` 为 `1.9.1-2_k10.0.5_d13.2_b4.2.4LTS`（KiCad 10.0.5）而本书按 10.0.8 核对；index digest 与实测响应头一致；AGPL-3.0 只引用不内嵌；第 421 行与验收第 464 行两次声明“schema 校验不算实跑证据”。这正面回应了上一轮对“版本漂移”的担忧。

5. **辅助改动正确且未隐藏内容。** `tools/check_book.py` 第 24–30 行的 `.tmp` 排除只影响草稿/参考材料（`manifest.json` 列出的全部书稿仍在真实章节目录），同时让字数统计不再把外部文档计入正文；README 的“16 个变异用例”与 `tools/test_si_numbers.py` 的 `MUTATIONS` 实际条数一致，“205 页 / 25 书签 / 14.0MB”与 PDF 实测一致。Round 2 的另一个 MINOR（`sources.json` 中 upload-artifact v4/v7 重复登记）也已关闭，现只剩 v7 一条。

## Weaknesses（ranked CRITICAL > MAJOR > MINOR）

无 CRITICAL、无 MAJOR。

### 1. Severity: MINOR — KiBot 的 `dir` 输入是配置内 `dir` 的前缀，示例实际产出 `fab/fab/...`
- **Location:** `第四部分-进阶篇/15-自动化与插件.md` 第 310 行（`dir: fab`）、第 321 行（“`dir` 是输出根目录”）、第 345/363/371/381 行（各输出 `dir: fab/gerbers` / `dir: fab`）；对照第 316 行 `path: fab/`。
- **Evidence:** 上游固定 SHA 的 `entrypoint.sh` 第 44 行原文：`'-d DIR' output path. Default: current dir, will be used as prefix of dir configured in config file`；同一 SHA 的 `action.yml` `runs.args` 把 `-d ${{ inputs.dir }}` 传给 KiBot。因此 `with.dir: fab` 与输出项 `dir: fab/gerbers` 拼接后得到 `fab/fab/gerbers`，Gerber/BOM/坐标并非第 321 行所暗示的 `fab/gerbers`。`actions/upload-artifact` 的 `path: fab/` 仍能收录嵌套文件，所以流水线不会失败——问题是“直接复用”示例中记录的目录结构与读者预期不符，且与 §15.6 直接写 `fab/gerbers/`（第 229 行）的布局不一致，练习 2 对比两套流水线时会看到无解释的差异。
- **Why it matters:** §15.7 的定位就是“照抄即可跑”，路径语义写错会让读者按文档去 `fab/gerbers/` 找不到文件，或误以为 KiBot 输出与 §15.6 不同源；这是可复现的读者可见偏差，但不影响检查是否执行、也不影响产物归档，故列 MINOR。
- **Smallest actionable fix:** 二选一：把 action 输入改为 `dir: .`（保留各输出的 `dir: fab/...`），或删掉四个输出项的 `dir:`（让 `with.dir: fab` 成为唯一根目录）；同时把第 321 行的“输出根目录”改为“输出前缀（会与配置中各输出的 `dir` 拼接）”，并在映射说明里加一句目录结果。改后无需重跑镜像，YAML 仍可通过同一 schema 校验。

### 2. Severity: MINOR — 前言宣称“后续章节不再整段复述”，但第 2 章仍保留整段基线复述
- **Location:** `00-前言.md` 第 52 行（“先把基线一次说清；后续章节只说明‘这项内容是否适用于本基线’，不再整段复述”）对照 `第一部分-入门篇/02-原理图第一笔.md` 第 17 行。
- **Evidence:** 第 2 章“必做/选做”提示仍整段写出“本书前四章的验收基线是**单张原理图 + ATtiny85 内部 RC 时钟 + USB-C 仅供电**……第 3 章的层次图、总线、设计变体是面向更大工程的可选扩展，不是完成基线的必要条件”，与前言表“原理图”行逐项对应。第 6 章第 143 行的“本项目基线”提示只服务于 CC 电阻摆放，属于就地操作依据，不算整段复述；第 5 章第 11/122 行同理。Round 2 的 MINOR #3 明确点名的是 §7.4/§7.7、§8.5–8.7、§13.6，这三处本轮已清干净。
- **Why it matters:** 前言用了“全书 / 不再整段复述”的全球性措辞，而实际只覆盖了指定章节；细心的读者会在第 2 章再遇到一次同样的话，削弱“唯一来源”的承诺。没有安全或否定边界丢失，不影响操作，属残留的编辑性问题。
- **Smallest actionable fix:** 把第 2 章第 17 行改为“基线见前言‘基线范围与可选扩展’表；本章先画最小系统，层次图/总线按第 3 章选读”，或把前言措辞收窄为“在第 7、8、13 章等重点章节不再整段复述”。

## Missing or wrong-context references

- **新增来源登记完整且可核验：** `yuyu-book/sources.json` 第 510–523 行的 `kibot` 条目含 HTTPS URL（指向 v1.9.1 commit `8a5106ec…`）、 `pinned.tag/commit`、访问日期、AGPL-3.0、`scope`，snapshot 中的 action SHA、镜像 tag、`/etc/kiauto_tag` 与 index digest 均与独立抓取结果一致；未发现错误上下文。
- **Round 2 来源重复已修：** `github-actions-upload-artifact`（v4）条目已不存在，只剩第 497 行的 v7 条目，其 `scope` 正确指向第 15 章。
- **未新增错误引用：** §15.7 中 KiBot issue #811（第 281 行，属 §15.6）已注明是旧版线索、不套用到 10.0.8；§15.7 的三个链接（KiBot 仓库、GHCR 镜像、KiCad CLI 手册语境）与正文说法一致。
- **第 9 个改动文件是工作流元数据：** `docs/book-improvement/state.json` 被更新为 `current_round: 3 / status: reviewing`，并新增 `round3_pdf` 等字段；它不进入书稿，也不影响读者可见内容，但任务书描述的“7/8 个改动文件”与实际 `git status` 的 9 个不一致，合并说明里应注明该文件用途。

## Visual review

- 抽样对象：`yuyu-book/dist/kicad-book-zh-round3.pdf`（与 README 指向的 `kicad-book-zh.pdf` MD5 相同）。独立确认 **205 页、25 书签**，无空白页候选；全文 48 个图号无重复、无跨页碰撞——Round 2 的 MAJOR 在成品中确认关闭。
- 第 155–161 页（§15.7 主体）：按文本块 Y 坐标排序复核，第 157 页为“工作流 YAML → 其后说明文字”，第 159 页为“BOM YAML → 与 §15.6 的对应关系 → §15.7.3 → 版本核验 bash”，与源码顺序一致；PyMuPDF 默认 `get_text()` 会把 prose 排到代码块之前，属于抽取顺序而非版面顺序。未见代码块被页边裁切、截断或倒置。
- 第 156 页起为 §15.7、第 160 页起为 §15.8；目录页给出第 15 章 p148、附录 A p163，与正文位置相容。
- 来源页卡片结构统一，KiBot 新条目在文末呈现为一张独立卡片（未与 v7 条目混排）。
- 未做全部 205 页的栅格级逐页目检；除上述范围外不宣称全页视觉验收通过。

## Remaining uncertainties

- 无 Docker，未在 KiBot 镜像内实跑工作流；因此只能确认 schema 合规与上游事实一致，不能确认 `warnings_as_errors` 与 `--severity-all --exit-code-violations` 在实际报告中完全等价，也不能确认 `fill_zones` 与 `check_zone_fills` 的“先重填、再检查”顺序（上游源码中 `Fill_Zones` 显式 `_priority = 10`，`Check_Zone_Fills` 用默认优先级，且文档说明 `check_zone_fills` 自身会在图层操作前临时填铜）。正文第 421/464 行已声明该边界，本项不升级为缺陷。
- 缓存的 `schema.json` 来自 KiBot v1.9.1 发布产物（同目录 `tag.tar.gz` 仅含镜像的 `/etc/kiauto_tag`，非源码包）；schema 文本个别条目提到“KiCad 11+”，但注入伪键测试证明其对本示例的键集是严格的。未在线重新拉取 schema 做二次比对。
- `kicad/kicad:10.0.8` 是否真的返回无后缀的 `10.0.8`，以及 GHCR 镜像 `latest` 在读者执行时的实际补丁版，均需首次运行时确认——正文已明确要求确认。
- 当前 `kicad-book-zh-round2.pdf` 为 200 页，而 Round 2 审查记录写的是 201 页；该历史产物可能被后续构建覆盖。此差异不影响 Round 3 结论，但引用 Round 2 页数时应以实物为准。
- 未运行任何构建或测试套件（按任务书“测试仅作辅助”口径）；README 的 205 页/16 变异用例为直接读取 PDF 与 `MUTATIONS` 得到的静态核对。

## Merge verdict: ALLOW

Round 2 的阻断 MAJOR（成品图号重复）已用成品 PDF 独立复核关闭；deferred MINOR #3 在指定章节关闭且未丢安全/否定/测量边界；§15.7 在可静态核验的层面准确，并对版本漂移与未实跑作了明确声明。剩余两项 MINOR 都是局部文字/路径说明问题，不阻断读者完成主线验收。建议合并时附带两项 MINOR 的修复（或记为下一轮编辑项）。

{"score":8,"verdict":"Accept","merge":"ALLOW","major_count":0,"minor_count":2,"confidence":0.88}
