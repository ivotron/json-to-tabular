#!/usr/bin/env python

import collections
import os
import os.path
import subprocess


def get_kv_path_and_files(path):
    """Generator of (kv_path, file) tuples for benchmark output files. A kv_path
    is a dictionary that comes from treating a path as key-value pairs
    concatenated in a single string. E.g. `a/b/c/d` generates an `{a: b, c: d}`
    map.
    """
    # TODO assumes that all files are in the same key-value paths
    for path, _, files in os.walk(path):
        for f in files:
            if not f.endswith(".json"):
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

            yield kv, f


def get_header(path):
    # TODO support header for lists and maps
    json_header = ["benchmark", "test", "lower_is_better", "result"]
    for kv_path, _ in get_kv_path_and_files(path):
        print("kv path: " + str(kv_path))
        return kv_path.keys() + json_header


def get_records_for_file(fname):
    jq_expression = (
        "'. | "
        "[.benchmark] + (.tests | .[] | [.name, .lower_is_better, .result]) | "
        "@csv'"
    )

    value_list = subprocess.check_output(["jq", "-r", jq_expression, fname])

    return value_list.split(",")


def get_records(path):
    records = []
    for kv_path, f in get_kv_path_and_files(path):
        for r in get_records_for_file(f):
            records += [(kv_path.values() + r)]
    return records

print(get_header("./"))
print(get_records("./"))
