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
from codecs import open
import utils

class ProjectUnit(object):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def create(self):
        pass

    @property
    def basename(self):
        return os.path.basename(self.name)

    @property
    def completename(self):
        name = self.name
        if self.parent:
            name = os.path.join(self.parent.completename, name)
        return name

    def local_path(self, basepath="."):
        return os.path.join(basepath, self.completename)


class ProjectFile(ProjectUnit):
    def __init__(self, name, parent=None, content=None):
        ProjectUnit.__init__(self, name, parent)
        self.content = content or ""

    def create(self, basename="."):
        filename = self.local_path(basename)
        dirpath = os.path.dirname(filename)
        if not os.path.exists(dirpath) and not os.path.islink(dirpath):
            os.makedirs(dirpath)
        #os.makedirs(os.path.dirname(filename))
        if os.path.exists(filename):
            print("File {0} already exists".format(filename))
            return
        with open(filename, "wt", encoding="utf8") as f:
            f.write(self.content or "")


class SymbolicFile(ProjectFile):
    def __init__(self, filename, targetname, parent=None):
        ProjectUnit.__init__(self, filename, parent)
        self.targetname = targetname

    def create(self, basename="."):
        filename = self.local_path(basename)
        dirpath = os.path.dirname(filename)
        if not os.path.exists(dirpath) and not os.path.islink(dirpath):
            os.makedirs(dirpath)
        if os.path.exists(filename) or os.path.islink(filename):
            os.remove(filename)
        os.symlink(filename, self.targetname)

class ProjectDirectory(ProjectUnit):
    def __init__(self, name, parent=None):
        ProjectUnit.__init__(self, name, parent)
        self.paths = []
        self.files = []

    def add_folder(self, path):
        self.paths.append(path)
        path.parent = self

    def add_file(self, file):
        self.files.append(file)
        file.parent = self

    def create(self, basename=".", all=True):
        dirpath = self.local_path(basename)
        if not os.path.exists(dirpath) and not os.path.islink(dirpath):
            os.makedirs(dirpath)
        if all:
            [path.create(basename) for path in self.paths]
            [path.create(basename) for path in self.files]


class SymbolicDirectory(ProjectDirectory):
    def __init__(self, name, parent=None):
        ProjectDirectory.__init__(self, name, parent)

    def create(self, basename="."):
        filename = self.local_path(basename)
        if os.path.exists(filename) or os.path.islink(filename):
            os.remove(filename)
        os.symlink(filename)

