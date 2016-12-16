# JSON to tabular format

Tools to generate tabular format files from a collection of 
semi-structured files. Benchmarking tools generate results in JSON or 
YAML formats but most of the analysis and visualization tools work 
better with tabular formats (e.g. CSV, R/Pandas dataframes, etc.).

# Utilities

## `to_csv.py`

Uses [jq](https://stedolan.github.io/jq/) to convert a hierarchy of 
folders storing JSON/YAML files into a CSV file. For example, given a 
set of JSON files store in the following hierarchy:

```
./
└── repetition
    ├── 0
    │   └── limits
    │       ├── no
    │       │   └── mode
    │       │       ├── randread
    │       │       │   └── out.json
    │       │       ├── read
    │       │       │   └── out.json
    │       │       └── write
    │       │           └── out.json
    │       └── yes
    │           └── mode
    │               ├── randread
    │               │   └── out.json
    │               ├── read
    │               │   └── out.json
    │               └── write
    │                   └── out.json
    ├── 1
    │   └── limits
    │       ├── no
    │       │   └── mode
    │       │       ├── randread
    │       │       │   └── out.json
    │       │       ├── read
    │       │       │   └── out.json
    │       │       └── write
    │       │           └── out.json
    │       └── yes
    │           └── mode
    │               ├── randread
    │               │   └── out.json
    │               ├── read
    │               │   └── out.json
    │               └── write
    │                   └── out.json
```

And `out.json` files containing data such as:

```javascript
{
  "fio version" : "fio-2.10",
  "timestamp" : 1480611510,
  "time" : "Thu Dec  1 16:58:30 2016",
  "global options" : {
    "ioengine" : "libaio",
    "invalidate" : "1",
    "ramp_time" : "5",
    "iodepth" : "1",
    "runtime" : "30",
    "direct" : "1"
  },
  "jobs" : [
    {
      "jobname" : "rw-sdb-4k-seq",
      "groupid" : 0,
      "error" : 0,
      "eta" : 0,
      "elapsed" : 36,
      "job options" : {
        "bs" : "4k",
        "rw" : "rw",
        "write_bw_log" : "fio-filec318a5d4212e-4k-sdb-rw-seq.results",
        "write_iops_log" : "fio-filec318a5d4212e-4k-sdb-rw-seq.results",
        "filename" : "/dev/sdb"
      },
      "read" : {
        "io_bytes" : 89304,
        "bw" : 2976,
        "iops" : 744.13,
        "runtime" : 30003,
        "total_ios" : 22326,
        "short_ios" : 0,
        "drop_ios" : 0,
        "slat" : {
          "min" : 6,
          "max" : 181,
          "mean" : 24.62,
          "stddev" : 2.07
        },
      },
      "write" : {
        "io_bytes" : 89480,
        "bw" : 2982,
        "iops" : 745.59,
        "runtime" : 30003,
        "total_ios" : 22370,
        "short_ios" : 0,
        "drop_ios" : 0,
        "slat" : {
          "min" : 7,
          "max" : 72,
          "mean" : 24.93,
          "stddev" : 1.80
        }
      }
    }
  ]
}
```

A list CSV headers and attributes to extract (in [JQ 
syntax](https://stedolan.github.io/jq/tutorial/)) from the set of 
`out.json` files in this hierarchy, e.g.:

```
to_csv.py \
  --json-header 'benchmark,job,read_iops,write_iops'
  --jq-exp '. | .jobs | .[] | ["fio", .jobname, .read.iops, .write.iops ]'
  path/to/hierarchy
```

This utility produces the following CSV file:

```csv
repetition,limits,mode,benchmark,job,read_iops,write_iops
0,no,randread,"fio","randread-sdb-4k-seq",29.78,0
0,no,read,"fio","read-sdb-4k-seq",586.31,0
0,no,write,"fio","write-sdb-4k-seq",0,5546.54
0,yes,randread,"fio","randread-sdb-4k-seq",15.83,0
0,yes,read,"fio","read-sdb-4k-seq",42.61,0
0,yes,write,"fio","write-sdb-4k-seq",0,43.04
1,no,randread,"fio","randread-sdb-4k-seq",29.78,0
1,no,read,"fio","read-sdb-4k-seq",533.76,0
1,no,write,"fio","write-sdb-4k-seq",0,5489.39
1,yes,randread,"fio","randread-sdb-4k-seq",15.47,0
1,yes,read,"fio","read-sdb-4k-seq",40,0
1,yes,write,"fio","write-sdb-4k-seq",0,41.98
```
