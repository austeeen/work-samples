import os
import sys
import json
import unittest

from unittest.mock import patch
from configuration import Configuration

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), ".."))

SNAP_COMMON = os.environ.copy()['SNAP_COMMON']
SNAP = os.environ.copy()['SNAP']
IDL_PATH = 'PRIVATE'
data_path = '/usr/src/app/tests/data'
local_config_path = os.path.join(data_path, 'local_config.json')
snap_config_path = os.path.join(data_path, 'snap_config.json')


class TestStoreConfig(unittest.TestCase):

    def setUp(self):
        # PRIVATE

    @patch('configuration.utils.get_store_dn', return_value='PRIVATE')
    def test_get_PRIVATE_args(self, get_store):
        # PRIVATE

    """
        repeats test_get_[STORE]_args (...) for each store/customer
            - AH 08/19/22 Public Viewing Edits
    """
