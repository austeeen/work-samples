import unittest

from bv_test_case import BVTestCase
from storage.local_storage import LocalStorage
from fmcg_blur import FMCGBlur


storage_data = {
    "resource_path": "images/", "resources": ["test1.jpg", "test1_expected_blurred.png"], "output_path": "output/",
    "output_resources": ["test1_expected_blurred.png"]
}
storage = LocalStorage(storage_data)

filter_data = {
    "mask_polygons": [[0, 0, 10, 0, 10, 10, 0, 10], [10, 10, 20, 10, 20, 20, 10, 20]],
    "mask_color": "#A9A9A9",
    "mask_alpha": 1.0
}
image_filter = FMCGBlur(filter_data)


class TestFMCGBlur(BVTestCase):

    def setUp(self):
        super().setUp()
        storage.purge_output_resources()

    def test_create(self):
        self.assertEqual(filter_data["mask_polygons"], image_filter.mask_polygons)
        self.assertEqual(filter_data["mask_color"], image_filter.mask_color)

    def test_convert_polygon(self):
        self.assertSequenceEqual([[1, 2], [3, 4], [5, 6]], image_filter.convert_polygon([1, 2, 3, 4, 5, 6]).tolist())

    def test_convert_polygon_bad_data(self):
        with self.assertRaises(TypeError):
            _ = image_filter.convert_polygon(None)

    def test_create_polygon_list(self):
        polygon_list = image_filter.create_polygon_list()
        self.assertEqual(2, len(polygon_list))
        self.assertSequenceEqual([[0, 0], [10, 0], [10, 10], [0, 10]], polygon_list[0].tolist())
        self.assertSequenceEqual([[10, 10], [20, 10], [20, 20], [10, 20]], polygon_list[1].tolist())

    def test_blur(self):
        blurred_image = image_filter.blur(storage.get_image())

        self.assertImagesEqual(storage.get_image(1), blurred_image)

#        storage.save_image(blurred_image, image_format="png")

    def test_blur_no_image(self):
        with self.assertRaises(AttributeError):
            _ = image_filter.blur(None)