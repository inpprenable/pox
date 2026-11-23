#!/usr/bin/env python
#
# Copyright 2011-2012 Andreas Wundsam
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A simple unit test that discovers all modules in the pox directory and
tries to load them
"""

import sys
from os import path
import os
import importlib

import unittest
SCRIPT_DIR=path.dirname(path.abspath(__file__))
ROOT=path.abspath(path.join(SCRIPT_DIR,"../.."))
sys.path.append(ROOT)

modules = []

for root, dirs, files in os.walk(ROOT):
  assert root.startswith(ROOT)
  relroot = root[len(ROOT)+1:]
  if not relroot.startswith("pox"): continue

  if not path.exists(path.join(root, "__init__.py")):
    continue
  packagename = relroot.replace(path.sep,".")
  modules.append(packagename)

  files = [f for f in files if f.endswith(".py")
           and not f.startswith("__") and f != "setup.py"]
  for f in sorted(files):
    modules.append(packagename + "." + f[:-3])


# Optional dependencies which may legitimately be missing
OPTIONAL_DEPS = ("tkinter", "_tkinter")

class ModuleLoadTest (unittest.TestCase):
  def test_load_modules (self):
    for module in sorted(modules):
      with self.subTest(module=module):
        try:
          importlib.import_module(module)
        except ImportError as e:
          if e.name in OPTIONAL_DEPS:
            self.skipTest("%s needs %s" % (module, e.name))
          raise


if __name__ == '__main__':
  unittest.main()
