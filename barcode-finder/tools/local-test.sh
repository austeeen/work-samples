#!/bin/bash

rc=0
docker-compose up -d
cid=$(docker ps -aqf "name=barcode-finder_1")
docker exec $cid bash -c "test/run_test.sh"

if [ "$?" -ne "0" ]; then
  echo "Failed test"
  rc=1
fi
docker-compose down
exit $rc
