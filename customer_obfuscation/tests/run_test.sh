#!/usr/bin/env bash

set -e

cd tests

echo "Fetching redis cli tools..."
wget -q http://download.redis.io/redis-stable.tar.gz
tar xf redis-stable.tar.gz
cd redis-stable
make > /dev/null 2>&1 #SSSSHhhhhh
cp src/redis-cli /usr/local/bin/
chmod 755 /usr/local/bin/redis-cli
echo "Done fetching redis cli tools"

echo "Fetching jq..."
cd /usr/local/bin
wget https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64
cp jq-linux64 jq
chmod 755 jq
echo "Done fetching jq"

echo "Fetching awscli..."
pip install awscli --upgrade --quiet
if [ "$?" -ne "0" ]; then
  echo "Installation of awscli failed."
  exit 1
fi
echo "Done fetching awscli"

cd /usr/src/app/tests

echo "Configuring localstack..."
aws --endpoint-url="http://PRIVATE:PRIVATE" s3 mb s3://PRIVATE-bucket
aws --endpoint-url="http://PRIVATE:PRIVATE" s3api PRIVATE-bucket-acl --bucket PRIVATE-bucket --acl PRIVATE-read
aws --endpoint-url="http://PRIVATE:PRIVATE" s3 cp /usr/src/app/tests/data/test.jpg s3://PRIVATE-bucket/PRIVATE/test.jpg
echo "Done configuring localstack"

redis-cli -h redis -x LPUSH PRIVATE:review < test.json
result=$(redis-cli -h redis BRPOP PRIVATE:result 300 | grep -i "1234")
echo $result

faces_detected=$(echo $result | jq '.keys | length')
if [ "$face_detected" == "0" ]; then
  echo "No faces were detected!!"
  exit 1
fi

key=$(echo $result | jq '.keys | first')
aws --endpoint-url="http://PRIVATE:PRIVATE" s3 ls s3://PRIVATE-bucket/$key
if [ "$?" -ne "0" ]; then
  echo "File was not uploaded to bucket!"
  exit 1
fi

echo "Sending success"
exit 0
