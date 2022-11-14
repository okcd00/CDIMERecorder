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
import win32gui
import win32api
import win32con
import numpy as np
from tqdm import tqdm
from PIL import Image, ImageGrab
from utils import PROJECT_PATH
from pykeyboard import PyKeyboard
from visual_residue import see_and_remember, time_identifier


class IMERecorder(object):
    EDITOR_WINDOW_NAME = '*new 1 - Notepad++'  # the editor window 
    RECORD_DIR_PATH = './records/'  # the path to store captures
    RECORD_OFFSETS = (66, 128, 1080, 172, 1080-66, 172-128)  # relative position x1, y1, x2, y2

    def __init__(self, debug=False) -> None:
        self.debug = debug
        self.project_path = PROJECT_PATH

        # member variables
        self.window_handle = None
        self.window_position = (0, 0, 0, 0)
        self.keyboard = PyKeyboard()

    def print(self, *args):
        if self.debug:
            print(*args)

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

    def _get_screenshot(self, dir_path, file_name, offsets=None, handle=None, postfix=None):
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
        img = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)
        img = Image.fromarray(img)
        return img

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
            if self.debug:
                print(e)
        return None, valid_flag

    def record_candidates(self, dir_name, file_name=None, offsets=None, postfix=None):
        if file_name is None:
            file_name = time_identifier()
        if offsets is None:
            offsets = self.RECORD_OFFSETS
        image = self._get_screenshot(
            dir_path=dir_name, file_name=file_name, 
            offsets=offsets, postfix=postfix)

        # 将截图保存到文件中
        self.save_fig(
            image=image, 
            save_dir=dir_name, 
            file_path=file_name,
            type_postfix='jpg', 
            quality=100)

    def __call__(self, input_sequence_list, record_page=10, editor_window=None, record_path=None):
        # set the editor foreground
        if editor_window is None:
            editor_window = self.EDITOR_WINDOW_NAME
        self.window_handle = self.find_handle(editor_window)
        # set the dump path
        if record_path is None:
            record_path = self.RECORD_DIR_PATH
        for _is in tqdm(input_sequence_list):
            self.set_foreground(self.window_handle)
            self.type_string(_is)
            for _page in range(record_page):
                self.record_candidates(
                    dir_name=record_path,
                    file_name=f"{_is}_page{_page}",
                    postfix=f"{_is}_page{_page}")
                time.sleep(0.1)
                self.page_down()
                time.sleep(0.3)
            time.sleep(0.5)
            self.clear_board()


if __name__ == "__main__":
    ir = IMERecorder(debug=True)
    ir(input_sequence_list=['chendian', 'jiayou', ])