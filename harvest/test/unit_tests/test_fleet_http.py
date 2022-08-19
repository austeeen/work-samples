import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src.fleet_http import FleetHttp
from src.utils.helpers import date_from_play_id
from .data import get_all_play_executions, get_scan_events, get_robot_play_execution
from .data.data_factory import DATA_DIR


class TestFleetHttp(unittest.TestCase, FleetHttp):

    def setUp(self):
        # PRIVATE

    def test_set_auth(self):
        # PRIVATE

    def test_list_plays_between(self):
        # PRIVATE

    def test_list_plays_on(self):
        # PRIVATE

    def test_list_plays_since(self):
        # PRIVATE

    def test_list_plays_from(self):
        # PRIVATE

    def test_collect_scan_events(self):
        # PRIVATE
