import unittest
from unittest.mock import patch, MagicMock
from .data import get_all_stores, filter_play_executions_store_id
from src.org_http import OrgHttp


class TestOrgHttp(unittest.TestCase, OrgHttp):

    def setUp(self):
        # PRIVATE

    def test_get_stores_in_org(self):
        # PRIVATE

    def test_get_play_executions(self):
        # PRIVATE
