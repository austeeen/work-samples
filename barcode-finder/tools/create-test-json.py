#!/usr/bin/env python3
import sys
import json
import time
import boto3

def create_json (url):
    data = {'id': 1234, 'url': url}

    return json.dumps(data)

def get_url(bucket, key):
    s3 = boto3.client('s3')
    return s3.generate_presigned_url('get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=300)

def main():
    if len(sys.argv) < 3:
        print("Usage:\n./create-test-json.py <bucket> <key>")
        exit()

    bucket = sys.argv[1]
    key = sys.argv[2]

    url = get_url(bucket, key)

    json_contents = create_json(url)

    with open("test.json", "w") as output:
        output.write(json_contents)

if __name__ == "__main__":
    main()

