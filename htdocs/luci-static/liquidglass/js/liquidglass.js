/* Liquid Glass for LuCI, 2026. SPDX-License-Identifier: Apache-2.0 */
(function () {
    'use strict';
    var key = 'luci-liquidglass-appearance';
    var root = document.documentElement;
    var system = window.matchMedia('(prefers-color-scheme: dark)');
    var modes = ['auto', 'light', 'dark'];
    var mode = 'auto';
    var zh = /^zh/i.test(root.lang);
    var labels = zh ? ['跟随系统', '浅色', '深色'] : ['System', 'Light', 'Dark'];
    try {
        var saved = localStorage.getItem(key);
        if (modes.indexOf(saved) >= 0) mode = saved;
    } catch (_) { /* Private browsing: keep this page usable. */ }
    function apply() {
        var dark = mode === 'dark' || (mode === 'auto' && system.matches);
        root.setAttribute('data-lg-theme', dark ? 'dark' : 'light');
        root.style.colorScheme = dark ? 'dark' : 'light';
        var css = document.getElementById('lg-dark-css');
        if (css) css.media = dark ? 'all' : 'not all';
        var meta = document.querySelector('meta[name="theme-color"]');
        if (meta) meta.content = dark ? '#101e35' : '#dceaff';
        document.querySelectorAll('[data-lg-appearance]').forEach(function (button) {
            var current = modes.indexOf(mode);
            button.textContent = '◐ ' + labels[current];
            button.title = (zh ? '切换为' : 'Switch to ') + labels[(current + 1) % 3];
            button.setAttribute('aria-label', (zh ? '外观：' : 'Appearance: ') + labels[current] + '. ' + button.title);
        });
    }
    apply();
    if (system.addEventListener) system.addEventListener('change', apply);
    else if (system.addListener) system.addListener(apply);
    window.addEventListener('storage', function (event) {
        if (event.key !== key) return;
        mode = modes.indexOf(event.newValue) >= 0 ? event.newValue : 'auto';
        apply();
    });
    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('[data-lg-appearance]').forEach(function (button) {
            button.addEventListener('click', function () {
                mode = modes[(modes.indexOf(mode) + 1) % 3];
                try { localStorage.setItem(key, mode); } catch (_) { }
                apply();
            });
        });
        var menu = document.querySelector('.showSide');
        if (menu) menu.addEventListener('keydown', function (event) {
            if (event.key === ' ') { event.preventDefault(); menu.click(); }
        });
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' && menu && menu.classList.contains('active')) menu.click();
        });
        apply();
    });
})();
