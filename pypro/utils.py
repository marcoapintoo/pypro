 #!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
#from __future__ import absolute_import
from __future__ import unicode_literals
__author__ = 'marco'

import os
import sys
import re
import tempfile
import shutil
import contextlib
from threading import Thread
import os
import ctypes

class OS(object):
    @staticmethod
    def call(program, *args, **config):
        in_another_thread = config.get("in_another_thread", True)
        if in_another_thread:
            thread = Thread(target=OS.direct_call, args=[program] + list(args), kwargs=config)
            thread.start()
        else:
            OS.direct_call(program, *args, **config)

    @staticmethod
    def direct_call(program, *args, **config):
        convert_slashes = config.get("convert_slashes", True)
        on_finish = config.get("on_finish", None)
        if convert_slashes and os.name == "nt":
            program = program.replace("/", "\\")
        app_args = []
        for arg in args:
            narg = arg
            if convert_slashes and os.name == "nt":
                narg = narg.replace("/", "\\")
            if " " in narg or "\t" in narg:
                narg = '"{0}"'.format(narg)
            app_args.append(narg)
        cmd =("{0} {1}".format(program, " ".join(app_args)))
        #print("CMD:", cmd)
        os.system(cmd)
        if on_finish:
            on_finish(cmd)

    @staticmethod
    def change_ext(filename, ext):
        return os.path.splitext(filename)[0] + ext

    @staticmethod
    @contextlib.contextmanager
    def make_temp_directory():
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)


class PDF(object):
    rxcountpages = re.compile(r"$\s*/Type\s*/Page[/\s]", re.MULTILINE|re.DOTALL)
    @staticmethod
    def countPages(filename):
        """http://code.activestate.com/recipes/496837-count-pdf-pages/"""
        data = file(filename,"rb").read()
        return len(PDF.rxcountpages.findall(data))


if getattr("sys", "__patch_symlink__", False):
    sys.__patch_symlink__ = True
    __CSL = None
    def patch_symlink():
        #_symlink = os.symlink
        _symlink = getattr(os, "symlink", None)

        def symlink(source, link_name):
            """symlink(source, link_name)
               Creates a symbolic link pointing to source named link_name"""
            if os.path.exists(link_name) or os.path.islink(link_name):
                print(link_name, "already exists")
                return
            if os.name != "nt":
                _symlink(source, link_name)
                return
            try:
                global __CSL
                if __CSL is None:
                    import ctypes
                    csl = ctypes.windll.kernel32.CreateSymbolicLinkW
                    csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
                    csl.restype = ctypes.c_ubyte
                    __CSL = csl
                flags = 0
                if source is not None and os.path.isdir(source):
                    flags = 1
                if __CSL(link_name, source, flags) == 0:
                    raise ctypes.WinError()
            except Exception, e:
                print(e)
        os.symlink = symlink
