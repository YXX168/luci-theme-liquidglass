"""Reproducible, pure-Python build for an architecture-independent LuCI IPK."""
from pathlib import Path
import gzip
import hashlib
import io
import json
import tarfile
import zipfile

BASE = Path(__file__).resolve().parents[1]
DIST = BASE / 'dist'
NAME = 'luci-theme-liquidglass'
VERSION = '1.0.0-1'
EPOCH = 1789171200


def archive(items):
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode='w', format=tarfile.USTAR_FORMAT) as tar:
        directories = sorted({str(parent).replace('\\', '/') for path, _, _ in items for parent in Path(path).parents if str(parent) != '.'})
        for path in directories:
            member = tarfile.TarInfo('./' + path + '/')
            member.type = tarfile.DIRTYPE
            member.mode = 0o755
            member.mtime = EPOCH
            member.uname = member.gname = 'root'
            tar.addfile(member)
        for path, data, mode in sorted(items):
            member = tarfile.TarInfo('./' + path)
            member.size = len(data)
            member.mode = mode
            member.mtime = EPOCH
            member.uid = member.gid = 0
            member.uname = member.gname = 'root'
            tar.addfile(member, io.BytesIO(data))
    return gzip.compress(raw.getvalue(), mtime=EPOCH)


def build():
    DIST.mkdir(exist_ok=True)
    data = []
    maps = [('htdocs', 'www'), ('ucode', 'usr/share/ucode/luci'), ('root', '')]
    for source, target in maps:
        for file in sorted((BASE / source).rglob('*')):
            if not file.is_file():
                continue
            path = '/'.join(filter(None, [target, file.relative_to(BASE / source).as_posix()]))
            mode = 0o755 if path.startswith(('etc/uci-defaults/', 'usr/libexec/')) else 0o644
            data.append((path, file.read_bytes(), mode))
    for name in ['LICENSE', 'NOTICE']:
        data.append((f'usr/share/doc/{NAME}/{name}', (BASE / name).read_bytes(), 0o644))
    assert len({p for p, _, _ in data}) == len(data)
    assert all(not p.startswith('/') and '..' not in p.split('/') for p, _, _ in data)
    assert not any('/themes/argon/' in p or '/luci-static/argon/' in p for p, _, _ in data)
    control = f'''Package: {NAME}
Version: {VERSION}
Architecture: all
Maintainer: Liquid Glass theme project
Section: luci
Priority: optional
Depends: luci-base
License: Apache-2.0
Installed-Size: {sum(len(b) for _, b, _ in data)}
Description: Standalone Liquid Glass theme for modern ucode-based LuCI
 Based on Argon 2.4.3. Local assets, light/dark appearance, responsive login.
 Installation registers the theme without changing the active theme.
'''.encode()
    controls = [('control', control, 0o644)]
    for name in ['postinst', 'prerm']:
        controls.append((name, (BASE / 'package' / name).read_bytes().replace(b'\r\n', b'\n'), 0o755))
    members = [('debian-binary', b'2.0\n'), ('control.tar.gz', archive(controls)), ('data.tar.gz', archive(data))]
    # OpenWrt's ipkg-build uses a gzip-compressed tar container, not Debian ar.
    result = archive([(name, payload, 0o644) for name, payload in members])
    output = DIST / f'{NAME}_{VERSION}_all.ipk'
    output.write_bytes(result)
    manifest = {p: {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(), 'mode': oct(m)} for p, b, m in data}
    (DIST / 'package-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    source = DIST / f'{NAME}-1.0.0-source.zip'
    includes = ['htdocs', 'ucode', 'root', 'package']
    files = [p for folder in includes for p in (BASE / folder).rglob('*') if p.is_file()]
    files += [BASE / p for p in ['LICENSE', 'NOTICE', 'Makefile', 'README.md', 'scripts/build_ipk.py']]
    with zipfile.ZipFile(source, 'w', zipfile.ZIP_DEFLATED) as z:
        for file in sorted(files):
            z.write(file, NAME + '/' + file.relative_to(BASE).as_posix())
    hashes = '\n'.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}' for p in [output, source]) + '\n'
    (DIST / 'SHA256SUMS.txt').write_text(hashes, encoding='ascii')
    print(output)
    print(f'{len(data)} files; {len(result)} bytes; no Argon path collisions')
    print(hashes)


if __name__ == '__main__':
    build()
