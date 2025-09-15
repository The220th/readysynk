# -*- mode: python ; coding: utf-8 -*-

# pip3 install --upgrade pip pyinstaller
# pyi-makespec --collect-data=gradio_client --collect-data=gradio --collect-data=safehttpx --collect-data=groovy {NAME}.py
# add to hiddenimports safehttpx and groovy
# add to module_collection_mode gradio (to do it without pyc)
# pyinstaller {NAME}.spec

from PyInstaller.utils.hooks import collect_data_files

datas = []
datas += collect_data_files('gradio_client')
datas += collect_data_files('gradio')
datas += collect_data_files('safehttpx')
datas += collect_data_files('groovy')


a = Analysis(
    ['readysynk.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "safehttpx",
        "groovy",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    module_collection_mode={
        'gradio': 'py',  # Collect gradio package as source .py files
    },
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='readysynk',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    onefile=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='readysynk',
)
