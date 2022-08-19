#!/bin/bash

IP_APP="PRIVATE.py"
OUTDIR=$1

CPU_STATS="$OUTDIR/cpu_pid.txt"
GPU_STATS="$OUTDIR/gpu_stats.csv"
META_DATA="$OUTDIR/meta_data.txt"
NETWORK="$OUTDIR/network.log"

mkdir -p "$OUTDIR"
if test -f "$CPU_STATS"; then echo rm "$CPU_STATS"; fi
if test -f "$GPU_STATS"; then echo rm "$GPU_STATS"; fi
if test -f "$META_DATA"; then echo rm "$META_DATA"; fi
if test -f "$NETWORK"; then echo rm "$NETWORK"; fi

## save snap list
snap list > "$META_DATA"

## run background processes and save their pids
CPU_PID=$(./monitoring/cpu.sh "$CPU_STATS")
if [[ $? -ne 0 ]]; then exit 1; fi
GPU_PID=$(./monitoring/gpu.sh "$GPU_STATS")
if [[ $? -ne 0 ]]; then exit 1; fi

NET_PID=$(./monitoring/network.sh "$NETWORK")
if [[ $? -ne 0 ]]; then exit 1; fi


app_running () {
  PS_OUT=$(ps -ef | grep $IP_APP | tr -s ' ' | cut -d ' ' -f2)
  IP_PIDS=($PS_OUT)
  if [[ ${#IP_PIDS[@]} -gt 1 ]]; then
    echo 1
  else
    echo 0
  fi
}

SLEEP_FOR="30s"
is_running=$(app_running)
while [[ $is_running -ne 1 ]]; do
  echo "waiting $SLEEP_FOR for $IP_APP to start..."
  sleep $SLEEP_FOR
  is_running=$(app_running)
done

SLEEP_FOR="5m"
echo "sleeping $SLEEP_FOR until $IP_APP is finished..."
sleep $SLEEP_FOR
echo "done sleeping, will quit if $IP_APP is done..."

SLEEP_FOR="1m"
WAIT_TIMEOUT=10
is_running=$(app_running)
while [[ $is_running -eq 1  && $WAIT_TIMEOUT -ne 0 ]]; do
  echo "waiting $SLEEP_FOR (x$WAIT_TIMEOUT)..."
  sleep $SLEEP_FOR
  WAIT_TIMEOUT=$((WAIT_TIMEOUT - 1))
  is_running=$(app_running)
done

if [[ $WAIT_TIMEOUT -eq 0  && is_running -eq 1 ]]; then
  echo "timed out waiting for $IP_APP to finish, data collected may not be complete."
else
  echo "$IP_APP finished, data collected should be complete."
fi

## kill background processes
sudo kill -9 "$CPU_PID"
sudo kill -9 "$GPU_PID"
sudo kill -9 "$NET_PID"
