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
                    help="Print header.", default=False)
parser.add_argument('--header', required=False,
                    help=("Header associated to files. This header is a suffix "
                          "of the header obtained from the KV path"))
parser.add_argument('--jqexp',
                    help="JQ expression used against JSON files.")
parser.add_argument('--shexp',
                    help=("A shell expression (one or more piped commands) "
                          "used to extract rows from plain text files. A text "
                          "file is any non-tabular format (csv, json or yaml."))
parser.add_argument('--filefilter',
                    help=("Regex expression used to filter files. By default "
                          "all .csv .json .yaml/.yml files are processed."))
parser.add_argument('path',
                    help="Path to files to extract CSV from.")


def get_file_type(f, path=None):
    if path:
        f = path + "/" + f

    # if filter was given, check if file matches it
    if args.filefilter and not re.compile(args.filefilter).match(f):
        return "ignore"

    if f.endswith(".csv"):
        return "csv"
    if f.endswith(".json"):
        return "json"
    if f.endswith(".yaml") or f.endswith(".yml"):
        return "yaml"
    else:
        return "txt"


def get_kv_path_and_files(path):
    """Generator of (kv_path, file) tuples for benchmark output files. A kv_path
    is a dictionary that comes from treating a path as key-value pairs
    concatenated in a single string. E.g. `a/b/c/d` generates an `{a: b, c: d}`
    map.
    """
    for path, _, files in os.walk(path):
        for f in files:

            if get_file_type(f, path) == "ignore":
                continue

            kv_path = path.split("/")

            # remove '.' from list
            if path.startswith("."):
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
        cmd = "cat {}".format(fname)
        if args.shexp:
            # apply shexp to file
            cmd += " | {}".format(args.shexp)

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

if args.print_header or args.header:
    print_header()

print_records()
