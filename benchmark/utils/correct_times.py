import re
import json
import argparse

import pandas as pd

from datetime import datetime


def fix_pid(path, offset):
    with open(path) as f:
        h1 = f.readline()
        h2 = f.readline()
        h3 = f.readline()
        columns = h3.strip('#').split()
        num_columns = len(columns)
        print("reading in csv")
        df = pd.DataFrame.from_records([l.split(maxsplit=num_columns - 1) for l in f],
                                       columns=columns)
    print("converting times")
    df['Time'] = df['Time'].apply(pd.to_timedelta, errors='coerce')
    print("applying offset")
    df['Time'] = df['Time'] + pd.Timedelta(str(offset) + ' hour')
    print("formatting times")
    df['Time'] = pd.to_datetime(df['Time'], errors='coerce').dt.time

    with open(path + "-fixed", 'w+') as f:
        f.write(h1)
        f.write(h2)
        f.write(h3)
        x = df.to_string(header=False, index=False, index_names=False).split('\n')
        print("writing to csv file")
        for entry in x:
            f.write(' '.join(entry.split()).strip('\n'))


def fix_timings(path, normal_hour, offset, exclude):
    d = json.load(open(path, 'r'))

    for p in d['paths']:
        for s in p['steps']:
            if s['name'] in exclude:
                continue
            if datetime.fromtimestamp(s['start']).hour < normal_hour:
                s['start'] += offset * 3600

    json.dump(d, open(path + "-fixed", 'w+'), indent=4)


def inspect_timings(path, include):
    with open(path, 'r') as f:
        d = json.load(f)

        for p in d['paths']:
            for s in p['steps']:
                if s['name'] in include:
                    print("{} - {} - {}".format(p['name'],
                                                s['name'],
                                                datetime.fromtimestamp(s['start'])))


def get_args():
    parser = argparse.ArgumentParser(description='fix times')
    parser.add_argument('-a', '--inspect', action="store_true", default=False)
    parser.add_argument('-t', '--timings_path')
    parser.add_argument('-p', '--pid_path')
    parser.add_argument('-i', '--include', nargs='+', default=[])
    parser.add_argument('-e', '--exclude', nargs='+', default=[])
    parser.add_argument('-o', '--offset', type=int)
    parser.add_argument('-n', '--normal-hour', type=int)

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    if args.timings_path:
        if args.inspect:
            inspect_timings(args.timings_path, args.include)
        else:
            fix_timings(args.timings_path, args.normal_hour, args.offset, args.exclude)
    elif args.pid_path:
        fix_pid(args.pid_path, args.offset)
