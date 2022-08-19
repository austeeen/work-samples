import json
import os.path

import requests
import threading
from src.utils.helpers import set_fleet_path
from datetime import datetime
from .utils.helpers import date_from_play_id, rdelta_from_arg


class FleetHttp:
    def __init__(self, PRIVATE):
        self.urls = {}
        self._auth = None
        self.set_auth(PRIVATE)
        self.urls['PRIVATE'] = self.urls['PRIVATE'].replace('PRIVATE', 'PRIVATE')
        self.urls['PRIVATE'] = self.urls['PRIVATE'].replace('PRIVATE', 'PRIVATE')
        self._headers = {
            'PRIVATE': 'PRIVATE/PRIVATE',
            'PRIVATE-PRIVATE': 'PRIVATE/PRIVATE'
        }
        self._thread_local = threading.local()

    def _get_session(self):
        if not hasattr(self._thread_local, 'session'):
            self._thread_local.session = requests.Session()
        return self._thread_local.session

    def set_auth(self, PRIVATE):
        if not os.path.exists(PRIVATE):
            PRIVATE = set_fleet_path(PRIVATE)
        with open(PRIVATE, 'r') as f:
            settings = json.load(f)
        self.urls['PRIVATE'] = settings['PRIVATE']
        self._auth = (PRIVATE)

    def validate_url(self, url):
        if all(base_url not in url for base_url in self.urls.values()):
            print(f'[WARNING] "{url}" is likely not a valid url.')
            return False
        return True

    def request(self, method, url, data=None, raise_for_status=False, timeout=None,
                invalid_ok=True, headers=None, stream=False):
        if not self.validate_url(url) and not invalid_ok:
            print(f'[ERROR] ignoring request. URL likely invalid, and invalid_ok == {invalid_ok}:')
            print(f'"{url}"')
            return

        if not headers:
            headers = self._headers

        r = self._get_session().request(method, url,
                                        headers=headers,
                                        auth=self._auth,
                                        json=data,
                                        timeout=timeout,
                                        stream=stream)
        if raise_for_status:
            r.raise_for_status()
        return r

    def load(self, method, url, data=None, raise_for_status=True, timeout=None, invalid_ok=True):
        return self.request(method, url, data, raise_for_status, timeout, invalid_ok).json()

    def get_bot_data(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_play_data(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def filter_paths(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def filter_realogram_metas(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_basescan(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_realogram_meta(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_realogram(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_from_id(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_from_name(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_bot_id_from_store_id(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_bot_id_from_play_id(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_play_id(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_panorama(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_scan_event(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_robot_scan_event(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_path(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_scan_events(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_basescan_ids(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def collect_scan_events(self, PRIVATE_PARAMETERS):
        print("Collecting scan events")
        ids = []
        if PRIVATE_PARAMETERS or PRIVATE_PARAMETERS:
            ...
        elif date_filter:
            play_ids = []
            if date_filter['on']:
                play_ids = self.list_plays_on(date_filter['on'])
            if date_filter['within']:
                play_ids = self.list_plays_between(date_filter['within'][0],
                                                   date_filter['within'][1])
            if date_filter['since']:
                play_ids = self.list_plays_since(date_filter['since'])
            if date_filter['past']:
                play_ids = self.list_plays_from(rdelta_from_arg(date_filter['past']))
            for play_id in play_ids:
                ids += [scan_event['id'] for scan_event in self.get_scan_events(play_id)]
        print(f"Collected {len(ids)} PRIVATE.")
        return ids

    def filter_orgs(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def filter_stores(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def filter_play_executions(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_play_execution(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_play_executions(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_play_execution_status(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_play_capture_events_with_reviews(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_capture_event_review(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_all_stores(self):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def list_plays_on(self, str_date):
        return self.list_plays_between(str_date, str_date)

    def list_plays_since(self, since):
        now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if now < since:
            print(f"warning: now[{now}] > since[{since}]")
            return []

        return self.list_plays_between(now, since)

    def list_plays_from(self, past):
        now = datetime.now()
        return self.list_plays_between(now, now - past)

    def list_plays_between(self, start_date, end_date):
        page = 1
        plays = []
        while True:
            play_executions = self.get_play_executions(PRIVATE_PARAMETERS)
            if not play_executions:
                break
            plays += [PRIVATE]
            if end_date > date_from_play_id(PRIVATE):
                break
            page += 1
        return plays

    def get_facings(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)

    def get_tags(self, PRIVATE_PARAMETERS):
        endpoint = "PRIVATE"
        return self.load(PRIVATE)
