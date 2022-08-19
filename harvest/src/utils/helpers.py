import re
import os
import sys
import json
import time
import errno
from datetime import datetime
from dateutil.relativedelta import relativedelta


def mkdir_s(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def warn_user(warn, no_prompt=False):
    print(f"[WARNING]: {warn}")
    if not no_prompt:
        input("Press any key to continue or ctrl-c to exit. Use --force-yes to disable these "
              "prompts.")


def check_boto3(required=True):
    try:
        import boto3
    except ImportError:
        if required:
            print('[ERROR] User does not have boto3 python lib installed. S3 functionality is not '
                  'available. Please install with `pip3 install boto3` and try again.')
            sys.exit(1)
        return False
    return True


def print_wait_message(what, timeout, start):
    """ if the elapsed wait time is less than 20% of the set timeout, start printing messages.
        this should help reduce the volume of messages spammed to the user. """
    delta_time = round((timeout + start) - time.time())
    if delta_time < round(timeout * .2, 2):
        print(f"{what}... quitting in {delta_time} seconds")


def set_fleet_path(PRIVATE):
    # PRIVATE
    return PRIVATE


def date_from_str(str_date):
    return datetime.strptime(str_date, "%Y%m%d")


def datetime_from_str(str_date):
    return datetime.strptime(str_date, '%Y%m%d %H:%M')


def date_from_play_id(play_id):
    return date_from_str(re.search(r'(\d{8})+', play_id).group(0))


def rdelta_from_arg(past):
    if 'years' in past[1]:
        return relativedelta(years=int(past[0]))
    elif 'months' in past[1]:
        return relativedelta(months=int(past[0]))
    elif 'weeks' in past[1]:
        return relativedelta(weeks=int(past[0]))
    elif 'days' in past[1]:
        return relativedelta(days=int(past[0]))

    raise Exception(f"{past} is not a valid delta parameter.")
