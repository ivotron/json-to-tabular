#!/usr/bin/env python

import argparse
import collections
import os
import os.path
import subprocess
import yaml

parser = argparse.ArgumentParser()

parser.add_argument(
        '--csv-spec', dest='spec', default="csv_spec.yml", help="Spec file.")


def check_spec(spec):
    for s in spec:
        if not isinstance(s, dict):
            raise Exception("Expecting a list of 1-item dictionaries")
        if len(s) != 1:
            raise Exception("Expecting dictionary with one key; got " + s)


def get_jq_expression(spec):
    exps = []

    for s in spec:
        exp = s.values()[0]

        # check if a literal was given, so we double-quote it
        if '.' not in exp:
            exp = '["{}"]'.format(exp)
        else:
            exp = '[{}]'.format(exp)

        exps.append(exp)

    return "'" + (" + ".join(exps)) + " | @csv'"


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

            yield kv, path+"/"+f


def print_header(spec):
    json_header = [s.keys()[0] for s in spec]
    for kv_path, _ in get_kv_path_and_files("./"):
        # TODO intersect json_header with kv_path.keys() to detect name clashes
        print(",".join(kv_path.keys() + json_header))
        return


def get_records_for_file(fname, jq_expression):
    value_list = subprocess.check_output(
                     "jq -r {} {}".format(jq_expression, fname), shell=True)
    return value_list.splitlines()


def print_records(spec):
    jq_expression = get_jq_expression(spec)

    for kv_path, f in get_kv_path_and_files("./"):
        for r in get_records_for_file(f, jq_expression):
            if len(kv_path.values()) > 0:
                print(",".join(kv_path.values()) + "," + r)
            else:
                print(r)


args = parser.parse_args()

with open(args.spec) as f:
    spec = yaml.load(f)

check_spec(spec)

print_header(spec)
print_records(spec)
