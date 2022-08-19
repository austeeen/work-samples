import logging
import os
from storage.storage import Storage


class LocalStorage(Storage):
    def __init__(self, storage_data):
        super().__init__(storage_data)

    def get_full_resource_path(self, index=0):
        return f"{self.resource_path}{self.resources[index]}"

    def get_full_output_resource_path(self, index=0):
        return f"{self.output_path}{self.output_resources[index]}"

    def resource_exists(self, index=0):
        return os.path.exists(self.get_full_resource_path(index=index))

    def purge_output_resources(self):
        for index in range(len(self.output_resources)):
            if self.output_resource_exists(index=index):
                file = self.get_full_output_resource_path(index=index)
                os.makedirs(os.path.dirname(file), exist_ok=True)
                logging.info(f"Removing {file}")
                os.remove(file)

    def output_resource_exists(self, index=0):
        return os.path.exists(self.get_full_output_resource_path(index=index))

    def get_data(self, index=0):
        file_path = self.get_full_resource_path(index=index)
        logging.info(f"Loading data index[{index}] path[{file_path}]")

        with open(file_path, "rb") as data_file:
            return data_file.read()

    def save_data(self, data, index=0):
        file_path = self.get_full_output_resource_path(index=index)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        logging.info(f"Saving data index[{index}] path[{file_path}]")

        with open(file_path, "wb") as data_file:
            return data_file.write(data)

