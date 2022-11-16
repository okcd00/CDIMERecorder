# -*- coding: utf8 -*-
# ==========================================================================
#   Copyright (C) since 2022 All rights reserved.
#
#   filename : ime_recorder.py
#   author   : chendian / okcd00@qq.com
#   date     : 2022-11-14
#   desc     : 
# ==========================================================================
import os
import sys
import time
sys.path.append('./')
sys.path.append('../')

# main packages
import re
import cv2
import win32gui
# import pywinauto
import itertools
import numpy as np
import paddlehub as hub
from tqdm import tqdm
from PIL import Image, ImageGrab
from utils import *
from pprint import pprint
from file_io import load_json, dump_json
from pypinyin import pinyin, Style
from pykeyboard import PyKeyboard  # PyUserInput


class IMERecorder(object):
    EDITOR_WINDOW_NAME = '*new 1 - Notepad++'  # the editor window 
    RECORD_DIR_PATH = './records/'  # the path to store captures

    # relative position x1, y1, x2, y2
    # Microsoft IME
    RECORD_OFFSETS = (66, 128, 1024, 172, 1024-66, 172-128)  

    def __init__(self, debug=False, use_ocr=True) -> None:
        self.debug = debug
        self.project_path = PROJECT_PATH

        # member variables
        self.window_handle = None
        self.window_position = (0, 0, 0, 0)
        self.keyboard = PyKeyboard()


        self.ocr = None
        self.records = {}
        if use_ocr:
            self.ocr = hub.Module(
                name="chinese_ocr_db_crnn_server", 
                enable_mkldnn=False)

    def print(self, *args):
        if self.debug:
            print(*args)

    def pprint(self, *args):
        if self.debug:
            pprint(*args)

    def find_handle(self, window_name):
        self.window_handle = win32gui.FindWindow(None, window_name)
        self.window_position = win32gui.GetWindowRect(self.window_handle)
        self.print(f"Loaded the handle {self.window_handle} for {window_name}")
        return self.window_handle

    def set_foreground(self, handle=None):
        if handle is None:
            handle = self.window_handle
        # win32api.keybd_event(13, 0, 0, 0)  # send an enter
        win32gui.SetForegroundWindow(handle)

    def _keys(self, key):
        if key.lower().startswith('ctrl+'):
            return [self.keyboard.control_key, key[5:]]
        if key.lower().startswith('alt+'):
            return [self.keyboard.alt_key, key[4:]]
        if re.match('^f[0-9]{1,2}$', key.lower()):
            return [self.keyboard.function_keys[int(key[1:])]]
        if key.lower().startswith('num'):
            if key[3:].isdigit():
                return [self.keyboard.numpad_keys[int(key[3:])]]
            return [self.keyboard.numpad_keys[key[3:]]]
        return [key]

    def type_string(self, input_sequence, interval=0.2):
        self.keyboard.type_string(input_sequence, interval=interval)

    def page_down(self):
        # press and release
        self.keyboard.tap_key(']', n=1, interval=0.1)

    def clear_board(self):
        self.keyboard.tap_key(self.keyboard.backspace_key, n=25, interval=0.1)

    def _get_screenshot(self, offsets=None, handle=None, postfix=None):
        if handle is None:
            handle = self.window_handle
        
        left, top, right, bottom = win32gui.GetWindowRect(handle)
        width, height = right - left, bottom - top
        position_case = [left, top, right, bottom, width, height]
        # print(left, top, right, bottom)

        if offsets:
            position_case = (
                left + offsets[0],
                top + offsets[1],
                left + offsets[2],
                top + offsets[3],
                offsets[4], offsets[5]
            )

        img = ImageGrab.grab(bbox=position_case[:4])
        img = np.array(img.getdata(), np.uint8).reshape(
            img.size[1], img.size[0], 3)
        img = Image.fromarray(img)
        return img

    def recognize_text(self, images):
        if self.ocr is None:
            return []
        if not isinstance(images, list):
            images = [images]

        images = [cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR) for img in images]
        # PaddleHub needs cv2.Image
        results = self.ocr.recognize_text(images=images)
        # results = self.ocr.recognize_text(images=[cv2.imread(file_path)])
        return results

    def save_fig(self, image, save_dir, file_path, type_postfix='jpg', quality=100):
        form_dict = {
            'jpg': 'JPEG',
            'png': 'PNG'
        }
        image.save(fp=os.path.join(save_dir, f"{file_path}.{type_postfix}"), 
                   format=form_dict.get(type_postfix), quality=quality)

    def load_fig(self, path):
        valid_flag = True
        try:
            image = Image.open(path)
            return image, valid_flag
        except Exception as e:
            valid_flag = False
            self.print(e)
        return None, valid_flag

    def record_candidates(self, dir_name=None, file_name=None, offsets=None, postfix=None, save_img=False):
        if offsets is None:
            offsets = self.RECORD_OFFSETS
        image = self._get_screenshot(
            offsets=offsets, postfix=postfix)

        # 将截图保存到文件中
        if save_img:
            self.save_fig(
                image=image, 
                save_dir=dir_name, 
                file_path=file_name,
                type_postfix='jpg', 
                quality=100)

        return image

    def extract_from_ocr_results(self, results, input_sequence=None):
        candidates = []

        def dfs(arr):
            _ret = []
            if len(arr) == 1:
                return arr[0]
            for cur in arr[0]:
                for post_arr in dfs(arr[1:]):
                    _ret.append(cur+post_arr)
            return _ret
                
        for result in results:
            rec = []
            for dic in result['data']:
                candidate = dic['text'].strip('0123456789 ')
                if 1 - dic['confidence'] > len(candidate) * 0.1:
                    continue
                if candidate:
                    if input_sequence:
                        token_pinyins = pinyin(
                            candidate, heteronym=True, 
                            style=Style.NORMAL)
                        pinyins = dfs(token_pinyins)
                        # self.print(candidate, pinyins)
                        failed_match = input_sequence not in pinyins 
                        failed_partly = not any([_py in input_sequence for _py in pinyins])
                        if failed_match and failed_partly:
                            continue
                    # text candidate, confidence, position
                    rec.append((
                        candidate, 
                        dic['confidence'],
                        dic['text_box_position'][0][0]))
            rec.sort(key=lambda x: x[2])  # sort by x-position
            candidates.extend([x[0] for x in rec])
        return candidates

    def arrange_records(self, records):
        records = {k: stable_unique(v) for k, v in records.items()}
        return records

    def dump_records(self, record_path):
        # record_path is a directory
        file_path = 'input_candidates_{}.{}'.format(
                time.strftime('%y%m%d_%H%M%S', time.localtime()), 'json')
        # arrange records for repeat candidates
        self.records = self.arrange_records(self.records)
        dump_path = os.path.join(record_path, file_path)
        dump_json(obj=self.records, fp=dump_path)

    def load_records(self, record_path):
        # record_path is a file
        self.records = load_json(record_path)

    def __call__(self, input_sequence_list, 
                 record_page=10, 
                 save_img=False,
                 editor_window=None, 
                 record_path=None,
                 update_mode='skip',
                 save_per_item=-1):
        # set the editor foreground
        if editor_window is None:
            editor_window = self.EDITOR_WINDOW_NAME
        self.window_handle = self.find_handle(editor_window)
        # set the dump path
        if record_path is None:
            record_path = self.RECORD_DIR_PATH
        # for each input sequence, record the candidates.
        for _is_index, _is in tqdm(enumerate(input_sequence_list)):
            if _is in self.records:
                if update_mode in ['skip']:
                    continue
            self.set_foreground(self.window_handle)
            self.type_string(_is)
            # win_panel = pywinauto.findwindows.find_windows(
            #     title="CandidateWindow", control_type="Pane",backend="uia")
            # print(win_panel.Texts())  # <= timeout here
            # print("Done here")
            images = []
            for _page in range(record_page):
                time.sleep(0.2)
                image = self.record_candidates(
                    dir_name=record_path,
                    file_name=f"{_is}_page{_page}",
                    postfix=f"{_is}_page{_page}",
                    save_img=save_img,
                )
                if images and image == images[-1]:
                    break
                images.append(image)
                time.sleep(0.1)
                self.page_down()
                time.sleep(0.1)
            self.clear_board()
            if self.ocr is not None:
                ocr_results = self.recognize_text(images)
                candidates = self.extract_from_ocr_results(ocr_results, input_sequence=_is)
                self.records.setdefault(_is, [])
                self.records[_is].extend(candidates)
                self.print('\n', _is, candidates)
            if 0 < save_per_item <= _is_index and _is_index % save_per_item == 0:
                self.dump_records(self.records, record_path)
        else:
            self.dump_records(self.records, record_path)
            self.print("Finished at:", time.ctime())


def record_single_char_words():
    ir = IMERecorder(debug=False)
    ir.load_records('./records/input_candidates_221115_173927.json')
    py_list = [line.strip() for line in open('./data/vocab_pinyin.txt', 'r') 
               if not line.startswith('[')]
    # test_list = ['wo', 'chendian', 'yaojiayou']
    ir(input_sequence_list=py_list)


def record_double_char_words():
    ir = IMERecorder(debug=True)
    ir.load_records('./records/input_candidates_221115_203841.json')
    py_list = [line.strip() for line in open('./data/vocab_pinyin.txt', 'r') 
               if not line.startswith('[')]
    double_word_py_list = [f'{a}{b}' for a, b in itertools.product(py_list, py_list)]
    # test_list = ['wo', 'chendian', 'yaojiayou']
    ir(input_sequence_list=double_word_py_list, 
       record_page=5, save_per_item=100)


if __name__ == "__main__":
    record_double_char_words()
