# -*- coding: utf8 -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : visual_residue.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-02-20
#   desc     : remember what the eyes see in a few time.
# ==========================================================================
import os
import random
import datetime

import win32ui
import win32gui
import win32con
from ctypes import windll
from utils import PROJECT_PATH


def time_identifier(type_postfix=None, postfix=None):
    time_stamp = '{0:%m%d%H%M%S%f}'.format(datetime.datetime.now())[::-1]
    mask = map(lambda x: chr(ord(x[0]) + ord(x[1])), zip(time_stamp[::2], time_stamp[1::2]))
    t_id = ''.join(mask) + ''.join([str(random.randint(1, 10)) for _ in range(2)])
    return t_id + (postfix if postfix else '') + (type_postfix if type_postfix else '')


def see_and_remember(handle, dir_path, position_case=None, remove_title_bar=True, postfix=None, debug=False):
    # position and size
    if position_case is not None:
        left, top, right, bottom, width, height = position_case
    else:
        left, top, right, bottom = win32gui.GetWindowRect(handle)
        width, height = right - left, bottom - top

    # 创建设备描述表
    desktop_dc = win32gui.GetWindowDC(handle)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)

    # 创建内存设备描述表
    mem_dc = img_dc.CreateCompatibleDC()

    # 创建位图对象
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)

    # 截图至内存设备描述表
    remove_title_bar = int(remove_title_bar)
    mem_dc.BitBlt(
        (0, 0), (width, height),
        img_dc, (left, top), win32con.SRCCOPY)
        # img_dc, (0, 0), win32con.SRCCOPY)
    result = windll.user32.PrintWindow(handle, mem_dc.GetSafeHdc(), remove_title_bar)
    if debug:
        print('mem_dc.GetSafeHdc:', result)

    # 存入bitmap临时文件
    tmp_path = os.path.join(dir_path, time_identifier(postfix=postfix, type_postfix='.bmp'))

    if debug:
        print('save source to {}'.format(tmp_path))
    screenshot.SaveBitmapFile(mem_dc, tmp_path)
    # bmp_str = screenshot.GetBitmapBits(True)

    # 内存释放
    win32gui.DeleteObject(screenshot.GetHandle())
    mem_dc.DeleteDC()
    img_dc.DeleteDC()
    win32gui.ReleaseDC(handle, desktop_dc)
    return tmp_path


if __name__ == '__main__':
    pass