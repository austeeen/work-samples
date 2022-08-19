"""
    plot_pid.py
"""
import re
import os
import json
import argparse
import pandas as pd


def vsz_rss_plot(pid_df) -> 'pd.DataFrame.axes':
    return pid_df.groupby('Time').aggregate({'VSZ': 'sum', 'RSS': 'sum'}).resample(
        '10S').mean().plot.area(figsize=(30, 15))


def mem_line_plot(pid_df) -> 'pd.DataFrame.axes':
    return pid_df.groupby(['Time', 'Name']).aggregate({'%MEM': 'sum'}).unstack().resample(
        '10S').mean().plot.line(figsize=(30, 10), sharey=True, subplots=True)[0]


def mem_stacked_plot(pid_df) -> 'pd.DataFrame.axes':
    return pid_df.groupby(['Time', 'Name']).aggregate({'%MEM': 'sum'}).unstack().resample(
        '10S').mean().plot.area(figsize=(30, 15))


def usr_sys_plot(pid_df) -> 'pd.DataFrame.axes':
    return pid_df.groupby('Time').aggregate({'%system': 'sum', '%usr': 'sum'}).resample(
        '10S').mean().plot.area(figsize=(30, 15))


def cpu_line_plot(pid_df) -> 'pd.DataFrame.axes':
    return pid_df.groupby(['Time', 'Name']).aggregate({'%CPU': 'sum'}).unstack().resample(
        '10S').mean().plot.line(figsize=(30, 10), sharey=True, subplots=True)[0]


def cpu_stacked_plot(pid_df) -> 'pd.DataFrame.axes':
    return pid_df.groupby(['Time', 'Name']).aggregate({'%CPU': 'sum'}).unstack().resample(
        '10S').mean().plot.area(figsize=(30, 15))


PLOT_TABLE = {
    'vsz_rss': vsz_rss_plot,
    'mem_line': mem_line_plot,
    'mem_stacked': mem_stacked_plot,
    'usr_sys': usr_sys_plot,
    'cpu_line': cpu_line_plot,
    'cpu_stacked': cpu_stacked_plot,
}


def load_pid(pid_fp) -> 'pd.DataFrame':
    with open(pid_fp) as f:
        f.readline()
        f.readline()
        columns = f.readline().strip('#').split()
        num_columns = len(columns)
        df = pd.DataFrame.from_records(
            [row.split(maxsplit=num_columns - 1) for row in f if row[0] == ' '], columns=columns)

    numcols = df.columns.drop('Command')
    df[numcols] = df[numcols].apply(pd.to_numeric, errors='coerce')

    # convert virtual/resident mem values from KB to GB
    df['VSZ'] = df['VSZ'].apply(lambda v: v / 1000000)
    df['RSS'] = df['RSS'].apply(lambda v: v / 1000000)
    return df


def align_to_timings(pid_df, timing_data) -> 'pd.DataFrame':
    eop = max(
        [s['start'] + s['duration'] for path in timing_data['paths'] for s in path['steps']])
    pid_df = pid_df.loc[pid_df.Time < eop].copy()
    pid_df['Time'] = pd.to_datetime(pid_df['Time'], unit='s')
    pid_df = pid_df.set_index('Time')
    return pid_df


def normalize_times(times):
    start_time = times[0]
    return [(t - start_time) for t in times]


def map_names(pid_df):
    def map_name(name):
        for r, v in command_names:
            if r.match(name):
                return v
        return 'other'

    command_names = [
        [re.compile(r'PRIVATE.*PRIVATE'), 'PRIVATE'],
        [re.compile(r'PRIVATE.*PRIVATE'), 'PRIVATE'],
        [re.compile(r'PRIVATE'), 'PRIVATE'],
        [re.compile(r'PRIVATE'), 'PRIVATE'],
        [re.compile(r'PRIVATE'), 'PRIVATE'],
        [re.compile(r'PRIVATE'), 'PRIVATE'],
        [re.compile(r'PRIVATE'), 'PRIVATE'],
        [re.compile(r'PRIVATE'), 'PRIVATE'],
        [re.compile(r'PRIVATE'), 'PRIVATE'],
        [re.compile(r'PRIVATE'), 'PRIVATE'],
        [re.compile(r'[./]?pidstat'), 'pidstat'],
        [re.compile(r'.*run_test.py'), 'run_test'],
        [re.compile(r'PRIVATE'), 'PRIVATE'],
    ]
    pid_df['Name'] = pid_df['Command'].map(map_name)


def save_plot(ax, out_fp):
    print("saving: " + out_fp)
    ax.get_figure().savefig(out_fp)


def plot_pid(plots, pid_path, timings_path, title="", out_path=""):
    if out_path:
        os.makedirs(out_path, exist_ok=True)

    with open(timings_path) as f:
        timing_data = json.load(f)

    pid_df = align_to_timings(load_pid(pid_path), timing_data)
    map_names(pid_df)

    if title:
        title += "_"

    for plt_name, plt_func in plots.items():
        save_plot(plt_func(pid_df), os.path.join(out_path, "{}{}.png".format(title, plt_name)))


def get_plots(args):
    if not isinstance(args, dict):
        vargs = vars(args)
    else:
        vargs = args
    return {
        plt_name: plt_func for plt_name, plt_func in PLOT_TABLE.items()
        if not vargs.get('skip_' + plt_name)
    }


def get_args():
    parser = argparse.ArgumentParser(
        description='plots PID times to various charts as PNG files')
    parser.add_argument('pid_path', help='path to the PID times file')
    parser.add_argument('timings_path', help='path to the timings json file')
    parser.add_argument('--skip-usr-sys', action='store_true', help='skip %usr vs %sys stack plot')
    parser.add_argument('--skip-cpu-line', action='store_true', help='skip %CPU line plot.')
    parser.add_argument('--skip-mem-line', action='store_true', help='skip %MEM line plot.')
    parser.add_argument('--skip-cpu-stacked', action='store_true', help='skip %CPU stack plot.')
    parser.add_argument('--skip-mem-stacked', action='store_true', help='skip %MEM stack plot.')
    parser.add_argument('--skip-vsz-rss', action='store_true',
                        help='skip virtual + resident memory stack plot')
    parser.add_argument('-o', '--out-path', default="./", help='specify path to output pngs to.')
    parser.add_argument('-t', '--title', default="", help='prepend title to all chart filenames')

    return parser.parse_args()


def main():
    args = get_args()
    plot_pid(get_plots(args), args.pid_path, args.timings_path, args.title, args.out_path)


if __name__ == "__main__":
    main()
