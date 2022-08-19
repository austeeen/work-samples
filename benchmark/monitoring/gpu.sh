#!/bin/bash

nohup nvidia-smi --format=csv --query-gpu=timestamp,memory.used,utilization.gpu,utilization.memory,temperature.gpu,pstate -lms 50 > "$1" &
PID=$!

if ! ps -p $PID > /dev/null; then
  echo "nvidia-smi did not run. exiting..."
  exit 1
fi

echo $PID