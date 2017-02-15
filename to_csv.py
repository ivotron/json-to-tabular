#!/usr/bin/env python

import argparse
import collections
import json
import os
import os.path
import subprocess
import yaml
import re

parser = argparse.ArgumentParser()

parser.add_argument('--print-header', action='store_true',
                    help="Print header.", default=True)
parser.add_argument('--header', required=False,
                    help=("Header associated to files. This header is a suffix "
                          "of the header obtained from the KV path"))
parser.add_argument('--jqexp',
                    help="JQ expression used against JSON files.")
parser.add_argument('--shexp',
                    help="command used to extract rows from plain text files.")
parser.add_argument('--txtregex',
                    help=("regular expression to filter plain text files. "
                          "Matching files are piped into shexp"))
parser.add_argument('path',
                    help="Path to files to extract CSV from.")


def get_file_type(f):
    if f.endswith(".csv"):
        return "csv"
    if f.endswith(".json"):
        return "json"
    if f.endswith(".yaml") or f.endswith(".yml"):
        return "yaml"

    # filename needs to match given regex, otherwise ignore
    if args.shexp and args.txtregex and re.compile(args.txtregex).match(f):
        return "txt"
    else:
        return "ignore"


def get_kv_path_and_files(path):
    """Generator of (kv_path, file) tuples for benchmark output files. A kv_path
    is a dictionary that comes from treating a path as key-value pairs
    concatenated in a single string. E.g. `a/b/c/d` generates an `{a: b, c: d}`
    map.
    """
    for path, _, files in os.walk(path):
        for f in files:

            if get_file_type(f) == "ignore":
                continue

            kv_path = path.split("/")

            # remove '.' from list
            kv_path.pop(0)

            if len(kv_path) % 2.0 != 0.0:
                raise Exception(
                    "Expecting even number of path elements: " + str(kv_path))

            kv = collections.OrderedDict()
            for i in range(0, len(kv_path), 2):
                kv.update({kv_path[i]: kv_path[i+1]})

            yield kv, path+"/"+f


def print_header():
    for kv_path, _ in get_kv_path_and_files(args.path):
        print(",".join(kv_path.keys() + args.header.split(",")))
        return


def get_records_for_file(fname):

    ftype = get_file_type(fname)

    if ftype == "csv":
        # TODO we assume CSVs have no header; we should make it optional
        with open(fname, 'r') as csvfile:
            return csvfile.readlines()

    if ftype == "txt":
        # apply shexp to file
        cmd = "cat {} | {}".format(fname, args.shexp)

    if ftype == "yaml" or ftype == "json":
        if ftype == "yaml":
            # convert to JSON
            with open(fname) as ymlfile:
                with open('/tmp/file.json', 'w') as jsonfile:
                    json.dump(yaml.load(ymlfile), jsonfile)
            fname = '/tmp/file.json'

        cmd = "jq -r '{} | @csv' {}".format(args.jqexp, fname)

    return subprocess.check_output(cmd, shell=True).splitlines()


def print_records():
    for kv_path, f in get_kv_path_and_files(args.path):
        for r in get_records_for_file(f):
            if len(kv_path.values()) > 0:
                print(",".join(kv_path.values()) + "," + r)
            else:
                print(r)


args = parser.parse_args()

if args.print_header:
    print_header()

print_records()
