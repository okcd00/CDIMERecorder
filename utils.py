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
import random
import datetime


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


def is_chinese_char(cp):
    """Checks whether CP is the codepoint of a CJK character."""
    # This defines a "chinese character" as anything in the CJK Unicode block:
    #   https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
    #
    # Note that the CJK Unicode block is NOT all Japanese and Korean characters,
    # despite its name. The modern Korean Hangul alphabet is a different block,
    # as is Japanese Hiragana and Katakana. Those alphabets are used to write
    # space-separated words, so they are not treated specially and handled
    # like the all of the other languages.
    if ((cp >= 0x4E00 and cp <= 0x9FFF) or  #
        (cp >= 0x3400 and cp <= 0x4DBF) or  #
        (cp >= 0x20000 and cp <= 0x2A6DF) or  #
        (cp >= 0x2A700 and cp <= 0x2B73F) or  #
        (cp >= 0x2B740 and cp <= 0x2B81F) or  #
        (cp >= 0x2B820 and cp <= 0x2CEAF) or
        (cp >= 0xF900 and cp <= 0xFAFF) or  #
        (cp >= 0x2F800 and cp <= 0x2FA1F)):  #
        return True
    return False


def is_pure_chinese_phrase(phrase_str):
    # all tokens are Chinese
    return False not in list(map(is_chinese_char, map(ord, phrase_str)))


def is_non_chinese_phrase(phrase_str):
    # there is not any Chinese token in it
    return True not in list(map(is_chinese_char, map(ord, phrase_str)))


if __name__ == '__main__':
    print(PROJECT_PATH)
