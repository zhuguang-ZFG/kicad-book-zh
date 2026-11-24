# 附录 B：文件格式与工程结构

> 本附录不要求你手写 s-expression，但要求你能在出问题时用文本编辑器定位：文件有没有版本号、对象有没有丢、路径有没有断。

## B.1 工程目录

一个 KiCad 工程**至少**包含一个工程文件、一份原理图和一块 PCB；这三者由项目管理器的 **File → New Project** 一次性创建、主名相同，放在同一个新建子目录里。其余文件都按需出现，不是每个工程都有。下面是读者自己的 `usb_breath_led` 工程在完成前几章、并按需配置后的“可能全貌”，本书不附带这些文件：

```text
usb_breath_led/
├── usb_breath_led.kicad_pro        # 必：工程设置（JSON），原理图与 PCB 共享
├── usb_breath_led.kicad_sch        # 必：根原理图（s-expression）
├── usb_breath_led.kicad_pcb        # 必：PCB（s-expression）
├── sym-lib-table                   # 可选但推荐：工程符号库表
├── fp-lib-table                    # 可选但推荐：工程封装库表
├── lib/                            # 可选：第 14 章的工程本地库
│   ├── symbols/                    # .kicad_sym 打包库
│   └── footprints/                 # .pretty/ 目录，内含 .kicad_mod
├── power.kicad_sch                 # 仅层次图才有；基础工程是单页，没有这些
├── mcu.kicad_sch
├── io.kicad_sch
├── usb_breath_led.kicad_dru        # 可选：自定义设计规则
├── usb_breath_led.kicad_wks        # 可选：自定义图纸（页面布局）
├── usb_breath_led.kicad_jobset     # 可选：输出作业集
├── fab/                            # 可选：制造输出目录
├── usb_breath_led.kicad_prl        # 本机界面状态，自动生成，不提交
├── fp-info-cache                   # 封装库加载缓存，自动生成，不提交
└── usb_breath_led-backups/         # 自动备份目录，不提交（不是 .kicad_sch-bak 文件）
```

**三类文件要分清**：

- **读者必做（核心）**：`.kicad_pro` + `.kicad_sch` + `.kicad_pcb`，由 **File → New Project** 一起生成；用了工程本地库时再加两个库表和 `lib/`。
- **可选增强**：子页（只有层次图才需要）、`.kicad_dru`、`.kicad_wks`、`.kicad_jobset`、3D 模型。它们都不是跑通 ERC/DRC 或出制造文件的前置条件。
- **自动生成、不要提交**：`.kicad_prl`、`fp-info-cache`、`<工程名>-backups/`。备份也可在 **View → Panels → Local History** 中查看与恢复，不必翻文件。

## B.2 核心文件速查

“谁生成”一栏要连起来读：**.kicad_pro / .kicad_sch / .kicad_pcb 三份都由项目管理器的 File → New Project 同时创建、主名相同**，随后各自在对应编辑器里保存。其余文件由各自的编辑器或对话框按需生成。“分发”一栏是团队交付/提交 Git 的建议。

| 扩展名 | 内容 | 格式 | 谁生成 | 分发 |
| --- | --- | --- | --- | --- |
| `.kicad_pro` | 工程设置：原理图与 PCB 共享的设置、网类、设计规则 | JSON | **项目管理器 File → New Project**；项目管理器维护 | 必提交 |
| `.kicad_sch` | 原理图（符号/导线/标签/层次），含符号与连接信息 | s-expression | **项目管理器 File → New Project**；原理图编辑器保存 | 必提交 |
| `.kicad_pcb` | PCB（板框/封装/走线/铺铜），含除页面布局外的板级信息 | s-expression | **项目管理器 File → New Project**；PCB 编辑器保存 | 必提交 |
| `sym-lib-table` | 符号库表：符号编辑器可用的库清单 | s-expression | **Preferences → Manage Symbol Libraries…** 写入；工程表在工程目录，全局表在配置目录 | 若工程依赖工程专用库表，随表引用的库一起提交 |
| `fp-lib-table` | 封装库表：PCB 编辑器可用的库清单 | s-expression | **Preferences → Manage Footprint Libraries…** 写入 | 若工程依赖工程专用库表，随表引用的库一起提交 |
| `.kicad_sym` | 符号库：打包库是一个文件，解包库是 `.kicad_symdir` 目录下的多个文件 | s-expression | 符号编辑器 | 用了才提交 |
| `.pretty/` | 封装库目录，目录本身即库 | 目录（含 `.kicad_mod`） | 封装编辑器 | 用了才提交 |
| `.kicad_mod` | 单个封装 | s-expression | 封装编辑器 | 同上 |
| `.kicad_dru` | 针对某个 `.kicad_pcb` 的自定义设计规则 | 规则文本 | Board Setup → Custom Rules / 图形设计规则编辑器 | 用了才提交 |
| `.kicad_wks` | 图纸（页面布局：图框与标题栏）描述文件 | KiCad 文本格式 | 图纸编辑器（Drawing Sheet Editor） | 用了才提交 |
| `.kicad_jobset` | 输出作业集 | JSON | **项目管理器 File → New Jobset File…**，在项目管理器标签页编辑 | 用了才提交 |
| `.kicad_prl` | 本机界面状态（层可见性、选择过滤器等） | JSON | 自动生成 | **不提交、不分发** |
| `fp-info-cache` | 封装库加载缓存 | 二进制缓存 | 自动生成 | **不提交、不分发** |
| `<工程名>-backups/` | 自动备份快照/压缩包 | 目录 | 自动生成（保存与自动保存触发） | **不提交** |

> **纠正一个常见误写**：备份不是 `.kicad_sch-bak` 这种“扩展名文件”。KiCad 10 的自动备份放在工程目录下的 `<工程名>-backups/` 目录里，也可通过 **View → Panels → Local History** 查看和恢复。

## B.3 一个原理图文件的开头

```text
(kicad_sch (version 20260306) (generator "eeschema") (generator_version "10.0")
  (uuid 4f3c2a1e-...)
  (paper "A4")
  (lib_symbols
    (symbol "Device:R" ...)
  )
  (junction (at 63.5 45.72) (diameter 0) (color 0 0 0 0))
  (wire (pts (xy 63.5 45.72) (xy 76.2 45.72))
    (stroke (width 0) (type default))
    (uuid ...)
  )
  (symbol (lib_id "Device:R") (at 63.5 45.72 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid ...)
    (property "Reference" "R1" (at 66.04 44.45 0))
    (property "Value" "10k" (at 66.04 46.99 0))
    (property "Footprint" "Resistor_SMD:R_0805_2012Metric" ...)
  )
)
```

要点：

- `version` 是文件格式版本，不是 KiCad 版本；
- `lib_symbols` 缓存了用到的符号定义，所以别人没有你的库也能打开（但封装仍要库）；
- 每个对象有 `uuid`，用于交叉引用和更新；
- 属性是字符串键值对，BOM 字段就在这里。
- **别把缓存当成库**：`lib_symbols` 让原理图在没有符号库时也能显示，但“从库更新符号”、编辑库中的符号定义仍需要库表与库文件；PCB 的封装几何内嵌在 `.kicad_pcb` 里，自定义规则却在单独的 `.kicad_dru`，页面布局在 `.kicad_wks`。要完整交付，带上 `.kicad_pro` 和用到的库。
- **版本号怎么看**：`version` 是**文件格式版本**，不是 KiCad 发布号。示例中的具体数字用于展示字段形式，不代表所有发行版都保存为同一值；格式升级后版本值可能变化。不要手抄到旧文件或手工修改，以本机保存出的文件为准；`generator` / `generator_version` 才是编辑器与版本标记。

## B.4 一个 PCB 文件的开头

```text
(kicad_pcb (version 20260206) (generator "pcbnew") (generator_version "10.0")
  (general (thickness 1.6))
  (paper "A4")
  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (32 "B.Adhes" user "B.Adhesive")
    ...
  )
  (setup
    (pad_to_mask_clearance 0)
    (pcbplotparams ...)
  )
  (net 0 "")
  (net 1 "GND")
  (footprint "Resistor_SMD:R_0805_2012Metric"
    (layer "F.Cu") (at 100 80)
    (property "Reference" "R1" ...)
    (pad "1" smd roundrect (at -0.9125 0) (size 1.025 1.4) (layers "F.Cu" "F.Paste" "F.Mask"))
    ...
  )
  (segment (start 100 80) (end 105 80) (width 0.25) (layer "F.Cu") (net 1))
)
```

要点：

- `layers` 定义层号与类型；
- `net` 定义网络编号与名字；
- `footprint` 是封装实例，`pad` 是焊盘；
- `segment` 是走线，`via` 是过孔，`zone` 是铺铜。
- **“自带全部板级信息”有边界**：官方文件表把 `.kicad_pcb` 描述为“除页面布局外包含全部信息”。封装几何、网络、走线都在文件里，所以单独打开 PCB 也能看到板子；但自定义设计规则在 `.kicad_dru`，自定义图框在 `.kicad_wks`，工程级设置（网类等）在 `.kicad_pro` —— 这些没跟上，就会出现“看起来对、规则不对”的情况。

## B.5 库表格式

`sym-lib-table`（工程表放在工程目录；全局表放在 KiCad 用户配置目录）：

```text
(sym_lib_table
  (version 7)
  (lib (name "Device")(type "KiCad")(uri "${KICAD10_SYMBOL_DIR}/Device.kicad_sym")(options "")(descr "Generic devices"))
  (lib (name "usb_breath_led")(type "KiCad")(uri "${KIPRJMOD}/lib/symbols/usb_breath_led.kicad_sym")(options "")(descr "Project symbols"))
)
```

`fp-lib-table` 结构相同，只是条目指向 `.pretty` 目录：

```text
(fp_lib_table
  (version 7)
  (lib (name "usb_breath_led")(type "KiCad")(uri "${KIPRJMOD}/lib/footprints/usb_breath_led.pretty")(options "")(descr "Project footprints"))
)
```

变量（用 **Preferences → Configure Paths…** 查看/设置）：

- `${KIPRJMOD}`：当前工程目录的绝对路径。库放在工程里就写 `${KIPRJMOD}/...`，整个目录搬走也不会断。
- `${KICAD10_SYMBOL_DIR}` / `${KICAD10_FOOTPRINT_DIR}`：KiCad 10 自带的官方符号/封装库目录；旧变量如 `${KICAD9_SYMBOL_DIR}` 会自动解析到当前版本对应变量，前提是没有在本机显式定义旧变量。
- 3D 模型路径也可以用变量；模型缺失时先查封装里的模型路径与 **Configure Paths…**。

**两条实用判断**：① 工程表只在该工程打开时生效，全局表对所有工程生效；只有工程依赖本地库时才需要把工程表和引用的库一起交付。② 绝对路径在目标机器/用户下不存在时会断链；工程本地库优先用 `${KIPRJMOD}/...`，避免依赖某个人的盘符或 home 目录。

## B.6 版本与兼容性

- 主版本（10.0 → 11.0）可能改变文件格式；
- 点版本（10.0.1 → 10.0.8）只修 bug，不改格式；
- 新版本能打开旧文件，旧版本不能打开新主版本保存的文件；
- 库格式在 KiCad 6 有过一次大迁移，旧库需要升级。

升级流程：

1. 备份整个工程；
2. 用新版本打开，逐个保存；
3. 跑 ERC/DRC；
4. 检查 3D 模型/库路径；
5. 提交一条“升级到 10.x”的独立 commit。

> **警惕：**不要在一次提交里同时升级版本和改电路。出问题时，你无法区分“升级导致”还是“改动导致”。

## B.7 文本 diff 的读法

原理图/PCB 是文本，Git diff 可读，但对象顺序可能变化。看 diff 时关注：

- `property "Reference"` / `"Value"` / `"Footprint"` 的变化；
- `net` 编号/名字的变化；
- `segment`/`via` 的新增/删除；
- `zone` 的填充参数；
- `uuid` 变化通常意味着对象被重建，不一定是电气变化。

如果 diff 太大，先看 `.kicad_pro` 是否被格式化/重排；有些编辑器会重写整个文件。

## B.8 文件损坏与库缺失的急救

先备份整个工程目录（含 `.kicad_pro`），再按现象动手：

| 现象 | 先查什么 | 恢复动作 |
| --- | --- | --- |
| `.kicad_sch` 打不开 | `<工程名>-backups/` 快照，或 **View → Panels → Local History** 的快照事件 | 用 Local History 的 **Restore Commit** 恢复；不要“新建工程再复制”，容易丢网络和属性 |
| `.kicad_pcb` 打不开 | 同上；再考虑用文本编辑器删掉最后一次新增、括号已配对的对象 | 改前先复制一份原文件 |
| 符号缺失 / “库未找到” | `sym-lib-table` 工程表条目及其 `uri`；库文件是否还在 `lib/` | 放回库文件与表文件；把绝对路径改回 `${KIPRJMOD}/...`；再跑 **Tools → Update Symbols from Library…** |
| 封装缺失 | `fp-lib-table` 与 `.pretty/` 目录 | 同上，再跑 **Tools → Update Footprints from Library…** |
| 3D 模型缺失 | 封装里的模型路径、**Configure Paths…** 的变量 | 补齐模型文件或修正变量；仅影响 3D 视图，不阻塞 ERC/DRC |
| 板子显示正常但规则不对 | `.kicad_pro`（网类/设计规则）、`.kicad_dru`、`.kicad_wks` 是否随工程交付 | 从 Git 或备份补回这些文件，重跑 DRC |

可复现的完整演练见第 14 章 14.7：移走库表/`lib/` → 记录“找不到库” → 放回并修正路径 → 确认恢复。背景：原理图/PCB 内嵌了符号与封装，所以画面通常还在；真正依赖外部库的是“从库更新”等操作，以及 `.kicad_pro` 里的工程级设置。

### 本附录官方依据（KiCad 10.0.8，文档修订 8acc7624）

- 工程文件分类、谁生成、分发建议：`https://docs.kicad.org/10.0/en/kicad/kicad.html` → *Using the KiCad project manager*（New Project 后的文件表）、*Project files*、*Project backups and autosave*、*Jobsets*。
- 三份核心文件同时创建、备份目录：`https://docs.kicad.org/10.0/en/getting_started_in_kicad/getting_started_in_kicad.html` → *First project creations*（File → New Project 一段）。
- 库表与路径变量：`https://docs.kicad.org/10.0/en/eeschema/eeschema.html` → *Managing symbol libraries*；`https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html` → *Managing footprint libraries* / *Path variable substitution*。
- 3D 模型与本地历史：`https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html` → *3D models (STEP / GLB / BREP / XAO / PLY / STL / STPZ / U3D / PDF)*；`https://docs.kicad.org/10.0/en/kicad/kicad.html` → *Project backups and autosave*。
- `.kicad_wks`：`https://docs.kicad.org/10.0/en/pl_editor/pl_editor.html` → *Introduction to the KiCad Drawing Sheet Editor*。
- 未决问题：官方文件表给出扩展名与用途，但没有逐项规定每种文件的精确格式名；本附录“格式”列按各编辑器实际保存形态归类，不当作 KiCad 文件格式规范。

