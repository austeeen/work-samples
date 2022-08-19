import cv2

from moto import mock_s3
from bv_test_case import BVTestCase
from storage.s3_storage import MockS3Storage

storage_data = {
    "resource_path": "test_resource_path", "resources": ["test.jpg"],
    "output_path": "test_output_path", "output_resources": ["test_blurred.jpg"]
}

storage = MockS3Storage(storage_data)
image_byte_size = 20236

@mock_s3
class TestS3Storage(BVTestCase):

    def setUp(self):
        global storage
        storage = MockS3Storage(storage_data)
        # storage.s3_res.Object(Bucket=storage_data['resource_path'])
        # storage.s3_res.Object(Bucket=storage_data['output_path'])

        storage.s3_res.Bucket(storage_data['resource_path']).create()
        storage.s3_res.Bucket(storage_data['resource_path']).upload_file('images/test1.jpg', storage_data['resources'][0])
        storage.s3_res.Bucket(storage_data['output_path']).create()

    def tearDown(self):
        for resource in storage_data['resources']:
            storage.s3_res.Object(storage_data['resource_path'], resource).delete()
        for resource in storage_data['output_resources']:
            storage.s3_res.Object(storage_data['output_path'], resource).delete()

    def test_create(self):
        self.assertEqual(storage_data["resource_path"], storage.resource_path)
        self.assertEqual(storage_data["resources"], storage.resources)
        self.assertEqual(storage_data["output_path"], storage.output_path)
        self.assertEqual(storage_data["output_resources"], storage.output_resources)

    def test_get_data(self):
        data = storage.get_data()
        self.assertIsNotNone(data)
        self.assertEqual(image_byte_size, len(data))

    def test_get_data_bad_index(self):
        with self.assertRaises(IndexError):
            _ = storage.get_data(index=1)

    def test_get_image(self):
        image = storage.get_image()

        self.assertIsNotNone(image)

    def test_get_image_bad_index(self):
        with self.assertRaises(IndexError):
            _ = storage.get_image(index=1)

    def test_save_image(self):
        image = storage.get_image()
        self.assertFalse(storage.output_resource_exists())
        storage.save_image(image)
        self.assertTrue(storage.output_resource_exists())

    def test_save_image_bad_data(self):
        with self.assertRaises(cv2.error):
            _ = storage.save_image(None)

    def test_save_image_bad_index(self):
        with self.assertRaises(IndexError):
            _ = storage.save_image(storage.get_image(), index=1)

    def test_resources_exists(self):
        self.assertTrue(storage.resource_exists())

    def test_resource_exists_no_data(self):
        storage.s3_res.Object(storage_data['resource_path'], storage_data['resources'][0]).delete()
        self.assertFalse(storage.resource_exists())

    def test_resource_exists_bad_index(self):
        with self.assertRaises(IndexError):
            storage.resource_exists(index=1)

    def test_output_resource_exists_no_data(self):
        self.assertFalse(storage.output_resource_exists())

    def test_output_resource_exists_bad_index(self):
        with self.assertRaises(IndexError):
            storage.output_resource_exists(index=1)