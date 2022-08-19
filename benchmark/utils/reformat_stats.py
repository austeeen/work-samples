import sys
import json
import argparse


def reorganize(timing_data):
    n_data = {}
    for path in timing_data['paths']:
        n_steps = {}
        for step in path['steps']:
            name = step['name']
            del step['name']
            n_steps[name] = step
        n_data[path['name']] = n_steps
    return n_data


def normalize_start_times(path_data, start_time):
    for step in path_data['steps']:
        step['start'] = step['start'] - start_time
        step['end'] = step['start'] + step['duration']


def normalize(data):
    start_time = min(min(data['paths'],
                         key=lambda p: min([s['start'] for s in p['steps']]))['steps'],
                     key=lambda p: p['start'])['start']
    [normalize_start_times(path, start_time) for path in data['paths']]


def reformat(data):
    normalize(data)
    return reorganize(data)


def get_args(args):
    parser = argparse.ArgumentParser(description='reports processing time data output from '
                                                 'gather_timings.py')
    parser.add_argument('timings_path')
    return parser.parse_args(args)


def main(args):
    args = get_args(args)
    with open(args.timings_path, 'r') as pt:
        timing_data = json.load(pt)

    reorg_data = reformat(timing_data)

    new_file_name = ".".join(args.timings_path.split(".")[:-1]) + "_reorg.json"

    with open(new_file_name, 'w+') as pt:
        json.dump(reorg_data, pt)


if __name__ == "__main__":
    main(sys.argv[1:])


