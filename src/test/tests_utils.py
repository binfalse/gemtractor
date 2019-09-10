# This file is part of the enalyzer
# Copyright (C) 2019 Martin Scharm <https://binfalse.de>
# 
# The enalyzer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# The enalyzer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from modules.enalyzer_utils.utils import Utils
from django.test import TestCase
import os
import tempfile

class UtilsTests (TestCase):
  def test_byte_conversion (self):
    self.assertEqual ("1 Byte", Utils.human_readable_bytes (1))
    self.assertEqual ("0 Bytes", Utils.human_readable_bytes (0))
    self.assertEqual ("517 Bytes", Utils.human_readable_bytes (517))
    self.assertEqual ("1.0 KB", Utils.human_readable_bytes (1024))
    self.assertEqual ("1.1 KB", Utils.human_readable_bytes (1099))
    self.assertEqual ("2.2 MB", Utils.human_readable_bytes (2314897))
    self.assertEqual ("2.2 GB", Utils.human_readable_bytes (2314897000))
    self.assertEqual ("2.1 TB", Utils.human_readable_bytes (2314897000000))
    self.assertEqual ("2.1 PB", Utils.human_readable_bytes (2314897000000000))

  def test_create_dir (self):
    dd = tempfile.TemporaryDirectory()
    d = dd.name
    self.assertTrue(os.path.isdir(d), msg="tempfile didn't create temp directory!??")
    os.rmdir (d)
    self.assertFalse(os.path.isdir(d), msg="we weren't able to remove the temp directory during tests")
    Utils._create_dir (d)
    self.assertTrue(os.path.isdir(d), msg="Utils was not able to create a creatable directory")
    Utils._create_dir (d)
    self.assertTrue(os.path.isdir(d), msg="Utils was not able to create an existing directory")
    
    # make sure the user cannot create a dir in /
    self.assertTrue(os.geteuid() != 0, msg="you must not execute the tests as root user!")
    with self.assertRaises (PermissionError):
        Utils._create_dir ("/PYTHON_SHOULD_FAIL")
    
    self.assertTrue(os.path.isdir(d), msg="suddenly the directory is lost!?")
