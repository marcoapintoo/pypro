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
import utils
from docopt import docopt
from basic_handlers import SkeletonHandler, QtHandler, VirtualExecutionHandler, WinBuildFile, LinuxBuildFile
from ui_handlers import ConsoleConfigHandler, ConsoleUnfinishedHandler


class Environment(object):
    def __init__(self, folder):
        self.handler = VirtualExecutionHandler(folder)
        self.handler.create()
        self.folder = folder
        self.cwd = os.getcwd()

    def __enter__(self, *args):
        os.chdir(self.folder)

    def __exit__(self, *args):
        os.chdir(self.cwd)


class CommonProject(object):
    def __init__(self):
        pass

    def read_config(self):
        reader = ConsoleConfigHandler()
        reader.dump_to_file()

    def create_project(self):
        skeleton = SkeletonHandler()
        skeleton.create_structure()

    def qt_update(self):
        handler = QtHandler()
        handler.convert()

    def debug_app(self, arguments):
        with Environment("debug") as env:
            app = "__init__.py"
            utils.OS.call("python", app, *arguments, in_another_thread=False)
            #os.system("python {app}".format(app=app))

    def pack_app(self, arguments):
        with Environment("debug") as env:
            app = WinBuildFile.DefaultName if os.name == "nt" else LinuxBuildFile.DefaultName
            utils.OS.call("python", app, *arguments, in_another_thread=False)
            #os.system("python {app}".format(app=app))

    def main(self):
        docstring = """
        PyPro 1.0 | Pinto's Python Project Manager
        Usage:
            pypro create
            pypro requirements add <name> [<version>]
            pypro requirements import all
            pypro update (qt | cython)
            pypro debug [<arguments>...]
            pypro show (problems | version | dependencies)
            pypro pack
            pypro release <version>
            pypro publish (git | pypi)
        """
        min_docstring = min(len(c)-len(c.lstrip()) for c in docstring.split("\n") if c.strip()!="")
        docstring = "\n".join(c[min_docstring:] for c in docstring.split("\n"))
        arguments = docopt(docstring)
        if arguments["create"]:
            self.read_config()
            self.create_project()
        elif arguments["requirements"]: 
            ConsoleUnfinishedHandler("requirements").show()
        elif arguments["update"] and arguments["qt"]: 
            self.qt_update()
        elif arguments["update"] and arguments["cython"]: 
            ConsoleUnfinishedHandler("update-cython").show()
        elif arguments["debug"]: 
            self.debug_app(arguments["<arguments>"] or [])
        elif arguments["show"]: 
            ConsoleUnfinishedHandler("show").show()
        elif arguments["pack"]: 
            self.pack_app(arguments["<arguments>"] or [])
        elif arguments["release"]: 
            ConsoleUnfinishedHandler("release").show()
        elif arguments["publish"]: 
            ConsoleUnfinishedHandler("publish").show()

    
if __name__ == "__main__":
    CommonProject().main()
        


