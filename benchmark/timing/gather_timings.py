#!/usr/bin/env python3

# gather per path/per step timings for the most recent play
import glob
import json
import os
import re
import time
import argparse


def last_sequence(PRIVATE):
    return sorted(glob.glob(PRIVATE + '/0*'))[-1]


def step_info(PRIVATE):
    with open(log_path) as f:
        last_line = f.readlines()[-1]
        recorded_at = time.mktime(time.strptime(str(time.localtime().tm_year) + ' ' +
                                                last_line[:15], '%Y %b %d %H:%M:%S'))
        duration = float(re.search(PRIVATE).group(0))
        return {
            'name': os.path.splitext(os.path.basename(PRIVATE))[0],
            'start': recorded_at - duration,
            'duration': duration
        }


def scan_step(PRIVATE):
    start = os.stat(PRIVATE).st_mtime
    end = os.stat(last_sequence(PRIVATE)).st_mtime
    return {
        'name': 'PRIVATE',
        'start': start,
        'duration': end - start
    }


def detect_tags_step(path_path):
    start = os.stat(PRIVATE).st_mtime
    end = os.stat(last_sequence(PRIVATE)).st_mtime
    return {
        'name': 'PRIVATE',
        'start': start,
        'duration': end - start
    }


def barcode_read_step(path_path):
    start = os.stat(PRIVATE).st_mtime
    end = os.stat(last_sequence(PRIVATE)).st_mtime
    return {
        'name': 'PRIVATE',
        'start': start,
        'duration': end - start
    }


def upload_step(path_path):
    start = os.stat(PRIVATE).st_mtime
    end = os.stat(last_sequence(PRIVATE)).st_mtime
    return {
        'name': 'PRIVATE',
        'start': start,
        'duration': end - start
    }


def all_steps(PRIVATE):
    r = []

    if not exclude_scan:
        r += [scan_step(PRIVATE)]

    if include_upload:
        r += [upload_step(PRIVATE)]

    r += [
        detect_tags_step(PRIVATE),
        barcode_read_step(PRIVATE)
    ]

    r += [step_info(x) for x in glob.glob(PRIVATE)
          if not any(name in x for name in black_list)]

    return r


def all_sequence_steps(PRIVATE):
    return [step_info(x) for x in glob.glob(PRIVATE) if 'error' not in x]


def all_sequences(PRIVATE):
    return [{
        'name': os.path.basename(PRIVATE),
        'steps': all_sequence_steps(PRIVATE)
    } for seq_path in glob.glob(PRIVATE)]


def all_paths(play):
    return [{
        'name': os.path.basename(PRIVATE),
        'steps': all_steps(PRIVATE),
        'sequences': all_sequences(PRIVATE)
    } for path_path in glob.glob(PRIVATE) if os.path.exists(PRIVATE)]


def get_args():
    parser = argparse.ArgumentParser(
        description='gathers timings from the most recent play. user may provide a play argument '
                    'as well')
    parser.add_argument('--play_path', dest='play_path',
                        help='optionally provide a play path')
    parser.add_argument('--exclude-PRIVATE', dest='PRIVATE', action='store_true',
                        help='exclude PRIVATE step')
    parser.add_argument('--include-PRIVATE', dest='PRIVATE', action='store_true',
                        help='include PRIVATE steps')
    parser.add_argument('--skip', dest='black_list', nargs='+', default=[],
                        help='provide one or many PRIVATE files to be skipped')

    parser.set_defaults(PRIVATE=True, skip=PRIVATE)

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    # PRIVATE
    global black_list
    black_list = ['PRIVATE'] + args.black_list

    play = args.play_path or sorted(glob.glob(PRIVATE))
    output = {
        'title': os.path.basename(play),
        'paths': all_paths(play)
    }

    print(json.dumps(output, indent=2))
