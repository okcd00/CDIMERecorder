# -*- coding: utf8 -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : paddle_hub.py
#   author   : chendian / okcd00@qq.com
#   date     : 2022-11-14
#   desc     : take the OCR module from PaddleHub.
#   https://www.paddlepaddle.org.cn/hubdetail?name=chinese_ocr_db_crnn_server&en_category=TextRecognition
# ==========================================================================


from tqdm import tqdm
from glob import glob
from pprint import pprint
from collections import defaultdict

import paddlehub as hub
import cv2


ocr = hub.Module(
    name="chinese_ocr_db_crnn_server", enable_mkldnn=True)       # mkldnn加速仅在CPU下有效


records = defaultdict(list)
files = glob('./records/*0.jpg')
for file in tqdm(files):
    result = ocr.recognize_text(images=[cv2.imread(file)])[0]
    # [or]
    # result = ocr.recognize_text(paths=['/PATH/TO/IMAGE'])
    # pprint(result)
    rec = []
    for dic in result['data']:
        if dic['confidence'] < 0.8:
            continue
        rec.append((
            dic['text'].strip('0123456789'), 
            dic['text_box_position'][0][0]
        ))
    rec.sort(key=lambda x: x[1])
    records[file[:-4]].append([x[0] for x in rec])

pprint(records)