# -*- coding: utf8 -*-
# ==========================================================================
#   Copyright (C) since 2022 All rights reserved.
#
#   filename : arrange_typist_logs.py
#   author   : chendian / okcd00@qq.com
#   date     : 2022-11-18
#   desc     : 
# ==========================================================================
import sys
sys.path.append('./')
sys.path.append('../')

from utils import *
from tqdm import tqdm
from pprint import pprint
from file_io import load_json, dump_json
VOCAB = [line.strip() for line in open('./data/vocab.txt', 'r', encoding='utf-8')]


def construct_input_candidates(log_path_case, dump_path):
    if not isinstance(log_path_case, list):
        log_path_case = [log_path_case]
    
    candidate_dict = {}
    for log_path in log_path_case:
        lines = [line.strip() for line in open(log_path, 'r', encoding='utf-8')]
        # print(f"file {log_path} has {len(lines)} lines.")
        for line in tqdm(lines):
            items = [item.strip() for item in line.split('|')]
            input_sequence = items[0]
            candidates = [token.strip() for token in items[1:] 
                          if token.strip() and is_pure_chinese_phrase(token) and all([t in VOCAB for t in token])]
            candidate_dict[input_sequence] = candidates
    dump_json(candidate_dict, dump_path)


if __name__ == "__main__":
    target = 'microsoft'
    dump_path = f'./release/input_candidates.{target}.json'
    src_path = []
    for file_path in ['1c40_log.txt', '2c16_log.txt', '3c8_log.txt']:
        src_path.append(f'./records/{target}/input_candidates.typist.{file_path}')
    
    # pprint(src_path)
    construct_input_candidates(log_path_case=src_path, dump_path=dump_path)
