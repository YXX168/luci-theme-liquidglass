# Liquid Glass for LuCI

独立的液态玻璃主题包，基于 Argon 2.4.3 的兼容样式和菜单，保留原作者版权。

## 适配范围

- 本次目标：Link NN6000 v2，ImmortalWRT SNAPSHOT r0-24fc52e，内核 6.12.68。
- LuCI：26.028.32477~ec83425，ucode 模板；包管理器：opkg。
- 安装包为 `all.ipk`，不含机器码。其他现代 ucode LuCI 可尝试，但未实机验证。
- 不适用于仅支持 Lua 模板的旧版 LuCI。使用 apk 包管理器的固件应从源码通过对应 SDK 构建，不能直接安装本 IPK。

## 安装及切换

1. 在 LuCI「系统 → 软件包」上传并安装 `luci-theme-liquidglass_1.0.0-1_all.ipk`。
2. 在「系统 → 系统 → 语言和界面」选择 `LiquidGlass`，保存并应用。
3. 刷新页面。右上角「◐」在跟随系统、浅色、深色之间循环。

也可将安装包放到路由器 `/tmp` 后运行：

```sh
opkg install /tmp/luci-theme-liquidglass_1.0.0-1_all.ipk
uci set luci.main.mediaurlbase='/luci-static/liquidglass'
uci commit luci
```

安装只注册主题，不自动切换，不需要重刷固件或重启网络服务。主题自己的目录与 Argon 分开，没有替换 Argon 文件。
明暗偏好保存在当前浏览器的本地存储，不修改路由器配置；清除浏览器站点数据后恢复跟随系统。
主题不会收集密码，不改变 LuCI 登录表单目标、权限、网络设置或功能视图。

## 切回及卸载

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
