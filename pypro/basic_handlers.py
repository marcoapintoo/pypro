#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
#from __future__ import absolute_import
__author__ = 'marco'
import os
import sys
import json
from codecs import open
import datetime
from files import *
from f_license import LicenseFile
from f_py2exe import WinBuildFile
from f_pyinstaller import LinuxBuildFile, PyInstallerConfigFile
from f_script import AppInitFile, PackageInitFile

class BasicHandler(object):
    def read_config(self):
        config = "{}"
        app_json = "application.json"
        if not os.path.exists(app_json):
            app_json = "config/" + app_json
        with open(app_json, "r") as f:
            config = "".join(f.readlines())
        return json.loads(config)


class BasicConfigHandler(BasicHandler):
    def __init__(self):
        BasicHandler.__init__(self)

    def read_input(self):
        config = {
            "application": {},
            "executable": {},
        }
        print("About your project...")
        config["application"]["name"] = raw_input("Project name:")
        config["application"]["author"] = raw_input("Author:")
        config["application"]["description"] = raw_input("Description:")
        config["application"]["creation"] = raw_input("Creation date:")
        print("About your program executable...")
        config["executable"]["name"] = raw_input("Executable name:")
        config["executable"]["icon"] = raw_input("Executable icon path:")
        print("About Qt environment...")
        config["executable"]["qt_toolkit"] = raw_input("Qt toolkit[PyQt4/PyQt5/PySide]:")
        config["executable"]["qt_toolkit"] = config["executable"]["qt_toolkit"].lower()
        if config["executable"]["qt_toolkit"] not in ("pyqt4","pyqt5","pyside"):
            config["executable"]["qt_toolkit"] = "pyqt4"
        return config

    def dump_to_file(self,):
        basepath = "config"
        if not os.path.exists(basepath):
            os.makedirs(basepath)
        filename = os.path.join(basepath, "application.json")
        #filename = "application.json"
        config = self.read_input()
        config["application"]["creation"] = str(config["application"]["creation"])
        content = json.dumps(config, indent=4)
        with open(filename, "w", encoding="utf8") as f:
            f.write(content)

class BasicUnfinishedHandler(object):
    def __init__(self, feature_name):
        self.feature_name = feature_name

    def show(self):
        print("Sorry. Feature: '{0}' is unfinished yet.".format(self.feature_name))

class SkeletonHandler(BasicHandler):
    def __init__(self):
        BasicHandler.__init__(self)

    def create_structure(self):
        config = self.read_config()

        root = ProjectDirectory(".")
        root.add_file(AppInitFile(config))
        root.add_file(LicenseFile(config))

        config_folder = ProjectDirectory("config")
        root.add_folder(config_folder)

        config_folder.add_file(WinBuildFile(config))
        config_folder.add_file(LinuxBuildFile(config))
        config_folder.add_file(PyInstallerConfigFile(config))

        build_dir = ProjectDirectory("build")
        root.add_folder(build_dir)

        proj_dir = ProjectDirectory(config["application"]["name"])
        root.add_folder(proj_dir)

        proj_init = PackageInitFile(config)
        proj_dir.add_file(proj_init)

        dist_dir = ProjectDirectory("dist")
        root.add_folder(dist_dir)

        lib_dir = ProjectDirectory("lib")
        root.add_folder(lib_dir)

        release_dir = ProjectDirectory("release")
        root.add_folder(release_dir)
        
        share_dir = ProjectDirectory("share")
        root.add_folder(share_dir)

        help_dir = ProjectDirectory("help")
        share_dir.add_folder(help_dir)

        test_dir = ProjectDirectory("test")
        share_dir.add_folder(test_dir)

        root.create(os.getcwd())

class QtHandler(BasicHandler):
    def __init__(self):
        BasicHandler.__init__(self)

    def tools(self):
        config = self.read_config()
        qt_toolkit = config["executable"]["qt_toolkit"]
        if qt_toolkit == "pyside":
            return ("pyside-rcc", "pyside-uic")
        elif qt_toolkit == "pyqt4":
            return ("pyrcc4", "pyuic4")
        elif qt_toolkit == "pyqt5":
            return ("pyrcc5", "pyuic5")
        raise Exception("Unknown Qt toolkit: {0}".format(qt_toolkit))

    def convert(self):
        path = os.getcwd()
        rcc, uic = self.tools()
        files = sum([[subdir + "/" + f for f in files if f.endswith(".ui") or f.endswith(".qrc")] for subdir, dirs, files in os.walk(path)], [])
        print("Searching and compiling UI files...")
        for f in files:
            path = os.path.dirname(f)
            name = os.path.basename(f)
            basename = os.path.splitext(os.path.basename(f))[0]
            print("   " + f)
            cmd = ""
            if f.endswith(".qrc"):
                cmd = ("cd '{path}'; {rcc} '{name}' -o '{basename}_rc.py'".format(
                    rcc=rcc,
                    path=path,
                    name=name,
                    basename=basename,
                ))
            elif f.endswith(".ui"):
                cmd = ("cd '{path}'; {uic} '{name}' -o '{basename}.py'".format(
                    uic=uic,
                    path=path,
                    name=name,
                    basename=basename,
                ))
        system_cmd(cmd)

import shutil

class VirtualExecutionHandler(BasicHandler):
    def __init__(self, path):
        BasicHandler.__init__(self)
        self.rootpath = path
        if not os.path.exists(path):
            os.makedirs(path)

    def transport_directories(self, subpath, linked):
        for name in os.listdir(subpath):
            #self.transport_file(os.path.join(subpath, name), linked)
            self.transport_file(os.path.join(subpath, name), linked=linked, destin_name=name)

    def transport_file(self, subpath, linked, destin_name=None):
        destin = os.path.join(self.rootpath, destin_name or subpath)
        #print("LINK:", subpath, "::", destin)
        #print("LINK:", origin, "::", os.getcwd())
        if os.path.exists(destin) or os.path.islink(destin):
            return
        if linked:
            origin = os.path.relpath(subpath, self.rootpath)
            os.symlink(origin, destin)
        else:
            origin = subpath
            shutil.copy(origin, destin)

    def create(self):
        config = self.read_config()
        app_package_name = config["application"]["name"]
        self.transport_directories("lib", linked=True)
        self.transport_directories("share", linked=True)
        self.transport_directories("config", linked=True)
        self.transport_file("dist", linked=True)
        self.transport_file(app_package_name, linked=True)
        self.transport_file(LicenseFile.DefaultName, linked=False)
        #self.transport_file(os.path.join("config", "application.json"), linked=False)
        #self.transport_file(os.path.join("config", WinBuildFile.DefaultName), linked=False)
        #self.transport_file(os.path.join("config", LinuxBuildFile.DefaultName), linked=False)
        #self.transport_file(os.path.join("config", PyInstallerConfigFile.DefaultName), linked=False)
        self.transport_file(AppInitFile.DefaultName, linked=False)
