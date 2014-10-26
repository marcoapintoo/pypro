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
from basic_handlers import BasicConfigHandler, BasicUnfinishedHandler

class ConsoleUnfinishedHandler(BasicUnfinishedHandler):
    def __init__(self, feature_name):
        BasicUnfinishedHandler.__init__(self, feature_name)

    def show_ui(self, *args):
        F  = npyscreen.Form(name = "PyPro | Pinto's Python Project Manager.",)
        F.add(npyscreen.BoxTitle,
            name = "FEATURE: {0}".format(self.feature_name),
            editable=False,
            values=["Sorry.", "This feature is not finished yet."],
            rely=5,
            max_height=10,
            scroll_exit=True,
        )
        F.edit()

    def show(self):
        npyscreen.wrapper_basic(self.show_ui)



class ConsoleConfigHandler(BasicConfigHandler):
    def __init__(self):
        BasicConfigHandler.__init__(self)

    def read_input_ui(self, *args):
        config = {
            "application": {},
            "executable": {},
        }
        # These lines create the form and populate it with widgets.
        # A fairly complex screen in only 8 or so lines of code - a line for each control.
        F  = npyscreen.Form(name = "PyPro | Pinto's Python Project Manager.",)
        project_name_widget  = F.add(npyscreen.TitleText, begin_entry_at=20,
            name="Project name:",
            value="project_one",
        )
        project_author_widget  = F.add(npyscreen.TitleText, begin_entry_at=20,
            name="Author(s):",
            value="John Smith",
        )
        project_descript_widget  = F.add(npyscreen.MultiLineEditableTitle, begin_entry_at=20,
            name="Description:",
            values=["General purpose project."],
            max_height=5,
            rely=2+2,
            scroll_exit=True,
        )
        project_date_widget  = F.add(npyscreen.TitleDateCombo, begin_entry_at=20,
            name="Creation date:",
            value=datetime.datetime.now()
        )
        exec_name_widget = F.add(npyscreen.TitleText, begin_entry_at=20,
            name="Executable name:",
            value="p1",
            scroll_exit=True,
        )
        exec_icon_widget = F.add(npyscreen.TitleFilenameCombo, begin_entry_at=20,
            name="Executable icon:"
        )
        exec_qt_widget = F.add(npyscreen.TitleSelectOne, begin_entry_at=20,
            max_height=3,
            value = [2,],
            name="Qt Toolkit",
            values = ["PyQt4", "PyQt5", "PySide"],
            scroll_exit=True
        )

        # This lets the user play with the Form.
        F.edit()

        config["application"]["name"] = project_name_widget.value or ""
        config["application"]["author"] = project_author_widget.value or ""
        config["application"]["description"] = "".join(project_descript_widget.values or [])
        config["application"]["creation"] = project_date_widget.value or ""
        config["executable"]["name"] = exec_name_widget.value or ""
        config["executable"]["icon"] = exec_icon_widget.value or ""
        config["executable"]["qt_toolkit"] = (exec_qt_widget.values[exec_qt_widget.value[0]] or "").lower()
        return config


    def read_input(self):
        config = npyscreen.wrapper_basic(self.read_input_ui)
        return config

try:
    import npyscreen
    import curses
except ImportError:
    print("For a more comfortable interface, we suggest to install npyscreen and ncurses.")
    ConsoleConfigHandler = BasicConfigHandler
    ConsoleUnfinishedHandler = BasicUnfinishedHandler