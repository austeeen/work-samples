import os
import json
import time


class FileManager:

    def __init__(self, out_dir=None):
        self.out_dir = out_dir

    def get_out_path(self, file_path, prepend=""):
        if prepend:
            path, filename = os.path.split(file_path)
            filename = f"{prepend}-{filename}"
            file_path = os.path.join(path, filename)
        if self.out_dir:
            full_out_path = os.path.join(self.out_dir, file_path)
        else:
            full_out_path = file_path
        for r in range(5):
            try:
                os.makedirs(os.path.dirname(full_out_path), exist_ok=True)
                break
            except:
                time.sleep(1) # MJP - I found this sometimes happens w/VPN + autofs + NFS
                if r == 4:
                    return None
        return full_out_path

    def save_data(self, file_data, file_path, pre_pend=""):
        if not file_data or not file_path:
            return ""

        full_out_path = self.get_out_path(file_path, pre_pend)
        if full_out_path is None:
            return None
        with open(full_out_path, "wb") as data_file:
            data_file.write(file_data)
            print(f"Downloaded {full_out_path}")
        return full_out_path

    def save_json(self, output_data, file_path):
        if not output_data:
            return

        full_out_path = self.get_out_path(file_path)
        with open(full_out_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)
