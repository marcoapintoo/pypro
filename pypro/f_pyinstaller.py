#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import unicode_literals
#from __future__ import print_function
#from __future__ import absolute_import
__author__ = 'marco'
import os
import sys
import json
import utils
from files import *

class LinuxBuildFile(ProjectFile):
  DefaultName = "build_linux.py"
  def __init__(self, config, name=None, parent=None):
    name = name or self.DefaultName
    ProjectFile.__init__(self, name, parent=None)
    self.content = self.common_content(config)

  @staticmethod
  def common_content(config):
    return r"""#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
os.system("pyinstaller {spec}")
""".format(spec=PyInstallerConfigFile.DefaultName)

class PyInstallerConfigFile(ProjectFile):
  DefaultName = "application.spec"
  def __init__(self, config, name=None, parent=None):
    name = name or self.DefaultName
    ProjectFile.__init__(self, name, parent=None)
    self.content = self.common_content(config)

  @staticmethod
  def common_content(config):
    return r"""#!/usr/bin/python
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
      name='./dist/{{DistributionName}}',
      debug=False,
      strip=None,
      upx=True,
      console=True,
      icon='{{IconPath}}',
      )
""".replace(
      "{{DistributionName}}", config["executable"]["name"]
    ).replace(
      "{{IconPath}}", config["executable"]["icon"]
    )
