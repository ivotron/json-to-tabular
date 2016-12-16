#!/usr/bin/env python

import argparse
import collections
import json
import os
import os.path
import subprocess
import yaml

parser = argparse.ArgumentParser()

parser.add_argument('--json-header', required=True, help="Header.")
parser.add_argument('--jqexp', required=True, help="JQ expression.")
parser.add_argument('path', help="Path to files to extract CSV from.")


def get_kv_path_and_files(path):
    """Generator of (kv_path, file) tuples for benchmark output files. A kv_path
    is a dictionary that comes from treating a path as key-value pairs
    concatenated in a single string. E.g. `a/b/c/d` generates an `{a: b, c: d}`
    map.
    """
    for path, _, files in os.walk(path):
        for f in files:
            is_json = f.endswith(".json")
            is_yaml = f.endswith(".yaml") or f.endswith(".yml")
            if not is_json and not is_yaml:
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
        print(",".join(kv_path.keys() + args.json_header.split(",")))
        return


def get_records_for_file(fname):

    if not fname.endswith(".json"):
        # if yaml, convert to JSON first
        with open(fname) as ymlfile:
            with open('/tmp/file.json', 'w') as jsonfile:
                json.dump(yaml.load(ymlfile), jsonfile)
        fname = '/tmp/file.json'

    cmd = "jq -r '{} | @csv' {}".format(args.jqexp, fname)
    value_list = subprocess.check_output(cmd, shell=True)
    return value_list.splitlines()


def print_records():
    for kv_path, f in get_kv_path_and_files(args.path):
        for r in get_records_for_file(f):
            if len(kv_path.values()) > 0:
                print(",".join(kv_path.values()) + "," + r)
            else:
                print(r)


args = parser.parse_args()

print_header()
print_records()
