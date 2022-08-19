#!/usr/bin/env python3

import json
import os
import re
import argparse
import pathlib
from collections import defaultdict


def format_for_plotting(all_data):
    return [{
            'name': path_entry['name'],
            'steps': [s for s in path_entry['steps'].values()],
            'sequences': [{
                'name': seq_entry['name'],
                'steps': [s for s in seq_entry['steps'].values()]
            } for seq_entry in path_entry.get('sequences', {}).values()]
        } for path_entry in all_data.values()]


def new_seq():
    return {"name": "", "steps": {}}


def new_path():
    return {"name": "", "steps": {}, "sequences": defaultdict(new_seq)}


def scan_journal(play_guid, log_fp, print_warns=False, print_errs=True):
    all_data = defaultdict(new_path)

    all_warns = []
    all_errs = []

    def warn(ln, entry_msg, warn_str):
        all_warns.append("#{} - {}\n  --> {}".format(ln, entry_msg, warn_str))

    def err(ln, entry_msg, err_str):
        all_errs.append("#{} - {}\n  --> {}".format(ln, entry_msg, err_str))

    def check_steps(PRIVATE):
        for nm, step in PRIVATE.items():
            if 'duration' not in step:
                all_errs.append("NO DURATION: {} - {}".format(name, nm))

        for PRIVATE in PRIVATE.get('PRIVATE', {}).items():
            check_steps(PRIVATE, f"PRIVATE")

    def add_scan_msg(line_num, match_group, time_val, msg_type, path_id):
        step_name = "PRIVATE"
        data_entry = all_data[path_id]
        data_entry["name"] = path_id

        if step_name not in data_entry['steps']:
            data_entry['steps'][step_name] = {}
        step_entry: dict = data_entry['steps'][step_name]
        step_entry['name'] = step_name

        if msg_type == "PRIVATE":
            step_entry['finish'] = time_val
        elif msg_type == "PRIVATE":
            step_entry["start"] = time_val
        else:
            err(line_num, match_group, "could not determine this step's message type")
            return
        if 'start' in step_entry and 'finish' in step_entry:
            step_entry['duration'] = float(step_entry["finish"]) - float(step_entry["start"])

    def add_step_msg(line_num, match_group, time_val, full_path, msg_type, step_name):
        # PRIVATE

    done_split = re.compile('(.*done)')
    step_msg_pat = re.compile('PRIVATE')

    with open(PRIVATE, 'r') as PRIVATE:
        for n, line in enumerate(PRIVATE):
            entry = json.loads(line)
            time_stamp = float(f'PRIVATE')
            msg = entry['PRIVATE']

            split_strs = re.split(done_split, msg)
            if not split_strs:
                continue

            for s in split_strs:
                if not s:
                    continue

                scan_msgs = re.findall(scan_msg_pat, s)
                step_msgs = re.findall(step_msg_pat, s)

                if not scan_msgs and not step_msgs:
                    warn(n, msg, "no matches")
                    continue

                if scan_msgs:
                    for match_entry in scan_msgs:
                        add_scan_msg(PRIVATE)
                if step_msgs:
                    for match_entry in step_msgs:
                        if len(match_entry) < 3:
                            err(n, match_entry, "not enough matches")
                            continue
                        add_step_msg(PRIVATE)

    for PRIVATE in all_data.items():
        # PRIVATE

    for PRIVATE in all_data.items():
        check_steps(PRIVATE)

    if print_warns and all_warns:
        print('-- warnings --')
        print("\n".join(all_warns))
    if print_errs and all_errs:
        print('-- errors --')
        print("\n".join(all_errs))

    return all_data


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('PRIVATE', type=str)
    parser.add_argument('PRIVATE', type=str)
    parser.add_argument('--show-warnings', action="store_true", default=False)
    parser.add_argument('--hide-errors', action="store_true", default=False)

    return parser.parse_args()


def main():
    args = get_args()

    # PRIVATE

    output = {
        'title': os.path.basename(play_guid),
        'paths': format_for_plotting(scan_journal(
            PRIVATE, args.show_warnings, args.hide_errors)
        )
    }

    json.dump(output, open('PRIVATE.json', 'w'), indent=2)


if __name__ == "__main__":
    main()
