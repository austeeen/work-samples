import os
import boto3
import botocore
import time


from .utils.helpers import print_wait_message


class S3Storage:
    def __init__(self):
        self.s3_res = boto3.resource("s3")

    def resource_exists(self, bucket_path, resource_key):
        if not bucket_path and not resource_key:
            return False
        try:
            self.s3_res.Object(bucket_path, resource_key).load()
        except botocore.exceptions.ClientError:
            return False
        return True

    def get_resource(self, bucket, key, timeout, sleep=5):
        if self.resource_exists(bucket, key):
            return self.s3_res.Object(bucket, key).get()["Body"].read()
        return self.wait_for_resource(bucket, key, timeout, sleep)

    def wait_for_resource(self, bucket, key, timeout, sleep):
        time.sleep(sleep)
        print(f"Waiting for {key} on S3, timeout: {timeout}")
        start = now = time.time()
        while now < timeout + start:
            if self.resource_exists(bucket, key):
                return self.s3_res.Object(bucket, key).get()["Body"].read()
            print_wait_message(f"Resource does not exist on s3", timeout, start)
            time.sleep(sleep)
            now = time.time()

        print(f"Timed out waiting for {os.path.join(bucket, key)} to upload to s3.")
        return None

    def add_client(self):
        """ To delete a bunch of objects, call this first to efficiency """
        if 'client' not in dir(self):
            self.client = boto3.client('s3')

    def remove_resource(self, bucket, key):
        self.add_client()
        self.client.delete_object(Bucket=bucket, Key=key)

    def copy_resource(self, src_bucket, src_key, dest_bucket, dest_key):
        self.s3_res.Object(dest_bucket, dest_key).copy_from(CopySource=f'{src_bucket}/{src_key}')

    def upload_file(self, filename, bucket, key):
        """ Upload a file to S3 """
        self.add_client()
        self.client.upload_file(filename, bucket, key)

    def get_md5sum(self, bucket, key):
        """ Get the MD5 hash for the given bucket/key.  Return None if not exists """
        self.add_client()
        try:
            return self.client.head_object(Bucket=bucket, Key=key)['ETag'][1:-1]
        except botocore.exceptions.ClientError:
            return None
        return None

