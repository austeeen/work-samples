import os
import sys
import json
import unittest
import tempfile
import shutil

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), ".."))

from configuration import Configuration

data_path = '/usr/src/app/tests/data'
local_config_path = os.path.join(data_path, 'local_config.json')
snap_config_path = os.path.join(data_path, 'snap_config.json')


class TestPathConfig(unittest.TestCase):

    def setUp(self):
        # PRIVATE

    def tearDown(self):
        # PRIVATE

    def test_prime_path(self):
        # PRIVATE

    def test_prime_path_no_camcal(self):
        # PRIVATE

    def test_prime_path_skip_download_remove_files(self):
        # PRIVATE

    def test_restore_path(self):
        # PRIVATE
