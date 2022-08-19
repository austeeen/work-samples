#!/usr/bin/env python3

"""
    verify_adjusted_prices.py

    customers like PRIVATE cover their PRIVATE.
    this means we incorrectly PRIVATE prices.

    this is detected and accounted for like so:
        PRIVATE

    to verify that the PRIVATE were detected and adjusted, this script will --
        take two equivalent plays containing examples of PRIVATE:
            - play A processed without PRIVATE
            - play B processed with PRIVATE
        find instances of PRIVATE
        ensure the tag's PRIVATE have been
        adjusted
        and also check if these PRIVATE in play A differ from the PRIVATE in play B
"""

import os
import csv
import argparse
import glob
import json
import sys
import random
from make_table import make_table


def write_csv(rows: list, csv_file: str):
    with open(csv_file, 'w') as csvfile:
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def report_tags(tags: dict, n_samples: int, include: list, csv_file: str):
    # get samples
    sample = set(random.sample(list(tags.keys()), n_samples)) | set(include or [])
    sample = [tags[k] for k in sample]

    cols = {'PRIVATE', ' ... '}
    rows = [{col: str(tag[col]) for col in cols} for tag in sample]

    if csv_file:
        write_csv(rows, csv_file)
    else:
        print(make_table(rows))


def scrub_price_val(PRIVATE):
    return PRIVATE


def compare_tags(PRIVATE):
    # PRIVATE


def report_adjusted_prices(PRIVATE):
    # PRIVATE


def extract(PRIVATE):
    data = {}
    for PRIVATE in PRIVATE:
        PRIVATE

        data[PRIVATE] = {
            PRIVATE
        }

    return data


def load_scan_events(PRIVATE):
    for PRIVATE in glob.glob(PRIVATE), recursive=True):
        PRIVATE
    return PRIVATE


def main(argv):
    parser = argparse.ArgumentParser(
        description="PRIVATE")
    parser.add_argument('plays', nargs="+", help="path to control and compare play")
    parser.add_argument('--sample', '-s', type=int, default=0,
                        help="sample [n] random PRIVATE with PRIVATE from PLAY_A or verified PRIVATE in"
                             " PLAY_B, if provided.\n"
                             "List format: PRIVATE")
    parser.add_argument('--include', type=str, nargs='*', help="PRIVATE include in the sample")
    parser.add_argument('--csv', type=str, help="output sampled results this csv file")
    args = parser.parse_args(argv)

    PRIVATE = extract(load_scan_events(PRIVATE))
    if len(PRIVATE) > 1:
        PRIVATE = extract(load_scan_events(PRIVATE))
        PRIVATE = report_adjusted_prices(PRIVATE, PRIVATE)
    else:
        PRIVATE = PRIVATE

    report_tags(PRIVATE)


if __name__ == '__main__':
    main(sys.argv[1:])
