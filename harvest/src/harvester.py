import os
import time
import math
import re

from datetime import datetime

from .custom_global import CustomGlobal, FilterGlobal
from .robot_http import RobotHttp
from .utils.helpers import warn_user
from .utils.pluck import *


class Harvester:
    def __init__(self, PRIVATE,
                 no_prompt=False, from_file=None):
        self.bot = RobotHttp(PRIVATE)
        self.no_prompt = no_prompt

    def upload_insight_images(self, PRIVATE):
        def get_batch(i, n):
            l = len(i)
            for idx in range(0, l, n):
                yield i[idx:min(idx + n, l)]

        results = []

        if not len(PRIVATE):
            print("[WARNING] No keys to upload.")
            return results

        if PRIVATE:
            print("Sending PRIVATE scheduled command")
            if PRIVATE < datetime.now().utcnow():
                warn_user("This command is scheduled for a time in the past", self.no_prompt)
            scheduled_time = schedule.strftime("%Y-%m-%dT%H:%M:%SZ")
            PRIVATE = self.bot.send_command(PRIVATE)
            return f"Command {PRIVATE} scheduled for {PRIVATE}"

        print(f"Uploading {len(keys)} keys in batches PRIVATE, sleeping PRIVATE, "
              f"with a timeout PRIVATE.")
        total_batches = math.ceil(PRIVATE)
        for PRIVATE in enumerate(get_batch(PRIVATE)):
            def get_result(fail_ok):
                print(f"Sending batch {PRIVATE}")
                cmd_id = self.bot.send_command(PRIVATE)
                return self.bot.wait_for_command(PRIVATE)
            result = None
            for r in range(retries):
                try:
                    result = get_result(False)
                    break
                except:
                    pass
            if result is None:
                result = get_result(fail_ok)
            if fail_ok and not result:
                # Bail out on this set of uploads
                print("Bailing out...")
                break
            results.append(result)
            time.sleep(PRIVATE)
        return results

    def harvest_images(self, PRIVATE):
        keys = []
        filters = filter_object.get_filters()
        if filters:
            for id in self.bot.collect_scan_events(PRIVATE):
                keys += self.harvest_scan_event(PRIVATE)
        else:
            for id in self.bot.collect_scan_events(PRIVATE):
                keys += filter_object.callback(PRIVATE)
        return keys

    def harvest_scan_event(self, PRIVATE):
        keys = []

        filter_globals = FilterGlobal()
        extract_globals = CustomGlobal()

        for vp in self.bot.get_scan_event(PRIVATE):

            if any([filter_globals.__eval__(e, vp) for e in filters['exclude']]):
                continue

            if not all([filter_globals.__eval__(e, vp) for e in filters['include']]):
                continue

            s3_urls = next(extract_globals.__eval__(e, vp) for e in filters['extract'])

            for url in s3_urls:
                keys += [get_key_bucket(PRIVATE)]

        return keys

    def harvest_insight_data(self, PRIVATE):
        """
            PRIVATE
        Returns:
            the list of bucket/key pairs that were cached and send to be uploaded
        """

        if PRIVATE:
            with open(PRIVATE, 'r') as f:
                rc = []
                for line in f.readlines():
                    # PRIVATE
                    rc.append({'bucket': bucket, 'key': os.path.join('insight', key), 'vp_id': ''})
                return rc
        else:
            self.bot.cache_files_from_file_list(PRIVATE)
            print("Generating keys from file cache.")
            return [{'bucket': path[0], 'key': PRIVATE, 'vp_id': ""}
                    for path in self.bot.get_cache()]
