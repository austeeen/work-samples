import boto3
import random
import string

from botocore.exceptions import ClientError
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError
from io import BytesIO


class Uploader:
    def __init__(self, bucket, log):
        self._bucket = bucket
        self._log = log

    def upload(self, image_obj, capture_event_id, camera_label):
        mem_file = BytesIO()
        image_obj.save(mem_file, format='JPEG')

        # We need to rewind the mem_file to point to the beginning of the file.
        # Otherwise we'll be uploading 0 bytes files.
        mem_file.seek(0)

        key = ('blurred-images/{}-{}.jpg'.format(capture_event_id,
               ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                       for _ in range(5))))

        if self._push_image(mem_file, key):
            return {'camera_label': camera_label, 'key': key}
        else:
            self._log.error("Error pushing image to bucket!")
            return None

    def _push_image(self, mem_file, key):
        pass


class S3(Uploader):
    def __init__(self, bucket, logger, test_run=None):
        Uploader.__init__(self, bucket, logger)
        if test_run:
            self._s3_client = boto3.client(service_name='s3', endpoint_url='http://PRIVATE:PRIVATE')
        else:
            self._s3_client = boto3.client('s3')

    def _push_image(self, mem_file, key):
        try:
            self._s3_client.upload_fileobj(mem_file, self._bucket, key)
        except ClientError as e:
            self._log.error("An error occurred while uploading image to bucket: {}".format(e))
            return False
        return True


class Gcloud(Uploader):
    def __init__(self, bucket, logger):
        Uploader.__init__(self, bucket, logger)
        self._g_client = storage.Client()

    def _push_image(self, mem_file, key):
        try:
            bucket_obj = self._g_client.get_bucket(self._bucket)
            blob = bucket_obj.blob(key)
            blob.upload_from_file(mem_file)
        except GoogleCloudError as e:
            self._log.error("An error ocurred while uploading image to bucket: {}".format(e))
            return False
        return True
