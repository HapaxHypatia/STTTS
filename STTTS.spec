# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['STTTS.py'],
             pathex=['C:\\Users\\rebecca.haskmann\\OneDrive - Brisbane Grammar School\\Programming\\STTTS'],
             binaries=[],
             datas=[('ffmpeg.exe', 'ffmpeg.exe')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='STTTS',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
