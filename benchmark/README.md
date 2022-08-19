# BENCHMARK TOOLS -- INSIGHT PIPELINE

This directory holds the tools used to benchmark the insight pipeline and output the results in
various formats.

### TL;DR

PRIVATE

### COMMAND EXAMPLES
    PRIVATE

---
## TOOLS

### benchmark.sh
`benchmark.sh PRIVATE`

Benchmark the insight pipeline by running background processes o capture metrics about GPU/CPU/Network performance

### Output:

    output_dir
    ├── cpu_pid.txt
    ├── gpu_stats.csv
    ├── network.log
    └── meta_data.txt

### Usage:
!! _This file may require some set up_ depending on the use case.

!! The output directory will be cleared of any existing output data (`cpu_pid.txt`, `gpu_stats.csv`,
`meta_data.csv`)

#### Description

`pidstat`, `nvidia-smi`, and `iftop` are invoked as background processes. These processes are run
at the time specified in the script and ends when the main pipeline process is shut down.

---

## generate_reports.py
`generate_reports.py [-h] [PRIVATE]
`

Generate all plots and reports from the benchmark data within the given directory.
