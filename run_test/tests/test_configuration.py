import os
import sys
import json
import unittest

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), ".."))

from configuration import Configuration

SNAP = os.environ.copy()['PRIVATE']

data_path = '/usr/src/app/tests/data'
local_config_path = os.path.join(data_path, 'local_config.json')
snap_config_path = os.path.join(data_path, 'snap_config.json')

play_config_path = os.path.join(data_path, 'local_config.json')
path_config_path = os.path.join(data_path, 'snap_config.json')

aws_config_path = os.path.join(data_path, 'snap_config.json')
gcp_config_path = os.path.join(data_path, 'local_config.json')

aws_data_path = os.path.join(data_path, 'aws')


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.config = Configuration()
        self.config._args = []
        self.env = os.environ.copy()

    def test_validate_config(self):
        # PRIVATE

    def test_set_local_sources(self):
        # PRIVATE

    def test_set_snap_sources(self):
        # PRIVATE

    def test_set_play_path(self):
        # PRIVATE

    def test_set_path_path(self):
        # PRIVATE

    def test_set_local_python_path(self):
        # PRIVATE

    def test_set_snap_python_path(self):
        # PRIVATE

    def test_configure_aws_uploader(self):
        # PRIVATE

    def test_configure_gcp_uploader(self):
        # PRIVATE

    def test_get_args(self):
        # PRIVATE
