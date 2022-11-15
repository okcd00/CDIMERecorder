# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : utils.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-02-19
#   desc     : global utils
# ==========================================================================
from __future__ import print_function
import os


# from pathlib import Path
# PROJECT_PATH = Path.cwd()
PROJECT_PATH = os.path.dirname(__file__)


def flatten(nested_list, unique=False):
    ret = [elem for sub_list in nested_list for elem in sub_list]
    if unique:
        return list(set(ret))
    return ret


def unique(input_list):
    return list(set(input_list))


def stable_unique(input_list):
    return sorted(unique(input_list), key=input_list.index)


if __name__ == '__main__':
    print(PROJECT_PATH)
