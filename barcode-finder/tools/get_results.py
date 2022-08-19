#!/bin/env python3

import sys
import json


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("no result json given")

    resfp = sys.argv[1]

    res_data = json.load(open(resfp, 'r'))

    total_images = 0
    total_barcodes = 0
    no_barcodes = 0
    only_one_barcode = 0
    atl_one_barcode = 0
    mrt_one_barcode = 0

    for result in res_data["results"]:
        total_images += 1
        if not result["barcodes"]:
            no_barcodes += 1
            continue
        c = len(result["barcodes"])
        total_barcodes += c
        atl_one_barcode += 1
        if c == 1:
            only_one_barcode += 1
        if c > 1:
            mrt_one_barcode += 1

    print("total images    {}".format(total_images))
    print("total barcodes  {}".format(total_barcodes))
    print("no barcodes     {}".format(no_barcodes))
    print("# barcodes == 1 {}".format(only_one_barcode))
    print("# barcodes >= 1 {}".format(atl_one_barcode))
    print("# barcodes >  1 {}".format(mrt_one_barcode))
