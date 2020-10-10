import os
import json


def create_ine(path):
    file_name = path.split("/")[-1]
    folders = path.split("/")[:-1]

    path_accumulator = "./"

    for folder in folders:
        if not os.path.exists(path_accumulator + folder):
            os.makedirs(path_accumulator + folder)
        path_accumulator += folder + "/"

    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("{}")


def get_config():
    with open("config.json", "r") as cfg:
        return json.load(cfg)


def update_config(updated_cfg):
    with open("config.json", "w") as cfg:
        json.dump(updated_cfg, cfg, indent=4)
