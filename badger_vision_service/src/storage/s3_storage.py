import boto3
import botocore

from moto import mock_s3
from storage.storage import Storage


class S3Storage(Storage):
    def __init__(self, storage_data):
        super().__init__(storage_data)
        self.s3_res = boto3.resource("s3")

    def resource_exists(self, index=0):
        try:
            self.s3_res.Object(self.resource_path, self.resources[index]).load()
        except botocore.exceptions.ClientError:
            return False
        return True

    def output_resource_exists(self, index=0):
        try:
            self.s3_res.Object(self.output_path, self.output_resources[index]).load()
        except botocore.exceptions.ClientError:
            return False
        return True

    def get_data(self, index=0):
        return self.s3_res.Object(self.resource_path, self.resources[index]).get()["Body"].read()

    def save_data(self, data, index=0):
        self.s3_res.Object(self.output_path, self.output_resources[index]).put(Body=data.tobytes())

@mock_s3
class MockS3Storage(S3Storage):
    def __init__(self, storage_data):
        super().__init__(storage_data)
        self.s3_res = boto3.resource("s3")