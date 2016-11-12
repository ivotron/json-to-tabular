# Performance Data

A simple schema to represent performance data. This repository 
contains utilities to manipulate files that use this format. Example:

```javascript
{
  "benchmark": "foo",
  "tests": [
    {
      "name": "bar",
      "lower_is_better": <true|false>,
      "result": <number|list|map>
    },
    ...
  ]
}
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

This utility produces the following CSV file:

```csv
repetition, limits, mode, benchmark, test, lower_is_better, result
```
