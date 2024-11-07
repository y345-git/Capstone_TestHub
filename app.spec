# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('institute_info.env', '.'), ('.env', '.'), ('home.py', '.'), ('modules.json', '.'), ('Absent_Copy_Case_Nos', 'Absent_Copy_Case_Nos'), ('System_Parameters', 'System_Parameters'), ('Exam_Block_Details', 'Exam_Block_Details'), ('Exam_Examinee_Details', 'Exam_Examinee_Details'), ('Reports', 'Reports'), ('System_Tools', 'System_Tools'), ('config', 'config'), ('essentials', 'essentials'), ('Exit', 'Exit')],
    hiddenimports=['dotenv', 'tkcalendar', 'customtkinter', 'mysql.connector', 'os', 'sys', 'datetime', 'pathlib', 'collections', 'json', 're', 'time', 'threading', 'functools', 'configparser'],
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
    a.binaries,
    a.datas,
    [],
    name='app',
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
