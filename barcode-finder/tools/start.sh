#!/bin/bash


echo "Using Redis server at --> ${REDIS_SERVER}:${REDIS_PORT}"
exec /usr/src/app/build/Analyzer
# tail -F dne.blah
