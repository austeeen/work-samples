"""
    plot_pid.py
"""
import re
import os
import json
import argparse
import pandas as pd
import matplotlib.pyplot as plt


def map_hosts(df):
    def map_name(name):
        for r, v in command_names:
            if r.match(name):
                return v
        return 'other'

    command_names = [
        [re.compile(r'work.*PRIVATE'), 'work <=> gateway'],
        [re.compile(r'work.*PRIVATE*'), 'work <=> CDN AWS'],
        [re.compile(r'work.*PRIVATE*'), 'work <=> CDN AWS'],
        [re.compile(r'work.*PRIVATE*'), 'work <=> CDN Akama'],
        [re.compile(r'work.*PRIVATE*'), 'work <=> CDN Akama'],
    ]
    df['Host <=> Host'] = df['Host <=> Host'].map(map_name)


def save_plot(ax, out_fp):
    print("saving: " + out_fp)
    ax.get_figure().savefig(out_fp)


def csv_to_df(csv_fp):
    with open(csv_fp) as bw_csv:
        columns = bw_csv.readline().strip('\n').split(',')
        rows = [ln.strip('\n').split(",") for ln in bw_csv.readlines()]
        df = pd.DataFrame.from_records(rows, columns=columns)
    df[["sec", "sent", "recv", "total"]] = df[["sec", "sent", "recv", "total"]].apply(pd.to_numeric)
    df = df.set_index('sec')
    return df


def plot_bandwidth(bw_csv_path, out_path=""):
    if out_path:
        os.makedirs(out_path, exist_ok=True)

    df = csv_to_df(bw_csv_path)
    map_hosts(df)
    fig, ax = plt.subplots(figsize=(15, 10))
    # save_plot(df.groupby(['sec', 'Host <=> Host']).sum()['total'].unstack().plot(ax=ax), "test.png")
    save_plot(df.groupby(['sec', 'Host <=> Host']).sum()['total'].unstack().plot.area(ax=ax, figsize=(50, 20)), "bandwidth_area.png")
    # save_plot(df.plot.line(y=["sent", "recv"]), "bandwidth_in_out.png")
    # save_plot(df.plot.line(y=["total"]), "bandwidth_total.png")
    # save_plot(df.plot.area(stacked=False, figsize=(50, 20), xlabel="sec", ylabel="Bytes"), "bandwidth_stacked.png")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('bandwidth_csv', type=str)

    return parser.parse_args()


def main():
    args = get_args()
    plot_bandwidth(args.bandwidth_csv)


if __name__ == "__main__":
    main()
