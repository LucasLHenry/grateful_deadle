# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\lucas\\Documents\\Projects\\Code\\Contract Work\\Grateful Deadle for Brian\\work\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\lucas\\Documents\\Projects\\Code\\Contract Work\\Grateful Deadle for Brian\\work\\lib\\database\\constraints.json', './lib/database/'), ('C:\\Users\\lucas\\Documents\\Projects\\Code\\Contract Work\\Grateful Deadle for Brian\\work\\lib\\database\\db.json', './lib/database/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
