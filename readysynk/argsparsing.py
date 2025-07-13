# coding: utf-8

import argparse
from readysynk import __version__


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="readysynk is readiness synchronization application. ")

    parser.add_argument("--version", action="version", version=f"V{__version__}", help="Check version. ")

    parser.add_argument("settings_path", type=str, help="Path to yaml file with settings. ")

    return parser.parse_args()
