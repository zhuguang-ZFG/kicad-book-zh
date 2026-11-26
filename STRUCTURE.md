# 仓库结构

本文是本书的开发规范、版本管理和交付说明，面向贡献者。

## 目录结构

```text
usb_breath_led/             # 读者按章节建立的工程（不随书附带）
├── usb_breath_led.kicad_pro
├── usb_breath_led.kicad_sch
├── usb_breath_led.kicad_pcb
├── ...
└── fab/                     # 参考制造输出

第一部分-入门篇/             # 第一篇章节
第二部分-设计篇/             # 第二篇章节
第三部分-制造篇/             # 第三篇章节
第四部分-进阶篇/             # 第四篇章节
附录/                       # 附录

.github/workflows/ci.yml      # 测试、检查与 HTML/PDF 构建

yuyu-book/                   # yuyu-book 构建器
├── yuyu_book/               # Python 包
├── manifest.json            # 书结构定义
├── sources.json             # 来源与参考引用
├── requirements.txt         # 构建与 PDF 依赖
├── illustrations/           # 手绘 SVG、实物照片与许可说明
├── screenshots/             # KiCad 10 官方界面截图（CC BY 3.0）
└── dist/                    # 构建产物，不提交

tools/                       # 开发脚本
├── ink.py                   # 手绘 SVG 生成器
├── make_emblems.py          # 生成章节徽章
├── make_plates.py           # 生成篇题与封面
├── make_figures.py          # 生成正文插图
├── check_book.py            # 内容事实检查（含信号完整性数字反算）
├── test_claims.py           # 声明措辞回归测试
├── test_usb_diagnostics.py  # USB 诊断措辞回归测试
├── test_book_metadata.py    # HTML 元数据与图号回归测试
├── test_readme_links.py     # README 相对链接回归测试
└── test_si_numbers.py       # 信号完整性数字闸门的变异测试

docs/                        # 预览、截图、发布包
.gitignore
README.md                    # 读者阅读的使用说明
STRUCTURE.md                 # 本文件
```

上图中的 `usb_breath_led/` 是读者按章节建立的目标结构，不是本仓库现有文件。

## 开发流程

1. 章节内容变更必须同时更新事实检查脚本中的对应规则；
2. 新插图必须符合 SVG 安全契约（无 `<script>`/`<style>`/`id`/`href`/`url()`，全用 `currentColor`），单文件小于 24KB；
3. 所有工具必须用 Python 3.12+ 标准库（除 playwright/pymupdf 等构建依赖）；
4. 提交前必须通过以下检查：
   - `python tools/test_claims.py`
   - `python tools/test_usb_diagnostics.py`
   - `python tools/test_readme_links.py`
   - `python tools/test_book_metadata.py`
   - `python tools/test_si_numbers.py`
   - `python tools/check_book.py`
   - `cd yuyu-book && PYTHONPATH=. python -m yuyu_book --check --mermaid source`
5. 版本更新时更新 `manifest.json` 中的日期和版本号。
6. 关键词式事实检查必须同时覆盖应拒绝的诊断用语与应接受的否定/解释用语；否定用例应包含自然长表述，并确认同段后续独立诊断仍会触发。
7. README 的本地 Markdown 链接必须由 `check_book.py` 验证目标存在；回归覆盖损坏路径、编码路径与应忽略的外链/代码示例。
8. 书中出现的可计算数字（带宽、时延门限、拐角/残桩电容、阻抗、参考面宽度）必须在 `check_book.py` 里由同一组常数反算；新增这类数字时同时补 `tools/test_si_numbers.py` 的变异用例，证明闸门会红。
9. 第三方 action 的版本必须与官方发行说明核对；主版本、运行时前提与破坏性变更要写进正文，不要只改 YAML。

## 内容规范

### 术语

- 优先使用中文术语，首次出现标注英文原名（如“设计规则检查（DRC）”）；
- 单位使用公制，英制标注在括号中（如“0.3 mm / 12 mil”）；
- KiCad UI 元素保留英文名称，首次出现给出中文含义；
- 章节标题采用“第 N 章：标题”，附录采用“附录 X：标题”。

### 格式

- 使用完整全角中文标点，中英文、数字之间留半角空格；
- 代码、命令、文件名使用反引号；
- 重要提示使用 `> **提示：**`、`> **警惕：**`、`> **版本差异：**`；
- 表格列对齐，数值项右对齐，文本项左对齐。

### 插图

- 所有插图使用手绘墨线风格，无渐变、填充图案；
- 插图下方必须有图题，正文首次引用解释含义；
- 代码、命令、文件列表优先用文本，不截图。

## 交付标准

- HTML 构建大小 < 8MB（当前约 5.6MB），单文件、无外部依赖、完全离线可用；
- PDF 构建无错误，书签、目录、页码正确；
- 所有链接、引用、脚注可跳转；
- 所有代码块语法高亮；
- 所有插图对比度 ≥ 4.5:1，适合暗模式自动重绘。

## 版本号规则

- 主版本（1.x）：新增章节、重大结构变更；
- 次版本（x.1）：内容更新、错误修正；
- 补丁版本（x.x.1）：拼写、格式、插图修正。
