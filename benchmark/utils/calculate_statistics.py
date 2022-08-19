import argparse
import json
import math


def variance(d, mean):
    return sum(pow((num - mean), 2) for num in d) / len(d)


def get_stats(data_set):
    stats = {}

    for path in data_set[0]:
        stats[path] = {}
        for step in data_set[0][path]:
            d = [data[path][step]['duration'] for data in data_set]
            mean = sum(d) / len(d)
            var = variance(d, mean)
            std_dev = math.sqrt(var)

            stats[path][step] = {
                'mean': mean,
                'min': min(d),
                'max': max(d),
                'var': var,
                'std-dev': std_dev
            }

    return stats


def reformat_data(data_set):
    new_set = {}
    for path in data_set['paths']:
        new_set[path['name']] = {}
        for step in path['steps']:
            new_set[path['name']][step['name']] = step

    return new_set


def open_json(path):
    with open(path, 'r') as fd:
        return json.load(fd)


def save_json(data, out_name):
    with open(out_name, 'w+') as f:
        json.dump(data, f, indent=4)


def get_args():
    parser = argparse.ArgumentParser(description='calculates statistics on the given timings.json '
                                                 'data sets')
    parser.add_argument('--timings', dest='timing_list', nargs='+', default=[], required=True,
                        help='paths to timing jsons to be used')
    parser.add_argument('-o', '--out-name', dest='out_name', required=True,
                        help='required name of file.')

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    data_set = [reformat_data(open_json(path)) for path in args.timing_list]

    save_json(get_stats(data_set), args.out_name)
