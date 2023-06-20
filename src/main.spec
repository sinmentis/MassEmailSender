# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries = [],

    # If missing libpyside6.abi3.so.6.5 and libpyside6qml.abi3.so.6.5 - add those in with result from sudo find / -name "libpyside*"
    datas=[
        ("./Frisbee/modules/", "./Frisbee/modules/"),               # Hidden import python file
        ("./EmailAll/modules/", "./EmailAll/modules/"),             # Hidden import python file

        ("./fake_useragent_data/", "./fake_useragent_data/"),       # Hidden import for fake_useragent

        ("./gui/", "./gui/"),                                       # Dynamic load QML for UI
        ("./config_json", "./config_json")                          # Dynamic load QML for UI
    ],

    hiddenimports=[
        "bs4", "urllib3", "requests_futures.sessions",                          # Required in Frisbee/modules/bing.py and Frisbee/modules/based.py
        "EmailAll.common.search", "EmailAll.common.utils", "fake-useragent"     # Required in EmailAll/modules/
    ],

    hookspath=[],
    hooksconfig={},
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
    name='main',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
