#!/bin/bash

nohup sudo iftop -i wlo1 -t > "$1" &
PID=$!

if ! ps -p $PID > /dev/null; then
  echo "iftop did not run. exiting..."
  exit 1
fi

echo $PID