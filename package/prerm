#!/bin/sh
# Restore an installed fallback before removing files used by the current UI.
set -eu
[ -z "${IPKG_INSTROOT:-}" ] || exit 0
[ "${1:-remove}" != 'upgrade' ] || exit 0
if [ "$(uci -q get luci.main.mediaurlbase || true)" = '/luci-static/liquidglass' ]; then
    fallback=''
    for candidate in argon bootstrap material openwrt-2020; do
        if [ -f "/usr/share/ucode/luci/template/themes/$candidate/header.ut" ] || [ -f "/usr/lib/lua/luci/view/themes/$candidate/header.htm" ]; then
            fallback="$candidate"
            break
        fi
    done
    [ -n "$fallback" ] || { echo 'Install and select another LuCI theme before removing Liquid Glass.' >&2; exit 1; }
    uci set "luci.main.mediaurlbase=/luci-static/$fallback"
fi
uci -q delete luci.themes.LiquidGlass || true
uci commit luci
exit 0
