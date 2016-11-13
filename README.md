# Performance Data

Tools to generate tabular format files from a collection of JSON and 
YAML files. Many benchmarking tools generate results in JSON or YAML 
formats, but many of the analysis and visualization tools work better 
with tabular formats (e.g. CSV, R/Pandas dataframes, etc.).

Example:

```javascript
```

# Utilities

## `to_csv.py`

Converts a hierarchy of folders storing JSON files into a CSV file. 
For example, given a set of JSON files store in the following 
hierarchy:

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

Given a list of attributes to extract from the set of `out.json` files 
in this hierarchy, for example:

```yaml
- benchmark: 'fio'
- job: '.jobs | .[] | .jobname'
- read_iops: .jobs | .[] | .read.iops
- write_iops: .jobs | .[] | .write.iops
```

This utility produces the following CSV file:

```csv
repetition, limits, mode, benchmark, job, result
```
