# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['gui\\run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('media/myIcon.png', 'media'),
        ('media/myIcon.ico', 'media'),
        ('scripts/conn.py', 'scripts'),
        ('scripts/functions.py', 'scripts'),
        ('.env', '.'),
    ],
    hiddenimports=['psycopg2'],  # Include the psycopg2 module explicitly
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    [],
    name='library',
    debug=False,
    bootloader_ignore_signals=False,
    bootloader_silent=False,
    bootloader_path=None,
    console=False,
    icon=['media\\myIcon.ico'],
)
