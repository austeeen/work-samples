#!/usr/bin/python3

"""
UPDATE: 2/25/20
    PRIVATE
-----------------------------------------------------------------
UPDATE: 11/24/20
    PRIVATE
-----------------------------------------------------------------
"""

import os
import json
import argparse
import subprocess
import manual_configuration
import traceback

from configuration import Configuration


def parse_args():
    parser = argparse.ArgumentParser(description="Run a test suite")
    parser.add_argument("--config", help="path to a configuration .json file for auto test "
                                         "configuration",
                        type=str, default="")
    parser.add_argument("--PRIVATE")

    return parser.parse_args()


def run_tests():
    argv = parse_args()
    args = vars(argv)

    if args['config']:
        # PRIVATE
    else:
        # PRIVATE


if __name__ == "__main__":
    run_tests()
