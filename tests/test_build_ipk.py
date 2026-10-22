"""Inspect the generated package without installing it on a router."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import tarfile
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_ipk', ROOT / 'scripts/build_ipk.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name) / 'source'
        shutil.copytree(ROOT, self.base, ignore=shutil.ignore_patterns('.git', 'dist', '__pycache__'))
        builder.BASE = self.base
        builder.DIST = self.base / 'dist'
        with contextlib.redirect_stdout(io.StringIO()):
            builder.build()

    def test_package_manifest_hashes_modes_and_maintainer_scripts(self):
        dist = builder.DIST
        ipk = next(dist.glob('*.ipk'))
        with tarfile.open(ipk, 'r:gz') as outer:
            self.assertEqual(outer.extractfile('./debian-binary').read(), b'2.0\n')
            payload = outer.extractfile('./data.tar.gz').read()
            control = outer.extractfile('./control.tar.gz').read()
        manifest = json.loads((dist / 'package-manifest.json').read_text())
        with tarfile.open(fileobj=io.BytesIO(payload), mode='r:gz') as data:
            files = {m.name.removeprefix('./'): m for m in data if m.isfile()}
            self.assertEqual(set(files), set(manifest))
            for name, member in files.items():
                self.assertNotIn('..', Path(name).parts)
                self.assertFalse(name.startswith('/'))
                self.assertNotIn('/themes/argon/', name)
                self.assertNotIn('/luci-static/argon/', name)
                content = data.extractfile(member).read()
                self.assertEqual(hashlib.sha256(content).hexdigest(), manifest[name]['sha256'])
                self.assertEqual(len(content), manifest[name]['bytes'])
                self.assertEqual(oct(member.mode), manifest[name]['mode'])
            for name in ('register.sh', 'unregister.sh'):
                self.assertEqual(files[f'usr/libexec/liquidglass/{name}'].mode, 0o755)
        with tarfile.open(fileobj=io.BytesIO(control), mode='r:gz') as scripts:
            for name in ('postinst', 'prerm'):
                self.assertEqual(scripts.getmember('./' + name).mode, 0o755)
            self.assertIn(b'Architecture: all', scripts.extractfile('./control').read())

    def test_source_zip_and_ipk_ignore_checkout_mtimes(self):
        before = {p.name: p.read_bytes() for p in builder.DIST.iterdir()}
        for file in self.base.rglob('*'):
            if file.is_file() and builder.DIST not in file.parents:
                os.utime(file, (builder.EPOCH + 99999, builder.EPOCH + 99999))
        with contextlib.redirect_stdout(io.StringIO()):
            builder.build()
        self.assertEqual(before, {p.name: p.read_bytes() for p in builder.DIST.iterdir()})
        with zipfile.ZipFile(next(builder.DIST.glob('*.zip'))) as source:
            self.assertIn(builder.NAME + '/tests/test_build_ipk.py', source.namelist())
        for line in (builder.DIST / 'SHA256SUMS.txt').read_text().splitlines():
            checksum, name = line.split('  ')
            self.assertEqual(checksum, hashlib.sha256((builder.DIST / name).read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()
