import unittest
from unittest.mock import patch, MagicMock

from src.store_http import StoreHttp
from .data import filter_play_executions_store_id


class TestStoreHttp(unittest.TestCase, StoreHttp):

    def setUp(self):
        # PRIVATE

    def test_get_play_executions(self):
        # PRIVATE
