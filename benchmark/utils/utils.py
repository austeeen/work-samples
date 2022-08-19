import os


def set_up_output_dir(out_path):
    if out_path == "":
        return
    os.makedirs(out_path, exist_ok=True)
