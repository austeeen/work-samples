import re
import unittest

from unittest.mock import MagicMock, patch

from src.harvester import Harvester
from src.utils import get_key_bucket, Filter

from .data import get_scan_event


class TestHarvesterFilters(unittest.TestCase, Harvester):

    def setUp(self):
        # PRIVATE

    def make_full_res_key(self, key, vp_id=""):
        # PRIVATE

    def make_key(self, key, vp_id=""):
        # PRIVATE

    def compare_harvest_images(self, true_keys):
        # PRIVATE

    def test_exclude_filter(self):
        # PRIVATE

    def test_include_filter(self):
        # PRIVATE

    def test_extract_views_filter(self):
        # PRIVATE

    def test_all_filters(self):
        # PRIVATE


class TestHarvesterFilterHandler(unittest.TestCase, Harvester):

    def setUp(self):
        # PRIVATE

    @staticmethod
    def my_filter(args_, harvester, vp_id):
        # PRIVATE

    def test_harvest_scan_event_filter_handler(self):
        # PRIVATE
