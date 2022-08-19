import unittest
import logging


class BVTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format="%(asctime)s %(levelname)s [%(module)s::%(funcName)s] %(message)s", level=logging.DEBUG)

    def assertImagesEqual(self, image1, image2):
        self.assertEqual(image1.shape, image2.shape)
        self.assertEqual(image1.tolist(), image2.tolist())
