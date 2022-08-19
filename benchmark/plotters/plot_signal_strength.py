"""
    plot_pid.py
"""
import re
import os
import json
import argparse
import pandas as pd

from plot_timings import PlayGanttChart, set_up


def net_timings_twin_plot(net_df, gant_chart: 'PlayGanttChart', title):
    fig = gant_chart.fig
    gnt_ax = gant_chart.gnt

    color = 'tab:blue'
    net_ax = gnt_ax.twinx()
    net_ax.set_ylabel('Network Strength (%)', color=color)
    net_ax.plot(net_df['Time (s)'].to_numpy(), net_df['SIGNAL STRENGTH'].to_numpy(), color=color)
    net_ax.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()
    fig.set_size_inches((100, 10))
    fig.savefig(title + "-network_strength.png", bbox_inches='tight', pad_inches=0)


def net_strength_line(net_df) -> 'pd.DataFrame.axes':
    net_df = net_df.set_index('Time (s)')
    ax = net_df.plot.line(y='SIGNAL STRENGTH', figsize=(30, 15))
    return ax


def save_plot(ax, out_fp):
    print("saving: " + out_fp)
    fig = ax.get_figure()
    fig.tight_layout()
    fig.set_size_inches((100, 10))
    fig.savefig(out_fp, bbox_inches='tight', pad_inches=0)


def load_csv(csv_path):
    with open(csv_path) as file_in:
        columns = file_in.readline().strip('\n').split(',')
        df = pd.DataFrame.from_records([ln.split(',') for ln in file_in], columns=columns)
    df['Time (s)'] = pd.to_numeric(df['Time (s)'])
    df['SIGNAL STRENGTH'] = pd.to_numeric(df['SIGNAL STRENGTH'])
    return df


def plot_network_strength(net_path, timing_path="", out_path=""):
    if out_path:
        os.makedirs(out_path, exist_ok=True)

    df = load_csv(net_path)

    if not timing_path:
        save_plot(net_strength_line(df), os.path.join(out_path, "network_strength.png"))
    else:
        timings_data, colors = set_up(timing_path)
        if not timings_data['title']:
            timings_data['title'] = "no-title"
        play_gc = PlayGanttChart(timings_data, colors, timings_data['title'])
        net_timings_twin_plot(df, play_gc, timings_data['title'])


def get_args():
    parser = argparse.ArgumentParser(
        description='plots network signal strength over time')
    parser.add_argument('net_path', help='network strength csv file')
    parser.add_argument('--timings', default="", help='timings json file')
    parser.add_argument('-o', '--out-path', default="./", help='specify path to output pngs to.')
    return parser.parse_args()


def main():
    args = get_args()
    plot_network_strength(args.net_path, args.timings, args.out_path)


if __name__ == "__main__":
    main()
