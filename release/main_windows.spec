# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['..\\program\\main.py'],
    pathex=['program'],
    binaries=[],
    datas=[
        # ('../data/conditionDb.csv', 'data'),  # Excluded for prod build
        # ('../data/db.csv', 'data'),   # Excluded for prod build
        # ('../data/treatmentDb.csv', 'data'),  # Excluded for prod build
        # ('../data/treatmentRevisionHistory.csv', 'data'), # Excluded for prod build
        # ('../data/attachment', 'data/attachment'),    # Excluded for prod build
        ('../program/asset/icons', 'program/asset/icons'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PatientCarePatientGood',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PatientCarePatientGood',
)
