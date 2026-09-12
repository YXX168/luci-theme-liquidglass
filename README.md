# Liquid Glass for LuCI

独立的液态玻璃主题包，基于 Argon 2.4.3 的兼容样式和菜单，保留原作者版权。

## 项目概述与特性

- **受 macOS 26 Liquid Glass 启发的通透材质**：5 层材质分级（微透导航侧栏、玻璃浮岛工具条、高对比卡片表格、居中模态弹窗、实白表单控件），兼顾视觉通透感与配置信息的高频扫描可读性。
- **双色环境光氛围**：左上暖杏光（#FFD29D）+ 右上冷蓝光（#A0CFFF），中央区域白净通透。
- **即时明暗切换**：右上角一键在「跟随系统、浅色、深色」之间循环切换，暗色模式为深邃冷色烟蓝玻璃。
- **独立安装与安全回退**：资源与规则独立于 `/luci-static/liquidglass`，不污染原有 Argon/Bootstrap 文件，支持随时无损切回与卸载。

## 兼容性与运行环境

- **支持固件**：
  - 官方 OpenWrt 22.03、23.05、24.x 及 Master/快照版
  - 主流 ImmortalWrt 21.02+、23.05 及各分支 SNAPSHOT
- **硬件架构**：全架构通用（纯前端样式与 ucode 模板，标记为 `all.ipk`，ARM / x86 / MIPS 均适用）。
- **不支持版本**：OpenWrt 19.07 / 18.06 等仅支持旧版 Lua (`.htm`) 模板的系统。

## 安装及切换

### 方式一：终端一键安装（推荐）

```sh
# 下载最新 Release 安装包并安装
wget -O /tmp/luci-theme-liquidglass_all.ipk https://github.com/YXX168/luci-theme-liquidglass/releases/latest/download/luci-theme-liquidglass_1.0.0-1_all.ipk
opkg install /tmp/luci-theme-liquidglass_all.ipk

# 切换为默认主题
uci set luci.main.mediaurlbase='/luci-static/liquidglass'
uci commit luci
```

### 方式二：Web 界面上传安装

1. 从 [Releases](https://github.com/YXX168/luci-theme-liquidglass/releases) 下载 `luci-theme-liquidglass_1.0.0-1_all.ipk`。
2. 登录路由器后台，进入「系统」→「软件包」→「上传软件包」并安装。
3. 进入「系统」→「系统」→「语言和界面」，主题选择 `LiquidGlass`，保存并应用即可。

界面正常时，在同一位置选择 Argon。SSH 回退命令：

```sh
uci set luci.main.mediaurlbase='/luci-static/argon'
uci commit luci
```

刷新浏览器。需要卸载时运行 `opkg remove luci-theme-liquidglass`。
卸载脚本会先检查已安装的备用主题；当前正在使用 Liquid Glass 且没有备用主题时会拒绝删除，避免后台失去模板。

## 设计与兼容性

半透明材质、静态柔和背景、边缘高光、圆角侧栏、分段标签和本地登录页；保留原有菜单、表单及插件功能。
支持浅色、深色、跟随系统、减少动画以及不支持背景模糊时的不透明回退。
第三方插件可能自带固定颜色、独立网页或复杂表格，应逐项实机检查；不能承诺覆盖所有插件。
微信参考文章在当前工具中被站点安全策略阻止读取，因此本版不声称复刻该文章，待用户提供效果图后继续调整。

## 从源码构建

在源码目录运行 `python scripts/build_ipk.py`，无需编译路由器固件或安装交叉工具链。
也提供 OpenWrt 软件包 Makefile，放入相应源码树的 `package/luci-theme-liquidglass` 后按 SDK 流程构建。
本次交付由 Python 构建器生成；Makefile 供后续源码集成，未经 SDK 构建验证。

`dist/SHA256SUMS.txt` 提供安装包和源码包校验值，`package-manifest.json` 列出安装文件及哈希。
当前验证记录见交付文件 `VALIDATION.md`。
