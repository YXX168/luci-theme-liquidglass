# 自动验证范围

运行 `python3 -m unittest discover -s tests -v`，在临时目录构建安装包并检查：

- IPK 外层、control 和 data 归档结构，以及全架构元数据。
- 安装文件清单、哈希、权限、路径安全和 Argon 路径隔离。
- 安装、卸载脚本均有执行权限。
- 改变源码时间戳后，IPK、源码 ZIP、清单与校验文件保持一致。

GitHub Actions 在 Linux 和 macOS 上运行同一组检查，并检查所有安装脚本的 shell 语法。

这些检查不会连接或修改路由器。LuCI 页面效果、实际安装/卸载回退、固件兼容性和 OpenWrt SDK 构建仍需要对应设备或 SDK 验收。
