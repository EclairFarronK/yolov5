import time

import cv2
import numpy as np
import win32gui
from PIL import ImageGrab
from mss import mss


#
def active_windows(title):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd != 0:
        win32gui.SetForegroundWindow(hwnd)
        return 'active_success'
    else:
        return False


name = '百度一下，你就知道 - Chrome'
print(active_windows(name))
cv2.namedWindow('windows', cv2.WINDOW_NORMAL)
while True:
    screenshot_count = 1
    # name = '有道云笔记'
    nam = win32gui.FindWindow(None, name)
    window_x, window_y, window_width, window_height = win32gui.GetWindowRect(nam)
    # todo 解决有可能出现窗口还没出来就截屏的情况？因为异步的原因吗？
    # time.sleep(1)

    # 以下任选其一
    screenshot = ImageGrab.grab(bbox=(window_x * 1.25, window_y * 1.25, window_width * 1.25, window_height * 1.25))
    # screenshot = ImageGrab.grab(bbox=(window_x, window_y, window_width, window_height))

    # method1
    scr = np.array(screenshot)
    # 将图像从BGR格式转换为RGB格式
    scr = cv2.cvtColor(scr, cv2.COLOR_BGR2RGB)
    # todo cv2.imshow会出现很多个窗口吗？
    cv2.imshow('windows', scr)

    # method2
    # bbox = {'top': int(window_x * 1.25), 'left': int(window_y * 1.25), 'width': int(window_width * 1.25),
    #         'height': int(window_height * 1.25)}
    # sct = mss()
    # screen = sct.grab(bbox)
    # scr = np.array(screen)
    # cv2.imshow('window', scr)

    # 用来退出
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

    # 用来保存图片
    screenshot.save(f'data\screenshot_{screenshot_count}.png')
    screenshot_count += 1
    print("截图已保存")
cv2.destroyAllWindows()
