# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['separator.py'],
    pathex=[],
    binaries=[],
    datas=[('/usr/local/lib/python3.11/site-packages/demucs', 'demucs/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'nvidia.cuda_nvrtc',
        'nvidia.cuda_runtime',
        'nvidia.cuda_cupti',
        'nvidia.cudnn',
        'nvidia.cublas',
        'nvidia.cufft',
        'nvidia.curand',
        'nvidia.cusolver',
        'nvidia.cusparse',
        'nvidia.nccl',
        'nvidia.nvtx',
        'cuda_nvrtc',
        'cusolver'
    ],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='separator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
