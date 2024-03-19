# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['jogo_lobo.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\dev\\python\\_Projetos\\Pygame1\\graphics', 'graphics'), ('C:\\dev\\python\\_Projetos\\Pygame1\\audio', 'audio'), ('C:\\dev\\python\\_Projetos\\Pygame1\\font', 'font')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='jogo_lobo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
