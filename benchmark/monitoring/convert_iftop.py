#!/usr/bin/env python3

import csv
import os
import re
import argparse
import pathlib
from heapq import heappush, heappop
from collections import defaultdict, namedtuple
from typing import List, Dict, Sequence, Set


class IfTopParser:
    header = ["sec", "Host <=> Host", "sent", "recv", "total"]
    dir_in = "<="
    dir_out = "=>"
    dir_both = " <=> "

    def __init__(self):
        self.all_tables = []
        self.cur_table = []
        self.parser_fun = None
        self.sequence = [self.get_header, self.get_sep, self.capture_lines]
        self.header = IfTopParser.header

    def parse(self, iftop_log_file):
        log_file = open(iftop_log_file, 'r')
        seq_indx = 0
        self.parser_fun = self.sequence[seq_indx]
        for line in log_file:
            if not line.strip():
                continue

            if self.parser_fun(line.strip()):
                seq_indx = (seq_indx + 1) % len(self.sequence)
                self.parser_fun = self.sequence[seq_indx]

    def print_lines(self):
        print(",".join(self.header))
        for i, tbl in enumerate(self.all_tables):
            sec = (i + 1) * 2
            for row in tbl:
                print(str(sec) + "," + ",".join([str(cl) for cl in row]))

    def get_header(self, line: str):
        if line[0] == "#":
            self.cur_table.clear()
            return True
        return False

    def get_sep(self, line: str):
        return all(c == '-' for c in line[:-1])

    def capture_lines(self, line: str):
        if all(c == '-' for c in line[:-1]):
            try:
                self.end_cur_table()
            except Exception as e:
                print(self.cur_table)
                raise e
            return True
        ln = line.split()
        if ln[2] == IfTopParser.dir_out:
            self.cur_table.append(ln[1:])
        else:
            self.cur_table.append(ln)
        return False

    def end_cur_table(self):
        def pairwise(iterable):
            a = iter(iterable)
            return zip(a, a)

        def as_float(byte_str: str):
            if byte_str[-2] == "M":
                return float(byte_str[:-2]) * 6
            if byte_str[-2] == "K":
                return float(byte_str[:-2]) * 3
            return float(byte_str[:-1])

        new_tbl = []
        for out_dir, in_dir in pairwise(self.cur_table):
            sent = as_float(out_dir[2])
            recv = as_float(in_dir[2])
            new_tbl.append([out_dir[0] + self.dir_both + in_dir[0], sent, recv, sent + recv])

        self.all_tables.append(new_tbl)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('network_fp', type=str)

    return parser.parse_args()


def main():
    args = get_args()
    p = IfTopParser()
    p.parse(args.network_fp)
    p.print_lines()


if __name__ == "__main__":
    main()
