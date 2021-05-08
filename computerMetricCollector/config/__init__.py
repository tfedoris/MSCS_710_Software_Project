import json
import os


def import_config(root_path):
    full_file_path = root_path + "\\config\\setting.json"
    settings = {}
    if os.path.exists(full_file_path):
        with open(file=full_file_path) as f:
            settings = json.load(f)
    else:
        print("Settings file can not be found: " + full_file_path)
    return settings
