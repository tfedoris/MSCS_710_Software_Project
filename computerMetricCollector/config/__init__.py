import json


def import_config(root_path):
    full_file_path = root_path + "/config/setting.json" # "\\config\\setting.json"
    with open(file=full_file_path) as f:
        settings = json.load(f)
    return settings
