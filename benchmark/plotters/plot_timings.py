#! /usr/bin/env python3

"""
    plot_timings.py
    given timings data from collect_timings.py, this will plot the data as a gantt chart and can
    save the chart to a PNG file
"""

import os
import argparse
import json
import random
import glob
import heapq

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors


class GanttChart:
    """ GanttChart
    Given a timings data json output from CollectTimings, this will generate a gantt chart of the
    processing times for each step in the timings data json file and can save this chart to a PNG.
    """
    def __init__(self, data, colors, normalize, title="", fig_size=(100, 10)):
        self._data = data
        self.colors = colors
        self._color_assignments = {}
        self.title = title
        self._normalize = normalize
        self._fig_size = fig_size
        self.fig, self.gnt = plt.subplots()

    def _set_up_plot(self, x_label, y_label, yticks, ylabels, start_time=None, end_time=None):
        """  set the plot's characteristics  """

        self.gnt.set_xlim(start_time, end_time)
        self.gnt.set_xlabel(x_label)
        self.gnt.set_ylabel(y_label)
        self.gnt.set_yticks([x * 5 for x in range(0, yticks)])
        self.gnt.set_yticklabels(ylabels)
        self.gnt.grid(True)

    def _generate_legend(self):
        plt.legend(handles=[mpatches.Patch(color=self._color_assignments[step], label=step)
                            for step in self._color_assignments],
                   bbox_to_anchor=(1.0005, 1),
                   loc='upper left',
                   borderaxespad=0.)

    def save_chart(self, out_path, dpi=None):
        self.save(os.path.join(out_path, 'timings', self.title), dpi)

    def save(self, out_path=None, dpi=None):
        """  save the chart as a png  """

        if out_path:
            out_path = os.path.join(out_path, self.title)

        self.fig.set_size_inches(self._fig_size)
        self.fig.savefig((out_path or self.title) + ".png",
                         dpi=(dpi or 'figure'),
                         bbox_inches='tight',
                         pad_inches=0)
        plt.close(self.fig)

    def _label_values(self, bars, y):
        """
        Attach a text label above each bar displaying its height
        """
        for start, duration in bars:
            if duration > 30:
                self.gnt.text(start + duration / 2., y + 2,
                              '%d' % int(duration),
                              ha='center', va='center')


class PlayGanttChart(GanttChart):
    def __init__(self, timings_data, colors, normalize=True,  title="", reverse=False,
                 fig_size=(100, 10)):
        GanttChart.__init__(self, timings_data, colors, normalize, title, fig_size)
        self._generate_chart(reverse)
        if not self.title:
            self.title = "play_chart"

    def _generate_chart(self, reverse):
        for path in self._data['paths']:
            rm_steps = []
            for i, step in enumerate(path['steps']):
                if not step.get('start', 0.0):
                    rm_steps.append(i)
                    print(f"bad step in {path['name']} : {step}")
            for step_indx in rm_steps:
                print(f"removing: step index {step_indx}")
                path['steps'].pop(step_indx)

        end_time = self._collect_and_sort_timing_data()
        self._set_up_plot('sec', 'path', len(self._data['paths']),
                          [path['name'] for path in self._data['paths']], end_time=end_time)
        self._generate_bars(reverse)
        self._generate_legend()

    def _collect_and_sort_timing_data(self):
        """  collect important time data and sort the steps by start time  """
        # sort each step within each path by start time
        self._data['paths'] = sorted(self._data['paths'], key=lambda p: min([s['start'] for s in p['steps']]))

        # get the lowest start time of all steps of the first path
        print("assuming path: {} is chronologically first".format(self._data['paths'][0]['name']))
        start_time = min(self._data['paths'][0]['steps'], key=lambda p: p['start'])['start']
        print("found start time: {}".format(start_time))
        if self._normalize:
            for path in self._data['paths']:
                normalize_start_times(path, start_time)
            print("normalized {} paths to start time: {}".format(
                len(self._data['paths']), start_time))

        # get the latest end time of all steps of all paths
        end_time = max(max(self._data['paths'],
                           key=lambda p: max([s['end'] for s in p['steps']]))['steps'],
                       key=lambda p: p['end'])['end']
        return end_time

    def _generate_bars(self, reverse):
        """  create the bars for each path's steps, apply to the plot, and create the legend  """

        c = 0
        for path in self._data['paths']:
            bars = []
            face_colors = []
            for step in sorted(path['steps'], key=lambda s: s['start'], reverse=reverse):
                if step['duration'] < 5:
                    continue

                if step['name'] not in self._color_assignments:
                    self._color_assignments[step['name']] = \
                        self.colors[len(self._color_assignments)]

                bars.append((step['start'], step['duration']))
                face_colors.append(self._color_assignments[step['name']])
            self.gnt.broken_barh(bars, (c, 5),
                                 facecolors=face_colors,
                                 edgecolors=mcolors.BASE_COLORS['k'],
                                 label=path['name'],
                                 alpha=0.5)
            self._label_values(bars, c)
            c += 5


class PathGanttChart(GanttChart):
    def __init__(self, path_data, colors, normalize, fig_size=(100, 10)):
        GanttChart.__init__(self, path_data, colors, normalize, path_data['name'], fig_size)
        self._generate_chart()

    def _generate_chart(self):
        start_time, end_time = self._collect_and_sort_timing_data()
        self._set_up_plot('sec', 'step', len(self._data['steps']),
                          [step['name'] for step in self._data['steps']],
                          start_time=start_time, end_time=end_time)
        self._color_assignments = {step['name']: self.colors[self._data['steps'].index(step)]
                                   for step in self._data['steps']}
        self._generate_bars()
        self._generate_legend()

    def _collect_and_sort_timing_data(self):
        """  collect important time data and sort the steps by start time  """
        self._data['steps'] = sorted(self._data['steps'], key=lambda p: p['start'])
        start_time = self._data['steps'][0]['start']
        end_time = max(self._data['steps'], key=lambda p: p['end'])['end']
        # sort each step within each path by start time
        return start_time, end_time

    def _generate_bars(self):
        c = 0
        for step in self._data['steps']:
            bars = [(step['start'], step['duration'])]
            self.gnt.broken_barh(
                bars,
                (c, 5),
                facecolor=self._color_assignments[step['name']],
                edgecolors=mcolors.BASE_COLORS['k'],
                label=step['name'])
            self._label_values(bars, c)
            c += 5


class SequenceGanttChart(GanttChart):
    def __init__(self, path_data, colors, normalize, fig_size=(100, 10)):
        GanttChart.__init__(self, path_data, colors, normalize, path_data['name'] + '-seq',
                            fig_size)
        self._generate_chart()

    def _generate_chart(self):
        start_time, end_time = self._collect_and_sort_timing_data()
        self._set_up_plot('sec', 'sequence', len(self._data['sequences']),
                          [seq['name'] for seq in self._data['sequences']],
                          start_time=start_time, end_time=end_time)
        self._color_assignments = {step['name']: self.colors[index]
                                   for index, step in
                                   enumerate(self._data['sequences'][0]['steps'])}
        self._generate_bars()
        self._generate_legend()

    def _collect_and_sort_timing_data(self):
        """  collect important time data and sort the sequences by start time  """
        self._data['sequences'] = sorted(self._data['sequences'], key=lambda p: p['name'])
        start_time = min([s['start'] for s in self._data['sequences'][0]['steps']])
        end_time = max([s['start'] + s['duration'] for s in self._data['sequences'][-1]['steps']])
        return start_time, end_time

    def _generate_bars(self):
        c = 0
        for seq in self._data['sequences']:
            bars = []
            face_colors = []
            for step in sorted(seq['steps'], key=lambda s: s['start']):
                if step['name'] not in self._color_assignments:
                    self._color_assignments[step['name']] = \
                        self.colors[len(self._color_assignments)]

                bars.append((step['start'], step['duration']))
                face_colors.append(self._color_assignments[step['name']])
            self.gnt.broken_barh(bars, (c, 5),
                                 facecolors=face_colors,
                                 edgecolors=mcolors.BASE_COLORS['k'],
                                 label=seq['name'],
                                 alpha=0.5)
            self._label_values(bars, c)
            c += 5


def generate_colors():
    """  generate 50 random, unique colors to represent each step  """
    num_colors = 30
    random.seed(42)
    cm = plt.cm.get_cmap('hsv', num_colors)
    colors = [cm(x) for x in range(num_colors)]
    return colors


def normalize_start_times(path_data, start_time):
    for step in path_data['steps']:
        step['start'] = step['start'] - start_time
        step['end'] = step['start'] + step['duration']


def set_up(timing_path):
    with open(timing_path, 'r') as pt:
        timings_data = json.load(pt)
    colors = generate_colors()
    return timings_data, colors


def generate_charts(timing_path,
                    out_path,
                    title="",
                    path=False,
                    sequence=False,
                    reverse=False,
                    normalize=True,
                    dpi='figure'):
    if out_path:
        os.makedirs(out_path, exist_ok=True)

    if path or sequence:
        os.makedirs(os.path.join(out_path, 'path_charts'), exist_ok=True)
        for f in glob.glob(os.path.join(out_path, 'path_charts/*.png')):
            os.unlink(f)

    timings_data, colors = set_up(timing_path)

    title = title + "_" + timings_data['title'] if title else timings_data['title']

    play_gc = PlayGanttChart(timings_data, colors, normalize, title, reverse)
    play_gc.save(out_path, dpi)

    if path:
        for path_data in timings_data['paths']:
            path_gc = PathGanttChart(path_data, colors, normalize)
            path_gc.save(os.path.join(out_path, 'path_charts'), dpi)

    if sequence:
        for path_data in timings_data['paths']:
            seq_gc = PathGanttChart(path_data, colors, normalize, (200, 10))
            seq_gc.save(os.path.join(out_path, 'path_charts'), dpi)


def get_args():
    parser = argparse.ArgumentParser(
        description='plots processing times to a gantt chart and prints to a PNG file')
    parser.add_argument('timings_path')
    parser.add_argument('--dpi', dest='dpi', default=0, type=int,
                        help='set the dpi for the image, anything (0, 300) recommended.')
    parser.add_argument('--reverse', dest='reverse', action='store_true',
                        help='reverse the order in which the steps are plotted')
    parser.add_argument('--path', dest='path', action='store_true',
                        help='print a plot for each path as well.')
    parser.add_argument('--sequence', dest='sequence', action='store_true',
                        help="print a plot for each path's sequences as well.")
    parser.add_argument('-o', '--out-path', dest='out_path', default="",
                        help='specify path to output pngs to.')
    parser.add_argument('-t', '--title', dest='title', default="",
                        help='specify a title to be prepended to all png names.')

    return parser.parse_args()


def main():
    args = get_args()
    dpi = 'figure'
    if args.dpi:
        dpi = args.dpi

    if os.path.isdir(args.timings_path):
        for timing_json in glob.glob(os.path.join(args.timings_path, "*.json")):
            title = '.'.join(os.path.basename(timing_json).split('.')[:-1])
            if args.title:
                title = args.title + '_' + title

            generate_charts(timing_json, args.out_path, title, args.path, args.sequence,
                            args.reverse, True, dpi)
    else:
        generate_charts(args.timings_path, args.out_path, args.title, args.path, args.sequence,
                        args.reverse, True, dpi)


if __name__ == "__main__":
    main()
