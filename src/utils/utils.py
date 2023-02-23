"""
ffs.streams
~~~~~~~~~~~~

Utility functions
"""
import logging
import os
import re
import time
import warnings
from sys import platform


def get_path_info(path):
    """
    Retuns path info
    """
    dirname = os.path.dirname(path)
    name = str(os.path.basename(path).rsplit(".", 1)[0])

    return dirname, name


def mkdir(dirname: str) -> None:
    """
    Makes a directory.
    """
    try:
        os.makedirs(dirname)
    except OSError as exc:
        logging.info(exc)


def rm(path: str) -> None:
    """
    Removes a direcrtory
    """
    try:
        os.remove(path)
    except OSError as exc:
        logging.info(exc)


def clean_args(args: list) -> list:
    """
    Cleans arguments
    """
    clean_args_ = []
    for arg in args:
        if " " in arg:
            arg = '"' + arg + '"'
        clean_args_.append(arg.replace("\\", "/").replace("__COLON__", ":"))

    return clean_args_


def convert_to_sec(time):
    """
    Time conversion to seconds
    """
    h, m, s = time.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def get_time(key, string, default):
    """
    Gets time frame
    """
    time = re.search("(?<={})\w+:\w+:\w+".format(key), string)
    return convert_to_sec(time.group(0)) if time else default


def time_left(start_time, unit, total):
    """
    Calculate time remaining
    """
    if unit != 0:
        diff_time = time.time() - start_time
        return total * diff_time / unit - diff_time
    else:
        return 0


def get_os():
    """
    Returns OS type.
    """
    if platform in ["linux", "linux2"]:
        return "linux"
    elif platform == "darwin":
        return "os_x"
    elif platform in ["win32", "Windows"]:
        return "windows"
    else:
        return "unknown"


def cnv_options_to_args(options: dict):
    """
    Converts options to arguments.
    """
    args = []
    for k, v in options.items():
        args.append("-{}".format(k))
        if v is not None:
            args.append("{}".format(v))

    return args
