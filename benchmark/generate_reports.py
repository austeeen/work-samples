#!/usr/bin/env python3
import os
import sys
import argparse
from plotters.plot_timings import generate_charts
from plotters.plot_pid import plot_pid, get_plots
from plotters.plot_gpu import plot_gpu
from timing.report_timings import report_timings


def get_files(path_to_dir):
    paths = {}
    for file_name in os.listdir(path_to_dir):
        if file_name == "timings.json":
            paths['timings'] = os.path.join(path_to_dir, file_name)
        elif file_name == "cpu_pid.txt":
            paths['pid'] = os.path.join(path_to_dir, file_name)
        elif file_name == "gpu_stats.csv":
            paths['gpu'] = os.path.join(path_to_dir, file_name)
    return paths


def main(args):
    if args.out_path:
        os.makedirs(args.out_path, exist_ok=True)
        out_path = args.out_path
    else:
        out_path = args.dir
    paths = get_files(args.dir)
    if 'timings' in paths:
        report_timings(paths['timings'], args.title, args.no_normalize, args.print_out, out_path)
        generate_charts(paths['timings'], args.title, os.path.join(out_path, 'timing_charts'),
                        args.path, args.sequence, args.reverse, True)
    if 'pid' in paths and 'timings' in paths:
        plot_pid(get_plots(args),
                 paths['pid'],
                 paths['timings'],
                 args.title,
                 os.path.join(out_path, 'pid_charts'))

    if 'gpu' in paths:
        plot_gpu(paths['gpu'], paths.get('timings', ""), args.mean_window,
                 os.path.join(out_path, 'gpu_charts'))


def get_args(argv):
    parser = argparse.ArgumentParser(
        description='provide a directory with benchmark files and generate reports/plots')
    parser.add_argument('dir', help='path to the directory containing the benchmark files, can'
                                    'be multiple benchmark directories')
    parser.add_argument('-o', '--out-path', dest='out_path', default="",
                        help='specify path to output files to')
    parser.add_argument('-c', '--clear-dest', dest='clear_dest', action='store_true',
                        help='clear all files/dirs within out-path, if specified. ')
    parser.add_argument('-t', '--title', dest='title', default="",
                        help='specify a title to be prepended to all file names.')
    # REPORT TIMINGS
    parser.add_argument('--no-normalize', dest='no_normalize', action='store_true',
                        help='data set does not need to be normalized (data made relative to the '
                             'lowest timestamp')
    parser.add_argument('-p', '--print', dest='print_out', action='store_true',
                        help='print report to stdout')
    # PLOT TIMINGS
    parser.add_argument('--dpi', dest='dpi', type=int,
                        help='set the dpi for the image, anything (0, 300) recommended')
    parser.add_argument('--reverse', dest='reverse', action='store_true',
                        help='reverse the order in which the steps are plotted')
    parser.add_argument('--path', dest='path', action='store_true', default=True,
                        help='print a plot for each path')
    parser.add_argument('--sequence', dest='sequence', action='store_true',
                        help="print a plot for each path's sequences")
    # PLOT PID
    parser.add_argument('--skip-usr-sys', action='store_true', help='skip %usr vs %sys stack plot')
    parser.add_argument('--skip-cpu-line', action='store_true', help='skip %CPU line plot.')
    parser.add_argument('--skip-mem-line', action='store_true', help='skip %MEM line plot.')
    parser.add_argument('--skip-cpu-stacked', action='store_true', help='skip %CPU stack plot.')
    parser.add_argument('--skip-mem-stacked', action='store_true', help='skip %MEM stack plot.')
    parser.add_argument('--skip-vsz-rss', action='store_true',
                        help='skip virtual + resident memory stack plot')
    # PLOT GPU
    parser.add_argument('--mean_window', help='size of gpu mean window', type=int, default=1200)

    return parser.parse_args(argv)


if __name__ == "__main__":
    main(get_args(sys.argv[1:]))
