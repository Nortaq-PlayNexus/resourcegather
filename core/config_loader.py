"""Path resolution + config/data loading. PyInstaller-aware."""
import json
import os
import sys


def bundle_root():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def output_root():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return bundle_root()


def resource_path(rel):
    return os.path.join(bundle_root(), rel)


def output_path(rel):
    return os.path.join(output_root(), rel)


def load_json(rel):
    with open(resource_path(rel), "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_text(rel):
    with open(resource_path(rel), "r", encoding="utf-8") as fh:
        return fh.read()


def load_settings():
    return load_json("config/settings.json")
