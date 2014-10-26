#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- mode: python -*-
import sys
import os
data_files = [
  #('File.py', 'Path-to\File.py', 'DATA'),
]
includes = ['encodings.ascii']
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
      'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
      'Tkconstants', 'Tkinter']
packages = []
dll_excludes = []
dll_includes = []

app = Analysis(['__init__.py'],
       pathex=['.'],
       hiddenimports=[],
       hookspath=None,
       runtime_hooks=None)

pyz = PYZ(app.pure)
exe = EXE(pyz,
      app.scripts + includes - excludes + packages,
      app.binaries - dll_excludes + dll_includes + data_files,
      app.zipfiles,
      app.datas,
      name='./dist/project',
      debug=False,
      strip=None,
      upx=True,
      console=True,
      icon='',
      )
