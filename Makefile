include $(TOPDIR)/rules.mk

PKG_NAME:=luci-theme-liquidglass
PKG_VERSION:=1.0.0
PKG_RELEASE:=1
PKG_LICENSE:=Apache-2.0
PKGARCH:=all

include $(INCLUDE_DIR)/package.mk

define Package/luci-theme-liquidglass
  SECTION:=luci
  CATEGORY:=LuCI
  SUBMENU:=4. Themes
  TITLE:=Liquid Glass theme for modern LuCI
  DEPENDS:=+luci-base
  PKGARCH:=all
endef

define Package/luci-theme-liquidglass/description
  A standalone glass theme based on Argon 2.4.3, with local light/dark
  appearance controls, accessible login and responsive layout.
  Requires modern LuCI with ucode templates.
endef

define Build/Compile
endef

define Package/luci-theme-liquidglass/install
	$(INSTALL_DIR) $(1)/www $(1)/usr/share/ucode/luci/template/themes $(1)/usr/share/doc/luci-theme-liquidglass
	$(CP) ./htdocs/* $(1)/www/
	$(CP) ./ucode/template/themes/liquidglass $(1)/usr/share/ucode/luci/template/themes/
	$(CP) ./root/* $(1)/
	$(CP) ./LICENSE ./NOTICE $(1)/usr/share/doc/luci-theme-liquidglass/
	chmod 755 $(1)/etc/uci-defaults/30-luci-theme-liquidglass $(1)/usr/libexec/liquidglass/register.sh
endef

define Package/luci-theme-liquidglass/postinst
#!/bin/sh
[ -n "$${IPKG_INSTROOT}" ] || /usr/libexec/liquidglass/register.sh
endef

define Package/luci-theme-liquidglass/prerm
#!/bin/sh
[ -n "$${IPKG_INSTROOT}" ] || /usr/libexec/liquidglass/unregister.sh "$$@"
endef

$(eval $(call BuildPackage,luci-theme-liquidglass))
