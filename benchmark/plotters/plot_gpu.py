""" nvidia-smi plot

Plot data captured using nvidia-smi

Leslie Hensley
Ryan Baltenberger
Austin Herman
Badger Technologies LLC
"""

import os
import sys
import json
import argparse

import pandas as pd


def parse_args(args):
    """ parse arguments

    Parse the passed in arguments

    Args:
        args (list): input list of arguments to parse

    Returns:
        args: parsed arguments and the values associated with them
    """

    parser = argparse.ArgumentParser(description='plot nvidia-smi data')
    parser.add_argument('csv_path', help='path to csv of nvidia-smi data', type=str)
    parser.add_argument('--timings_path', help='path to the timings json file')
    parser.add_argument('--mean_window', help='size of gpu mean window', type=int, default=1200)
    parser.add_argument('-o', '--out-path', dest='out_path', default="",
                        help='specify path to output files to')
    return parser.parse_args(args)


def end_of_play(json_path):
    """ find the end of the play for trimming nvidia-smi data """
    with open(json_path) as file_in:
        j = json.load(file_in)
        return max([s['start'] + s['duration'] for path in j['paths'] for s in path['steps']])


def load_nvidia_smi(nvidia_smi_path):
    """ load the nvidia-smi data """
    with open(nvidia_smi_path) as file_in:
        columns = file_in.readline().replace(' ', '').strip('\n').split(',')
        num_columns = len(columns)
        dataframe = pd.DataFrame.from_records(
            [l.replace('%', '').replace('MiB', '').split(',', maxsplit=num_columns - 1)
             for l in file_in if l[0] == '2'],
            columns=columns
        )
        return dataframe


def nvidia_smi_to_dataframe(nvidia_smi_path, json_path):
    """ convert loaded nvidia-smi data into a pandas dataframe """
    dataframe = load_nvidia_smi(nvidia_smi_path)

    numcols = dataframe.columns.drop(['pstate']).drop(['timestamp'])
    dataframe[numcols] = dataframe[numcols].apply(pd.to_numeric, errors='coerce')
    dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'], format='%Y/%m/%d %H:%M:%S.%f')
    if json_path:
        eop = pd.to_datetime(end_of_play(json_path), unit='s') - pd.Timedelta('04:00:00')
        dataframe = dataframe.loc[dataframe['timestamp'] < eop].copy()

    dataframe = dataframe.set_index('timestamp')
    dataframe = dataframe.drop(columns=['pstate'])

    return dataframe


def plot_gpu(csv_path, timings_path, mean_window, out_path=""):
    """ plot nvidia-smi gpu data """
    fix_dataframe = nvidia_smi_to_dataframe(csv_path, timings_path)
    fix_dataframe['utilization.gpu[%].mean'] = \
        fix_dataframe['utilization.gpu[%]'].rolling(mean_window).mean()
    fig_list = fix_dataframe.plot.line(figsize=(30, 15), subplots=True)

    plot_name = '.'.join(os.path.basename(csv_path).split('.')[:-1]) + ".png"
    if out_path:
        os.makedirs(out_path, exist_ok=True)
        plot_name = os.path.join(out_path, plot_name)
    print("saving: " + plot_name)
    fig_list[0].get_figure().savefig(plot_name)


def plot(argv):
    """ plot nvidia-smi gpu data """
    args = vars(parse_args(argv))
    plot_gpu(args['csv_path'], args['timings_path'], args['mean_window'], args['out_path'])


if __name__ == '__main__':
    plot(sys.argv[1:])
