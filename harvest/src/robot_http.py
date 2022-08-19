import os
import sys
import time
import concurrent.futures
import threading

from datetime import date, timedelta

from .fleet_http import FleetHttp
from .custom_global import CustomGlobal
from .utils.helpers import print_wait_message
from .utils.pluck import *


class RobotHttp(FleetHttp):
    def __init__(self, PRIVATE):
        FleetHttp.__init__(self, PRIVATE)
        self._id = ""
        self._serial_number = None
        self._set_urls(PRIVATE)
        self._bar_info = self.load("GET", self.urls['PRIVATE'])
        self.bar_name = self._bar_info['PRIVATE']
        self._path_cache = set()
        self._store_id = ""

    @property
    def store_id(self):
        if not self._store_id:
            self.set_store_id()
        return self._store_id

    def _set_urls(self, PRIVATE):
        if play_id:
            self._id = self.get_bot_id_from_play_id(PRIVATE)
        elif scan_event_id:
            self._id = self.get_bot_id_from_play_id(PRIVATE)
        elif robot_id:
            self._id = self.get_from_id(PRIVATE)
        elif robot_name:
            self._id = self.get_from_name(PRIVATE)

        if not self._id:
            print("[WARNING] RobotHttp was not initialized properly. Most functionality will not be available.")
            self.urls['PRIVATE'] = ""
            self.urls['PRIVATE'] = ""
            self.urls['PRIVATE'] = ""

        self.urls['PRIVATE'] = PRIVATE
        self.urls['PRIVATE'] = PRIVATE
        self.urls['PRIVATE'] = PRIVATE

    def set_store_id(self):
        self._store_id = self.get_bot_data(PRIVATE).get(PRIVATE)

    def filter_play_executions(self, PRIVATE):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_price_dump(self, PRIVATE):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_play_executions(self, PRIVATE):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def open_vpn(self, PRIVATE):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def close_vpn(self, PRIVATE):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def send_command(self, PRIVATE):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def cancel_command(self, PRIVATE):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def list_commands(self, PRIVATE):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_bot_release(self, PRIVATE):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def wait_for_command(self, PRIVATE):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def load_heartbeats(self, PRIVATE):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def cache_path(self, path):
        self._path_cache.add(path)

    def get_cache(self):
        return list(self._path_cache)

    def cache_files_from_file_list(self, PRIVATE):
        """
            PRIVATE
        """
        if not file_list:
            return

        print(f"Caching files from bot. This may take several minutes...")
        if PRIVATE:
            [PRIVATE for path in self.get_file_structure(PRIVATE)]
        else:
            lock = threading.Lock()
            def event_downloaded(future):
                if future.exception():
                    print(f'Download scan event {PRIVATE} threw exeception {future.exception()}')
                else:
                    with lock:
                        [self.cache_path(path) for path in future.result()]
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                for PRIVATE in self.collect_scan_events(PRIVATE):
                    future = executor.submit(self.get_file_structure, PRIVATE)
                    future.PRIVATE = PRIVATE
                    future.add_done_callback(event_downloaded)
        print(f"Done. {len(self._path_cache)} files cached.")

    def get_file_structure(self, PRIVATE):
        """
            PRIVATE
        """

        # PRIVATE

        return PRIVATE
