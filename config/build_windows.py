#!/usr/bin/python
# -*- coding: utf-8 -*-
import py2exe
import sys, os
from distutils.core import setup

#from glob import glob
#data_files = [("Microsoft.VC90.CRT", glob(r'C:\Program Files\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))]

dll_excludes = []
data_files = []
__preselected_dlls = [ "QtCore4.dll", "QtDesigner4.dll", "QtGui4.dll", "QtNetwork4.dll", "QtSql4.dll", "QtWebKit4.dll", ]
import os, site
for site in site.getsitepackages():
	pyside_path = os.path.join(site, "PySide")
	if not os.path.exists(pyside_path): continue
	dll_excludes.extend( f for f in os.listdir(pyside_path) if f.endswith(".dll") and f.startswith("Qt") )
	#data_files.extend( (os.path.basename(f), [os.path.join(pyside_path, f)]) for f in os.listdir(pyside_path) if f.endswith(".dll") and f.startswith("Qt") )
	data_files.extend( (".", [os.path.join(pyside_path, f)]) for f in os.listdir(pyside_path) if f.endswith(".dll") and f.startswith("Qt") and ( True if not __preselected_dlls else (f in __preselected_dlls) ) )
	break

if len(sys.argv) == 1:
	sys.argv.append("py2exe")

def gosetup(embebbed = True, ultracompress = False):
	if ultracompress:
		bundle_files = 1
		dist_dir = r"dist/ultracompress"
		zipfile = None
	elif embebbed:
		bundle_files = 2
		dist_dir = r"dist/embedded"
		zipfile = None
	else:
		bundle_files = 3
		dist_dir = r"dist/normal"
		zipfile = "base"
	if not os.path.exists(dist_dir): os.mkdir(dist_dir)
	setup(
		name="Call Control",
		version="2.1",
		description="Call Control | System",
		author="Marco Antonio Pinto",
		author_email="pinto.marco@live.com",
		url="http://.sourceforge.net",
		license="MIT",
		package_data = {},
		data_files=data_files,
		options={"py2exe": {
			#"compressed": 2,
			"optimize": 2,
			"bundle_files": bundle_files,
			"dll_excludes": dll_excludes,
			"dist_dir": dist_dir,
			'includes': #INCLUDES,
			[
				
			], 'excludes': [
				"pywin",
				"pywin.debugger",
				"pywin.debugger.dbgcon",
				"pywin.dialogs",
				"pywin.dialogs.list",
				"Tkconstants",
				"Tkinter",
				"tcl"
			]
		   }
		},
		dest_base = './dist/project',
		zipfile=zipfile,
windows = [
			{
				"script": "{{__init__.py}}",
				"icon_resources": [(1, r"")]
			}
		],
	)


#Generate an embebbed version
#gosetup(embebbed = True)

#Generate an single version
#gosetup(embebbed = False)

#Generate an single version
gosetup(ultracompress = True)


