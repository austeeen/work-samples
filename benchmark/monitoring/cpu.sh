#!/bin/bash


nohup ./monitoring/pidstat -h -l -r -u -d -w -p ALL 1 > "$1" &
PID=$!

if ! ps -p $PID > /dev/null; then
  echo "pidstat did not run. exiting..."
  exit 1
fi

echo $PID