"""
    report_timings.py
    given a timing data set, print a report with a couple options
"""

import argparse
import json
import os
import sys


def get_report(play_name, data, included_steps=None):
    report = ""
    report += "PLAY NAME:{}\n".format(play_name)
    report += "----PLAY----\n"
    report += "  DURATION: {0:<18}\n".format(data['play']['duration'])

    for path_name in data['paths']:
        report += "----{}----\n".format(path_name)
        report += "  DURATION: {0:<18}\n".format(
            data['paths'][path_name]['duration'])

        report += "    TOP 3 SLOWEST STEPS\n"
        for step in data['paths'][path_name]['top_3']:
            report += "{0:<20}: {1:<14} ({2}%)\n".format(
                step['name'], step['duration'], round(step['percent'], 2))

        if included_steps:
            for step in included_steps:
                if step not in data['paths'][path_name]['steps']:
                    continue
                report += "    ----{}----\n".format(step)
                report += "        DIFFERENCE: {0:<18}\n".format(
                    data['paths'][path_name]['steps'][step])
    return report


def top_three_by_play(paths):
    pass


def get_top_three(path_steps, path_duration):
    return [{
        'name': s['name'],
        'duration': s['duration'],
        'percent': s['duration'] / path_duration * 100
    } for s in sorted(path_steps, key=lambda e: e['duration'])[-3:]]


def get_report_data(data):
    report_data = {'paths': {}, 'steps': {}, 'play': {}}

    for path in data['paths']:
        for step in path['steps']:
            report_data['steps'][step['name']] = step['duration']

        start, stop = min(path['steps'], key=lambda s: s['start'])['start'], \
                      max(path['steps'], key=lambda s: s['end'])['end']
        duration = stop - start
        report_data['paths'][path['name']] = {'start': start, 'stop': stop, 'duration': duration,
                                              'top_3': get_top_three(path['steps'], duration)}

    start, stop = min([report_data['paths'][p]['start'] for p in report_data['paths']]), \
        max([report_data['paths'][p]['stop'] for p in report_data['paths']])
    duration = stop - start
    report_data['play'] = {'start': start, 'finish': stop, 'duration': duration,
                           'top_3': top_three_by_play(report_data['paths'])}

    return report_data


def normalize_start_times(path_data, start_time):
    for step in path_data['steps']:
        step['start'] = step['start'] - start_time
        step['end'] = step['start'] + step['duration']


def normalize(data):
    start_time = min(min(data['paths'],
                         key=lambda p: min([s['start'] for s in p['steps']]))['steps'],
                     key=lambda p: p['start'])['start']
    [normalize_start_times(path, start_time) for path in data['paths']]


def report_timings(timings_path, play_name="", no_normalize=False, print_out=False, out_path=""):
    with open(timings_path, 'r') as pt:
        timing_data = json.load(pt)

    if not no_normalize:
        normalize(timing_data)

    if not play_name:
        play_name = timing_data['title']
    else:
        play_name = play_name

    report = get_report(play_name, get_report_data(timing_data))
    if print_out:
        print(report)
    if out_path:
        os.makedirs(out_path, exist_ok=True)
        with open(os.path.join(out_path, "timing_report.txt"), 'w+') as f:
            f.write(report)


def main(args):
    report_timings(args.timings_path, args.name, args.no_normalize, args.print_out, args.out_path)


def get_args(argv):
    parser = argparse.ArgumentParser(description='reports processing time data output from '
                                                 'gather_timings.py')
    parser.add_argument('timings_path')
    parser.add_argument('--no-normalize', dest='no_normalize', action='store_true',
                        help='data set does not need to be normalized (data made relative to the '
                             'lowest timestamp')
    parser.add_argument('--name', dest='name', type=str, default='',
                        help='give the report a title')
    parser.add_argument('-p', '--print', dest='print_out', action='store_true',
                        help='print report to stdout')
    parser.add_argument('-o', '--out-path', dest='out_path', default="./",
                        help='specify path to output report to')

    return parser.parse_args(argv)


if __name__ == "__main__":
    main(get_args(sys.argv[1:]))
