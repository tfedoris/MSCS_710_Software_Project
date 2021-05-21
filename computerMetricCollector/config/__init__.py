import json
import os


def import_config(root_path):
    """
    This function import the settings for the computer metric collector
    from settings.json file
    :param root_path: Root dir of the computer metric collector program
    :return: dictionary represents configured values in settings.json
    """
    full_file_path = root_path + "\\config\\setting.json"
    settings = {}
    if os.path.exists(full_file_path):
        with open(file=full_file_path) as f:
            settings = json.load(f)
        settings["root_dir"] = root_path
    else:
        print("Settings file can not be found: " + full_file_path)
    return settings
