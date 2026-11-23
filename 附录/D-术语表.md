# 附录 D：术语表

> 本表按中文拼音/英文首字母混合排序，给出本书使用的含义。不同厂商/社区可能用不同译法；遇到歧义时，以英文原名和上下文为准。

| 中文 | English | 本书含义 |
| --- | --- | --- |
| 安装孔 | mounting hole | 用于螺丝/支柱固定的孔，通常非镀通 |
| 板框 | board outline / Edge.Cuts | 板子的外轮廓，决定切割形状 |
| 板厚 | board thickness | 成品板的总厚度，常见 1.6 mm |
| 半固化片 | prepreg | 多层板中未完全固化的树脂片，压合后成为介质 |
| 包地 | ground guard / guard trace | 在敏感信号两侧/周围设置接地铜线，并以过孔接到 GND 平面 |
| 表面处理 | surface finish | 焊盘表面的保护层，如 HASL、ENIG |
| 布局 | placement | 决定器件在板上的位置 |
| 布线 | routing | 用铜线连接网络 |
| 参考面 | reference plane | 信号回流所依赖的完整铜面（地/电源） |
| 差分对 | differential pair | 两根一起传输差分信号的线 |
| 层叠 | stackup | 铜箔/介质/芯板的排列与厚度 |
| 插件 | plugin / add-on | 扩展 KiCad 功能的程序 |
| 创建变体 | design variant | 同一设计的不同装配版本 |
| 磁珠 | ferrite bead | 抑制高频噪声的元件 |
| 导通孔 | via | 连接不同层的镀通孔 |
| 地平面 | ground plane | 完整的 GND 铜面 |
| 电迁移 | electromigration | 大电流下金属原子迁移导致的失效 |
| 电气规则检查 | ERC | 检查原理图电气连接/引脚冲突 |
| 叠层 | stackup | 同“层叠” |
| 定位孔 | locating hole | 用于机械装配或定位的孔；不等同于光学基准点 |
| 短支线 | stub | 从主信号路径分出的支线，高速设计中需评估其反射影响 |
| 飞线 | ratsnest | 未布线网络的示意线 |
| 封装 | footprint | 器件在 PCB 上的焊盘图形 |
| 符号 | symbol | 器件在原理图上的图形 |
| 复位 | reset | 让 MCU 回到初始状态 |
| 钢网 | stencil | 印刷锡膏用的金属模板 |
| 过孔 | via | 同“导通孔” |
| 焊盘 | pad | 铜箔上用于焊接的暴露区域 |
| 环宽 | annular ring | 焊盘外径与孔径之间的铜环宽度 |
| 回流焊 | reflow soldering | 以受控温度曲线加热锡膏并形成焊点的工艺 |
| 回流路径 | return path | 信号电流返回源头的路径 |
| 基准点 | fiducial mark | 供贴片机/视觉系统识别板面位置与方向的标记，不是机械孔 |
| 极限值 | absolute maximum rating | 器件不得超出的应力额定值，不是正常工作目标 |
| 寄生参数 | parasitics | 走线/过孔/器件非理想的电阻/电感/电容 |
| 间距 | clearance | 两个铜对象之间的最小距离 |
| 结点 | junction | 原理图中导线相交并连接的实心点 |
| 金属化孔 | plated through hole | 孔壁镀铜的孔 |
| 禁止区 | keepout | 不允许放置铜/器件/过孔的区域 |
| 开窗 | solder mask opening | 阻焊层上露出铜的区域 |
| 空心孔 | non-plated through hole | 不镀铜的孔 |
| 库 | library | 符号/封装/3D 模型的集合 |
| 跨分割 | split plane | 参考面被切开，回流被迫绕路 |
| 连接器 | connector | 板与外部线缆/设备的接口 |
| 埋孔 | buried via | 只连接内层、不到表面的孔 |
| 盲孔 | blind via | 从表面到内层、不到另一面的孔 |
| 平面 | plane | 大面积连续铜层或铜区域，常用作地/电源参考 |
| 内层 | inner layer | 多层板中间的铜层 |
| 拼板 | panelization | 把多块小板拼成一张生产板 |
| 屏蔽 | shielding | 用铜/金属隔离电磁场 |
| 铺铜 | copper pour / zone | 大面积填充铜 |
| 热焊盘 | thermal relief | 焊盘与铺铜之间留缺口、用细桥连接 |
| 散热焊盘 | thermal pad | 器件底部用于散热/接地的焊盘 |
| 丝印 | silkscreen | 板上的文字/图形标记 |
| 四层板 | 4-layer board | 含两个内层的 PCB |
| 铜厚 | copper weight | 铜箔厚度，常用 oz 表示 |
| 网表 | netlist | 网络与器件的连接表 |
| 网类 | net class | 一组网络的布线约束 |
| 网络 | net | 电气上相连的一组引脚及其连接关系 |
| 位号 | reference designator | R1/C1/U1 等器件编号 |
| 锡膏 | solder paste | 回流焊用的锡粉+助焊剂 |
| 线宽 | track width | 铜线宽度 |
| 阻抗 | impedance | 交流信号看到的电阻/电感/电容综合 |
| 阻焊 | solder mask | 覆盖铜面、防止焊接短路的涂层 |
| 走线 | track | PCB 上的铜线 |
| 组件 | component | 板上的器件 |
| 组装 | assembly | 把器件焊到板上 |
| 坐标文件 | pick-and-place / CPL | 贴片机用的位号/坐标/旋转 |
| 3D 模型 | 3D model | 器件/板的三维形状，常用 STEP |
| ATE | automated test equipment | 自动测试设备 |
| BOM | bill of materials | 物料清单 |
| CPL | component placement list | 贴片坐标文件 |
| DRC | design rule check | 设计规则检查 |
| DFM | design for manufacturability | 可制造性设计 |
| EMC | electromagnetic compatibility | 电磁兼容 |
| EMI | electromagnetic interference | 电磁干扰 |
| ERC | electrical rules check | 电气规则检查 |
| ESR | equivalent series resistance | 等效串联电阻 |
| F.Cu | front copper | 顶层铜 |
| B.Cu | back copper | 底层铜 |
| F.Mask | front solder mask | 顶层阻焊 |
| F.Paste | front paste | 顶层钢网 |
| F.SilkS | front silkscreen | 顶层丝印 |
| F.Fab | front fabrication | 顶层装配图 |
| GND | ground | 地 |
| HASL | hot air solder leveling | 喷锡表面处理 |
| ENIG | electroless nickel immersion gold | 沉金表面处理 |
| IPC | Institute for Printed Circuits | 印制电路行业标准组织 |
| IPC-2221 | generic standard on printed board design | 印制板设计通用标准 |
| IPC-7351 | land pattern standard | 焊盘图形标准 |
| IPC-2581 | open PCB assembly data format | 开放制造数据格式 |
| KLC | KiCad Library Convention | KiCad 库规范 |
| LDO | low dropout regulator | 低压差线性稳压器 |
| MCU | microcontroller unit | 微控制器 |
| ODB++ | open database format | 制造数据格式 |
| PCB | printed circuit board | 印制电路板 |
| PCM | Plugin and Content Manager | KiCad 插件/内容管理器 |
| QFN | quad flat no-lead | 方形扁平无引脚封装 |
| SOIC | small outline integrated circuit | 小外形集成电路封装 |
| SPI | serial peripheral interface | 串行外设接口 |
| STEP | standard for the exchange of product data | 三维模型交换格式 |
| TVS | transient voltage suppressor | 瞬态电压抑制器 |
| USB-C | USB Type-C | 可正反插的 USB 接口 |
| V-Cut | V-shaped scoring | 拼板时在板边切 V 形槽 |
| via stitching | stitching via | 缝合过孔，连接地平面 |
| 邮票孔 | castellated hole | 拼板/模块边缘的半孔 |
