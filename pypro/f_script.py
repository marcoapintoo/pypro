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

class AppInitFile(ProjectFile):
	DefaultName = "__init__.py"
	def __init__(self, config, name=None, parent=None):
		name = name or self.DefaultName
		ProjectFile.__init__(self, name, parent=None)
		self.content = self.common_content(config)

	@staticmethod
	def common_content(config):
		return r"""#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import unicode_literals
#from __future__ import print_function
#from __future__ import absolute_import
__author__ = '{{Author}}'

from {{ApplicationPackage}} import *

""".replace(
			"{{Author}}", config["application"]["author"]
		).replace(
			"{{ApplicationPackage}}", config["application"]["name"]
		)


class PackageInitFile(ProjectFile):
	DefaultName = "__init__.py"
	def __init__(self, config, name=None, parent=None):
		name = name or self.DefaultName
		ProjectFile.__init__(self, name, parent=None)
		self.content = self.common_content(config)

	@staticmethod
	def common_content(config):
		return r"""#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import unicode_literals
#from __future__ import print_function
#from __future__ import absolute_import
__author__ = '{{Author}}'


""".replace(
			"{{Author}}", config["application"]["author"]
		).replace(
			"{{ApplicationPackage}}", config["application"]["name"]
		)

