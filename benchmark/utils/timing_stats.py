import pandas as pd
import sys
import json
import argparse

from reformat_stats import reformat


def get_df(timing_data):
    return pd.concat({
        k: pd.DataFrame.from_dict(v, 'index') for k, v in timing_data.items()
    }, axis=0)


def get_args(args):
    parser = argparse.ArgumentParser(description='reports processing time data output from '
                                                 'gather_timings.py')
    parser.add_argument('timings_path')
    return parser.parse_args(args)


def main(args):
    args = get_args(args)
    with open(args.timings_path, 'r') as pt:
        timing_data = json.load(pt)

    data = reformat(timing_data)
    df = get_df(data)
    df.index.names = ['path', 'step']
    un = df.unstack()
    # step by average duration per path
    un['duration'].mean()
    # [count, mean, std, min, 25%, 50%, 75%, max] per step for step duration per path
    un['duration'].describe()


if __name__ == "__main__":
    main(sys.argv[1:])


