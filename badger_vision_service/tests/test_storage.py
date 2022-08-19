import cv2

from bv_test_case import BVTestCase
from storage.storage import Storage

storage_data = {
    "resource_path": "test_resource_path", "resources": ["test.jpg"], "output_path": "test_output_path",
    "output_resources": ["test_blurred.jpg"]
}

storage = Storage(storage_data)


class TestStorage(BVTestCase):

    def test_create(self):
        self.assertEqual(storage_data["resource_path"], storage.resource_path)
        self.assertEqual(storage_data["resources"], storage.resources)
        self.assertEqual(storage_data["output_path"], storage.output_path)
        self.assertEqual(storage_data["output_resources"], storage.output_resources)

    def test_validate_resources(self):
        with self.assertRaises(AttributeError):
            storage.validate_resources([None])

    def test_validate_bucket(self):
        with self.assertRaises(AttributeError):
            storage.validate_bucket(None)

    def test_save_image_no_image(self):
        with self.assertRaises(cv2.error):
            _ = storage.save_image(None)