# -*- mode: python ; coding: utf-8 -*-
# SOFTCURSE FILE READER — PyInstaller Build Spec
# Run: pyinstaller softcurse_reader.spec

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all pywebview data files and hidden imports
datas = [
    ('src/ui.html', '.'),           # HTML UI bundled at root
    ('src/assets/*', 'assets'),     # Assets folder bundled
]
datas += collect_data_files('webview')

hiddenimports = collect_submodules('webview') + [
    'webview',
    'webview.platforms',
    'webview.platforms.winforms',
    'clr',
    'System',
    'System.Windows.Forms',
    'System.Threading',
]

a = Analysis(
    ['src/main.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'PIL', 'tkinter', 'PyQt5', 'PyQt6', 'wx'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SoftcurseFileReader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,          # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    icon='src/assets/file_reader.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SoftcurseFileReader',
)
