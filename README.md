# JSON to tabular format

Tools to generate tabular format files from a collection of JSON and 
YAML files. Many benchmarking tools generate results in JSON or YAML 
formats, but many of the analysis and visualization tools work better 
with tabular formats (e.g. CSV, R/Pandas dataframes, etc.).

Example:

```javascript
```

# Utilities

## `to_csv.py`

Uses [jq](https://stedolan.github.io/jq/) to convert a hierarchy of 
folders storing JSON files into a CSV file. For example, given a set 
of JSON files store in the following hierarchy:

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

Given a list of attributes to extract (in [JQ 
syntax](https://stedolan.github.io/jq/tutorial/)) from the set of 
`out.json` files in this hierarchy, [for example]():

```yaml
- benchmark: 'fio'
- job: '.jobs | .[] | .jobname'
- read_iops: '.jobs | .[] | .read.iops'
- write_iops: '.jobs | .[] | .write.iops'
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
