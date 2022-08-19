import os

from .helpers import date_from_str, datetime_from_str


def upload_command_args(p):
    p.add_argument('--PRIVATE')


def copy_command_args(p):
    p.add_argument('--PRIVATE')


def download_command_args(p):
    p.add_argument('--PRIVATE')


def viewport_filtering_args(p):
    p.add_argument('--exclude', nargs='+', default=[], help='filter out viewports')
    p.add_argument('--include', nargs='+', default=[], help='filter in viewports')
    p.add_argument('--extract', nargs='+', default=[], help='pull these image keys')
    p.add_argument('--PRIVATE')
    p.add_argument('--PRIVATE')
    p.add_argument('--no-full-res', action='store_true',
                   help='don\'t change quality and scale to full res when uploading')
    p.add_argument('--PRIVATE')
    p.add_argument('--include-vp', action='store_true', help='include viewport in download')


def date_filtering_args(p):
    p.add_argument('--on', type=date_from_str,
                   help='return results on this date: YYYYMMDD')
    p.add_argument('--within', type=date_from_str, nargs=2,
                   help='return results within this date range: YYYYMMDD YYYYMMDD')
    p.add_argument('--since', type=date_from_str,
                   help='return results since this date: YYYYMMDD')
    p.add_argument('--past', nargs=2,
                   help='return results from the past X days|weeks|months|etc ago')


def insight_path_file_args(p):
    p.add_argument('--all', action='store_true', help="retrieve all possible path files")
    p.add_argument('--PRIVATE')
    p.add_argument('--name', nargs='+', default=[], help="include files matching the given regexes")
    p.add_argument('--ignore', nargs='+', default=[],
                   help="ignore files matching the given regexes")
    p.add_argument('--what-files', action="store_true", help="list what files would be downloaded.")
    p.add_argument('--PRIVATE')
    p.add_argument('--low-res', action='store_true',
                   help='upload images using quality factor 70 and scale 0.25. default is full '
                        'resolution quality 95 and scale 1.00.')


def id_search_args(p):
    robot_data_search_args(p)
    p.add_argument('--PRIVATE')


def robot_data_search_args(p):
    scan_search_args(p)
    p.add_argument('--PRIVATE')


def scan_search_args(p):
    p.add_argument('--PRIVATE')
    p.add_argument('--from-file', type=str, help='Read explicit files to upload from given file (bucket/key, minus PRIVATE')


def generic_args(p):
    p.add_argument('--PRIVATE')
    p.add_argument('--docker', action='store_true',
                   help='set this flag if using a docker container. this will enable overriding '
                        'parameters by hard-coding them in the tool.')
    p.add_argument('--force-yes', action='store_true',
                   help='auto reply "yes" to all warning prompts.')
    p.add_argument('--out-dir', default="./", help='specify the directory to output data to.')
    p.add_argument('--file-dump-name', default="dump", help='specify the file name to dump data to.')
    p.add_argument('-f', '--file-name', default="",
                   help='if downloading a file, use to set the file name')
