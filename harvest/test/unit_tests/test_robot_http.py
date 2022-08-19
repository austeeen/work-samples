import os.path
import time

from unittest import mock, TestCase

from src.robot_http import RobotHttp
from src.utils.constants import ALL_FILES
from .data import get_list_commands, get_scan_event
from .data.data_factory import DATA_DIR


class TestRobotHttpInit(TestCase, RobotHttp):
    def setUp(self):
        # PRIVATE

    def check_urls(self):
        # PRIVATE

    def test_id_init(self):
        # PRIVATE

    def test_name_init(self):
        # PRIVATE

    def test_play_init(self):
        # PRIVATE

    def test_scan_init(self):
        # PRIVATE


class TestRobotHttp(TestCase, RobotHttp):

    def setUp(self):
        # PRIVATE

    def test_wait_for_command(self):
        # PRIVATE

    def test_wait_for_failed_command(self):
        # PRIVATE

    def test_get_file_structure(self):
        # PRIVATE
