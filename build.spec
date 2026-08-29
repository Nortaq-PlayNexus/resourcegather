# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for Resource Gather -> ResourceGather.exe.

Build:  pyinstaller build.spec
Output: dist/ResourceGather/ResourceGather.exe  (or use --onefile)

Read-only assets (config/, data/) bundle via `datas` and resolve at runtime
through core.config_loader (sys._MEIPASS when frozen). Writable output
(findings.csv, snapshots/) is written next to the executable. Generated source
functions in core.sources are built at runtime, so no extra bundling needed.
"""
import os

block_cipher = None
ROOT = os.path.dirname(os.path.abspath(SPEC))

datas = [
    (os.path.join(ROOT, "config"), "config"),
    (os.path.join(ROOT, "data"), "data"),
]

hiddenimports = [
    "core", "core.config_loader", "core.tor_client", "core.utils",
    "core.validation", "core.opsec", "core.ethics", "core.parsers",
    "core.storage", "core.analytics", "core.scheduler", "core.sources",
    "core.search", "core.report",
    "bs4", "requests", "requests.socks",
]

a = Analysis(
    [os.path.join(ROOT, "main.py")],
    pathex=[ROOT],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name="ResourceGather",
    debug=False,
    console=True,
)

coll = COLLECT(
    exe, a.binaries, a.zipfiles, a.datas,
    name="ResourceGather",
)
