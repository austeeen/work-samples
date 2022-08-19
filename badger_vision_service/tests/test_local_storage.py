import cv2

from bv_test_case import BVTestCase
from storage.local_storage import LocalStorage


storage_data = {
    "resource_path": "images/", "resources": ["test1.jpg"], "output_path": "output/",
    "output_resources": ["test1_blurred.jpg"]
}
storage = LocalStorage(storage_data)

image_byte_size = 20236


class TestLocalStorage(BVTestCase):

    def setUp(self):
        super().setUp()
        storage.purge_output_resources()

    def test_create(self):
        self.assertEqual(storage_data["resource_path"], storage.resource_path)
        self.assertEqual(storage_data["resources"], storage.resources)
        self.assertEqual(storage_data["output_path"], storage.output_path)
        self.assertEqual(storage_data["output_resources"], storage.output_resources)

    def test_get_full_output_resource_path(self):
        self.assertEqual("output/test1_blurred.jpg", storage.get_full_output_resource_path())

    def test_get_full_resource_path(self):
        self.assertEqual("images/test1.jpg", storage.get_full_resource_path())

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

    def test_resource_exists_bad_index(self):
        with self.assertRaises(IndexError):
            storage.resource_exists(index=1)

    def test_output_resource_exists_no_data(self):
        self.assertFalse(storage.output_resource_exists())

    def test_output_resource_exists_bad_index(self):
        with self.assertRaises(IndexError):
            storage.output_resource_exists(index=1)
