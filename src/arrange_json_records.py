# -*- coding: utf8 -*-
# ==========================================================================
#   Copyright (C) since 2022 All rights reserved.
#
#   filename : arrange_json_records.py
#   author   : chendian / okcd00@qq.com
#   date     : 2023-01-10
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


def construct_input_candidates(json_path, dump_path):
    candidate_dict = {}
    
    record_dict = load_json(json_path)    
    for key in tqdm(sorted(record_dict.keys())):
        items = record_dict[key]
        input_sequence = key
        candidates = [token.strip() for token in items[1:] 
                      if token.strip() and is_pure_chinese_phrase(token) and all([t in VOCAB for t in token])]
        candidate_dict[input_sequence] = candidates
    dump_json(candidate_dict, dump_path)


if __name__ == "__main__":
    target = 'google'
    dump_path = f'./release/input_candidates.{target}.json'
    src_path = f'./records/{target}/' + 'input_candidates.api.230110_185602.json'
    
    # pprint(src_path)
    construct_input_candidates(json_path=src_path, dump_path=dump_path)
