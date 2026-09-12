#!/bin/sh
# Register an independent theme. Installation never changes the active theme.
set -eu
[ -z "${IPKG_INSTROOT:-}" ] || exit 0
[ -f /usr/share/ucode/luci/template/themes/liquidglass/header.ut ] || exit 1
uci -q get luci.themes >/dev/null || uci set luci.themes=internal
uci set luci.themes.LiquidGlass='/luci-static/liquidglass'
uci commit luci
exit 0
