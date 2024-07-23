# login_screen.spec
# -*- mode: python ; coding: utf-8 -*-

import os
import pyppeteer_stealth

block_cipher = None

# Path to the pyppeteer_stealth JavaScript files
pyppeteer_stealth_js_path = os.path.join(os.path.dirname(pyppeteer_stealth.__file__), 'js')

a = Analysis(
    ['login_screen.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        
        (pyppeteer_stealth_js_path, 'pyppeteer_stealth/js'),
    ],
    hiddenimports=['PyQt5', 'screeninfo', 'pyppeteer', 'pandas', 'pyppeteer_stealth'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
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
    name='login_screen',
    debug=True,  # Enable debug mode
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon='ABClogomark-1-white.ico',  # Path to your icon file
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='login_screen',
)
