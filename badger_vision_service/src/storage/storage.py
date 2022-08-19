import logging
import cv2
import numpy as np


class Storage:
    def __init__(self, storage_data):
        self.resource_path = storage_data["resource_path"]
        self.resources = storage_data["resources"]
        self.output_path = storage_data["output_path"]
        self.output_resources = storage_data["output_resources"]

        self.validate_bucket(self.resource_path)
        self.validate_resources(self.resources)

        self.validate_bucket(self.output_path)
        self.validate_resources(self.output_resources)

    def resource_exists(self, index=0):
        return False

    def output_resource_exists(self, index=0):
        return False

    @staticmethod
    def validate_resources(resources):
        for resource in resources:
            if not resource:
                raise AttributeError

    @staticmethod
    def validate_bucket(bucket):
        if not bucket:
            raise AttributeError

    def get_data(self, index=0):
        pass

    def get_image(self, index=0):
        logging.info("Creating image")
        return cv2.imdecode(np.frombuffer(self.get_data(index=index), dtype=np.uint8), cv2.IMREAD_UNCHANGED)

    def save_data(self, data, index=0):
        pass

    def save_image(self, image, image_format="jpg", index=0):
        logging.info("Saving image")
        # TODO: pull image type from output_resource
        self.save_data(cv2.imencode(f".{image_format}", image)[1], index=index)
