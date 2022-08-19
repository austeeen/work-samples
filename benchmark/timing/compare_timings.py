"""
    compare_timings.py

    given two timing data sets from a Control and a Compare play, compare the data

"""

import argparse
import json
import os


class CompareTimings:
    def __init__(self, control_timing_data, compare_timing_data, control_name="", compare_name="",
                 normalize=False):
        self._control_timing_data = control_timing_data
        self._compare_timing_data = compare_timing_data

        self._control_name = control_name
        self._compare_name = compare_name

        if normalize:
            self._normalize_all(control_timing_data)
            self._normalize_all(compare_timing_data)

        self.data = {
            'paths': {}
        }

        self._compare()

    def _compare(self):
        for path in self._control_timing_data['paths']:
            compare_path = next((p for p in self._compare_timing_data['paths']
                                 if p['name'] == path['name']), None)
            if not compare_path:
                print("path {} does not exist in control play.".format(path['name']))
                continue

            self.data['paths'][path['name']] = self._compare_path_timings(path, compare_path)

        self._get_play_durations()

        # TODO: take slope of end-time for last step in each path as a performance number

    @staticmethod
    def _compare_path_timings(control_timing, compare_timing):
        def get_start_finish_times(steps):
            return min(steps, key=lambda s: s['start'])['start'], \
                   max(steps, key=lambda s: s['end'])['end']

        data = {'steps': {}}

        control_overflow = 0
        compare_overflow = 0
        for step in control_timing['steps']:
            compare_step = next((s for s in compare_timing['steps'] if s['name'] == step['name']),
                                None)
            if not compare_step:
                control_overflow += step['duration']
            else:
                data['steps'][step['name']] = (step['duration'] - compare_step['duration'])

        for step in compare_timing['steps']:
            control_step = next((s for s in control_timing['steps'] if s['name'] == step['name']),
                                None)
            if not control_step:
                compare_overflow += step['duration']

        control_start, control_stop = get_start_finish_times(control_timing['steps'])
        compare_start, compare_stop = get_start_finish_times(compare_timing['steps'])

        data['control'] = {
            'start': control_start,
            'stop': control_stop,
            'duration': control_stop - control_start,
            'overflow': control_overflow
        }
        data['compare'] = {
            'start': compare_start,
            'stop': compare_stop,
            'duration': compare_stop - compare_start,
            'overflow': compare_overflow
        }

        data['total-difference'] = data['control']['duration'] - data['compare']['duration']

        base = max(data['control']['duration'], data['compare']['duration'])
        data['percent-difference'] = data['total-difference'] / base * 100

        data['control']['top-3'] = CompareTimings._get_top_three(control_timing['steps'],
                                                                 data['control']['duration'],
                                                                 data['steps'])
        data['compare']['top-3'] = CompareTimings._get_top_three(compare_timing['steps'],
                                                                 data['compare']['duration'],
                                                                 data['steps'])

        return data

    @staticmethod
    def _get_top_three(path_steps, path_duration, step_differences):
        return [{
            'name': s['name'],
            'duration': s['duration'],
            'percent': s['duration'] / path_duration * 100,
            'difference': step_differences.get(s['name'], 0)
        } for s in sorted(path_steps, key=lambda e: e['duration'])[-3:]]

    def _get_play_durations(self):
        def get_start_finish_times(play_type):
            return min([self.data['paths'][p][play_type]['start'] for p in self.data['paths']]),\
                   max([self.data['paths'][p][play_type]['stop'] for p in self.data['paths']])

        control_start, control_finish = get_start_finish_times('control')
        compare_start, compare_finish = get_start_finish_times('compare')

        self.data['play'] = {
            'control': {
                'start': control_start,
                'finish': control_finish,
                'duration': control_finish - control_start,
                'overflow': sum(self.data['paths'][p]['control']['overflow']
                                for p in self.data['paths'])
            },
            'compare': {
                'start': compare_start,
                'finish': compare_finish,
                'duration': compare_finish - compare_start,
                'overflow': sum(self.data['paths'][p]['compare']['overflow']
                                for p in self.data['paths'])
            }
        }
        self.data['play']['total-difference'] = \
            self.data['play']['control']['duration'] - self.data['play']['compare']['duration']

        base = max(self.data['play']['control']['duration'],
                   self.data['play']['compare']['duration'])
        self.data['play']['percent-difference'] = \
            self.data['play']['total-difference'] / base * 100

        self.data['play']['control']['overflow-percent'] = \
            self.data['play']['control']['overflow'] / self.data['play']['control']['duration'] \
            * 100

        self.data['play']['compare']['overflow-percent'] = \
            self.data['play']['compare']['overflow'] / self.data['play']['compare']['duration'] \
            * 100

    def _normalize_all(self, data):
        start_time = min(min(data['paths'],
                             key=lambda p: min([s['start'] for s in p['steps']]))['steps'],
                         key=lambda p: p['start'])['start']
        [self.normalize_start_times(path, start_time) for path in data['paths']]

    @staticmethod
    def normalize_start_times(path_data, start_time):
        for step in path_data['steps']:
            step['start'] = step['start'] - start_time
            step['end'] = step['start'] + step['duration']

    def print_report(self, included_steps=None, top_3=False):
        report = ""
        report += "CONTROL:{}\n".format(self._control_name)
        report += "COMPARE:{}\n".format(self._compare_name)
        report += "----PLAY----\n"
        report += "  CONTROL DURATION: {0:<18}\n".format(self.data['play']['control']['duration'])
        if self.data['play']['control']['overflow']:
            report += "    OVERFLOW: {0:<18} ({1}%)\n".format(
                self.data['play']['control']['overflow'],
                round(self.data['play']['control']['overflow-percent'], 2))

        report += "  COMPARE DURATION: {0:<18}\n".format(self.data['play']['compare']['duration'])
        if self.data['play']['compare']['overflow']:
            report += "    OVERFLOW: {0:<18} ({1}%)\n".format(
                self.data['play']['compare']['overflow'],
                round(self.data['play']['compare']['overflow-percent'], 2))

        report += "    DIFFERENCE:     {0:<18} ({1}%)\n".format(
            self.data['play']['total-difference'],
            round(self.data['play']['percent-difference'], 2))

        for path_name in self.data['paths']:
            report += "----{}----\n".format(path_name)
            report += "  CONTROL DURATION: {0:<18}\n".format(
                self.data['paths'][path_name]['control']['duration'])
            report += "  COMPARE DURATION: {0:<18}\n".format(
                self.data['paths'][path_name]['compare']['duration'])
            report += "    DIFFERENCE:     {0:<18} ({1}%)\n".format(
                self.data['paths'][path_name]['total-difference'],
                round(self.data['paths'][path_name]['percent-difference'], 2)
            )

            if top_3:
                report += "    TOP 3 SLOWEST STEPS -- CONTROL\n"
                for step in self.data['paths'][path_name]['control']['top-3']:
                    report += "{0:<20}: {1:<14} ({2}%) -- difference: {3}\n".format(
                        step['name'], step['duration'], round(step['percent'], 2),
                        step['difference'])
                report += "    TOP 3 SLOWEST STEPS -- COMPARE\n"
                for step in self.data['paths'][path_name]['compare']['top-3']:
                    report += "{0:<20}: {1:<14} ({2}%) -- difference: {3}\n".format(
                        step['name'], step['duration'], round(step['percent'], 2),
                        step['difference'])

            if included_steps:
                for step in included_steps:
                    if step not in self.data['paths'][path_name]['steps']:
                        continue
                    report += "    ----{}----\n".format(step)
                    report += "        DIFFERENCE: {0:<18}\n".format(
                        self.data['paths'][path_name]['steps'][step])

        print(report)

    def save_data(self, out_path):
        if not os.path.exists(os.path.dirname(out_path)):
            print("cannot write out file {}, path does not exist".format(out_path))
            return

        with open(os.path.join(out_path, 'compared-data.json'), 'w+') as f:
            f.write(json.dumps(self.data, indent=4))


def get_args():
    parser = argparse.ArgumentParser(description='compares timing data from collect_timings.py')
    parser.add_argument('--control', dest='control_data', required=True,
                        help='path to the control timing data')
    parser.add_argument('--compare', dest='compare_data', required=True,
                        help='path to the compare timing data')
    parser.add_argument('--include', dest='include_steps', nargs='+', default=[],
                        help='specify step(s) to be included in the report')
    parser.add_argument('--top-3', dest='top_3', action='store_true',
                        help='include top 3 slowest steps for both plays.')
    parser.add_argument('--intermediate', dest='intermediate', action='store_true',
                        help='save intermediate data to disk as json')
    parser.add_argument('--out_path', dest='out_path', default='./',
                        help='path to save intermediate data to')

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    with open(args.control_data, 'r') as pt:
        control_data = json.load(pt)
    with open(args.compare_data, 'r') as pt:
        compare_data = json.load(pt)

    ct = CompareTimings(control_data, compare_data,
                        control_name=os.path.basename(args.control_data),
                        compare_name=os.path.basename(args.compare_data),
                        normalize=True)
    ct.print_report(included_steps=args.include_steps, top_3=args.top_3)
    if args.intermediate:
        ct.save_data(args.out_path)
