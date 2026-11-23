# 附录 A：快捷键与界面速查

> 本附录按“在哪个编辑器里做什么”组织。快捷键以 KiCad 10.0.x 的默认配置为准；不同平台、不同主题可能略有差异，最终以 `Preferences → Hotkeys` 为准。
> 表中“无默认键”表示 KiCad 10 默认配置下未绑定该动作：请用菜单/工具栏执行，或在 `Preferences → Hotkeys` 里自行绑定。

## A.1 通用

| 操作 | 快捷键 | 说明 |
| --- | --- | --- |
| 保存 | `Ctrl+S` | 当前文件 |
| 另存为 | `Ctrl+Shift+S` | 当前文档另存到别处 |
| 撤销/重做 | `Ctrl+Z` / `Ctrl+Y` | 对话框内也支持（KiCad 10）；部分平台重做是 `Ctrl+Shift+Z` |
| 删除 | `Delete` | 删除选中对象 |
| 复制/粘贴 | `Ctrl+C` / `Ctrl+V` | 跨图纸粘贴时注意参考号 |
| 查找 | `Ctrl+F` | 打开查找对话框；搜索面板是 `Ctrl+G` |
| 缩放 | 滚轮 | 以光标为中心 |
| 全屏 | `F11` | 部分平台 |
| 切换单位 | `Ctrl+U` | mm / mil |
| 取消当前动作 | `Esc` | 第一次取消动作，第二次退出工具 |
| 显示热键表 | `Ctrl+F1` | List Hotkeys；`F1` 是“以光标为中心放大”，不是帮助 |

## A.2 原理图编辑器

| 操作 | 快捷键 | 说明 |
| --- | --- | --- |
| 放置符号 | `A` | Place Symbols |
| 放置导线 | `W` | Draw Wires |
| 放置网络标签 | `L` | Place Net Labels |
| 放置电源符号 | `P` | Place Power Symbols |
| 放置无连接标志 | `Q` | Place No Connect Flags；只用于“有意不接”的引脚 |
| 放置层次图 | `S` | Draw Hierarchical Sheets |
| 放置总线 | `B` | Draw Buses |
| 放置结点 | `J` | Place Junctions |
| 复制 / 重复 | `Ctrl+C` / `Ctrl+D` | `C` 是“从总线展开”，不是复制 |
| 旋转 | `R` | 逆时针 90° |
| 镜像 | `X` / `Y` | 水平/垂直 |
| 属性 | `E` | Edit properties |
| 编辑封装（选中符号） | `F` | 打开封装编辑器；批量分配走 `Tools → Assign Footprints`，无默认键 |
| ERC | 无默认键 | `Inspect → Electrical Rules Checker`；命令行 `kicad-cli sch erc` |
| 仿真 | 无默认键 | `Inspect → Simulator`；模拟器里 `R` = Run Simulation |
| 高亮网络 | `` ` `` | 反引号键，不是 `~` |
| 栅格切换 | `N` / `Shift+N` | 下一个/上一个栅格；`Ctrl+G` 是搜索面板 |

## A.3 PCB 编辑器

| 操作 | 快捷键 | 说明 |
| --- | --- | --- |
| 布线 | `X` | Route Single Track |
| 差分对布线 | `6` | Route Differential Pair |
| 过孔 | `V` | 放通过孔并换层 |
| 切换层 | `PgUp` / `PgDn` | 直接切到 F.Cu / B.Cu；`+` / `-` 是上/下一层 |
| 角度吸附模式 | `Shift+Space` | 切换线模式的吸附角度，不是布线推挤模式 |
| 选择工具 | 无默认键 | 按 `Esc` 退出当前工具即回到选择工具 |
| 移动 | `M` | Move |
| 拖动 | `G` | Drag（保持连接） |
| 旋转 | `R` | 旋转封装/对象 |
| 翻转 | `F` | Flip，顶层/底层翻转 |
| 铺铜 | `Ctrl+Shift+Z` | Draw Filled Zones |
| 填充所有铺铜 | `B` | Fill All Zones |
| DRC | 无默认键 | `Inspect → Design Rules Checker` |
| 测量 | `Ctrl+Shift+M` | 两点距离；`Ctrl+M` 不是测量 |
| 3D 视图 | `Alt+3` | View → 3D Viewer |
| 锁定/解锁 | `L` | 切换选中对象锁定 |
| 高亮网络 | `` ` `` | 光标下网络；清除高亮用 `~` |
| 栅格切换 | `N` / `Shift+N` | 下一个/上一个栅格 |

## A.4 符号/封装编辑器

| 操作 | 快捷键 | 说明 |
| --- | --- | --- |
| 新建符号/封装 | `Ctrl+N` | 在现有库中新建 |
| 放置引脚 | `P` | 符号编辑器 Draw Pins |
| 放置焊盘 | 无默认键 | 封装编辑器：工具栏或 `Place → Add Pad` |
| 放置线条 | 无默认键 | 绘图工具栏 |
| 放置矩形 | 无默认键 | 绘图工具栏 |
| 放置圆 | 无默认键 | 绘图工具栏 |
| 放置文本 | 无默认键 | 绘图工具栏；原理图中的 Draw Text 是 `T` |
| 编辑属性 | `E` | 选中对象 |
| 旋转 | `R` | 逆时针 90° |
| 镜像 | `X` / `Y` | 水平/垂直 |
| 引脚表 / 焊盘表 | 无默认键 | 右侧工具栏的表格按钮 |
| 3D 模型预览 | `Alt+3` | 封装编辑器中打开 3D Viewer |

## A.5 选择与拖拽的方向

| 操作 | 行为 |
| --- | --- |
| 从左向右拖框 | 只选中完全在框内的对象 |
| 从右向左拖框 | 选中碰到框的对象 |
| 单击 | 选择光标下最上层对象 |
| `Shift+单击` | 添加/移除选择 |
| `Ctrl+单击` | 选择同一网络/同类对象（部分编辑器） |
| 拖动封装 | 移动封装，保留连接（`G`） |
| 拖动导线 | 改变走向，保持端点（`G`） |

## A.6 常用菜单路径

| 目标 | 路径 |
| --- | --- |
| 工程设置 | `File → Project Settings` |
| 板级设置 | `File → Board Setup` |
| 网类 | `Board Setup → Net Classes` |
| 叠层 | `Board Setup → Physical Stackup` |
| DRC 规则 | `Board Setup → Design Rules` |
| 自定义规则 | `Board Setup → Custom Rules`（打开 `.kicad_dru`） |
| 封装分配 | `Tools → Assign Footprints` |
| 更新 PCB | `Tools → Update PCB from Schematic`（`F8`） |
| 导出 Gerber | `File → Fabrication Outputs → Gerbers` |
| 导出钻孔 | `File → Fabrication Outputs → Drill Files` |
| 导出坐标 | `File → Fabrication Outputs → Component Placement` |
| 导出 BOM | `Tools → Generate BOM` 或 `kicad-cli` |
| 3D 视图 | `View → 3D Viewer` |
| 符号库浏览器 | `Tools → Symbol Library Browser` |
| 封装库浏览器 | `Tools → Footprint Library Browser` |

> **提示：**快捷键冲突时，KiCad 会在 `Preferences → Hotkeys` 里标红。团队可以导出一份 `.hotkeys` 配置共享，但不要强制覆盖个人习惯。

## A.7 官方界面截图

下面 8 张图直接截自 KiCad 10 官方文档，用来和正文手绘图对照。截图按 CC BY 3.0 或 GPLv3+ 使用；逐张来源、访问日期与版本见 `yuyu-book/screenshots/README.md`，书末“来源与许可”也列出了 KiCad 文档条目。

<figure class="illu illu-photo screenshot">
<div class="illu-frame"><img src="../yuyu-book/screenshots/eeschema-dialog-erc.png" alt="ERC 对话框"></div>
<figcaption><span class="fig-no">图 A-1</span><span class="fig-cap">ERC 对话框。左侧按错误类型分组列出违规对象；底部可筛选错误、警告和排除项，或重新运行检查。</span></figcaption>
</figure>

<figure class="illu illu-photo screenshot">
<div class="illu-frame"><img src="../yuyu-book/screenshots/eeschema-erc-severity.png" alt="Schematic Setup 违规严重级别"></div>
<figcaption><span class="fig-no">图 A-2</span><span class="fig-cap">Schematic Setup 的 Violation Severity 页。每类 ERC 检查可单独设为 Error、Warning 或 Ignore。</span></figcaption>
</figure>

<figure class="illu illu-photo screenshot">
<div class="illu-frame"><img src="../yuyu-book/screenshots/pcbnew-board-setup-stackup.png" alt="Board Setup 叠层页"></div>
<figcaption><span class="fig-no">图 A-3</span><span class="fig-cap">Board Setup 的 Physical Stackup 页。层数、材料、厚度和铜厚在这里定义；板厚由叠层参数计算。</span></figcaption>
</figure>

<figure class="illu illu-photo screenshot">
<div class="illu-frame"><img src="../yuyu-book/screenshots/pcbnew-board-setup-constraints.png" alt="Board Setup 约束页"></div>
<figcaption><span class="fig-no">图 A-4</span><span class="fig-cap">Board Setup 的 Constraints 页。板级最小值在这里；网类中的线宽、过孔尺寸是默认值，不等同于 DRC 下限。</span></figcaption>
</figure>

<figure class="illu illu-photo screenshot">
<div class="illu-frame"><img src="../yuyu-book/screenshots/pcbnew-zone-properties.png" alt="铺铜区域属性"></div>
<figcaption><span class="fig-no">图 A-5</span><span class="fig-cap">Copper Zone Properties。网络、间距、焊盘连接方式、热焊盘参数和孤岛移除都在这里设置。</span></figcaption>
</figure>

<figure class="illu illu-photo screenshot">
<div class="illu-frame"><img src="../yuyu-book/screenshots/pcbnew-track-via-properties.png" alt="走线与过孔属性"></div>
<figcaption><span class="fig-no">图 A-6</span><span class="fig-cap">Track &amp; Via Properties。选中走线或过孔后按 E 打开；可改网类、线宽、过孔尺寸和所在层。</span></figcaption>
</figure>

<figure class="illu illu-photo screenshot">
<div class="illu-frame"><img src="../yuyu-book/screenshots/pcbnew-drc-violations.png" alt="DRC 违规列表"></div>
<figcaption><span class="fig-no">图 A-7</span><span class="fig-cap">DRC 的 Violations 页。每条记录给出规则、对象、实测值与要求值；底部可勾选 Exclusions、保存报告或重新运行；排除单条违规要用右键菜单。</span></figcaption>
</figure>

<figure class="illu illu-photo screenshot">
<div class="illu-frame"><img src="../yuyu-book/screenshots/pcbnew-board-setup-violation-severity.png" alt="DRC 严重级别设置"></div>
<figcaption><span class="fig-no">图 A-8</span><span class="fig-cap">Board Setup 的 Violation Severity 页。每类 DRC 违规可单独设为 Error、Warning 或 Ignore，决定是否阻塞发板。</span></figcaption>
</figure>
