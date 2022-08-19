#!/usr/bin/env sh

set -e

apt-get install -y python3 redis-server

cd test

python3 -m http.server &

sleep 5

redis-cli -h redis -x LPUSH analyzer:review < test.json
redis-cli -h redis BRPOP analyzer:result 300

pkill python3

exit 0
