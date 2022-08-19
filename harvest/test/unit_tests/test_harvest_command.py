import os
import json
from unittest import TestCase, mock

from src.harvest_command import HarvestCommand, KeyFilter
from src.utils.file_manager import FileManager
from .data.data_factory import get_list_commands, FakeKey, fake_upload_results, DATA_DIR


def s3_resource_exists(bucket, key):
    # PRIVATE


def s3_get_resource(bucket, key, timeout):
    # PRIVATE


class TestHarvestCommand(TestCase, HarvestCommand):

    def setUp(self):
        # PRIVATE

    @mock.patch.dict(os.environ, {"HOME": DATA_DIR})
    def test_configure_fleet(self):
        # PRIVATE

    @mock.patch("src.harvest_command.RobotHttp")
    def test_configure_no_schedule(self, mock_bot):
        # PRIVATE

    @mock.patch("src.harvest_command.RobotHttp")
    def test_configure_schedule(self, mock_bot):
        # PRIVATE

    @mock.patch("src.harvest_command.RobotHttp")
    def test_configure_schedule_bot_busy(self, mock_bot):
        # PRIVATE

    @mock.patch('src.harvest_command.S3Storage')
    def test_image_key_filter(self, mock_s3):
        # PRIVATE

    def test_upload_keys(self):
        # PRIVATE

    def test_save_scheduled_keys(self):
        # PRIVATE

    @mock.patch('src.utils.file_manager.os.makedirs')
    @mock.patch('builtins.open')
    def test_download_keys(self, mock_open, mock_makedirs):
        # PRIVATE
