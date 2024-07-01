import numpy as np
import cv2
import mss
from PIL import Image

with mss.mss() as sct:
    # 获取屏幕大小
    width, height = sct.monitors[0]["width"], sct.monitors[0]["height"]
    # 宽
    print(width)
    # 高
    print(height)

    # 计算要截取的区域
    left = int(width * 0.25)
    top = int(height * 0.25)
    right = int(width * 0.75)
    bottom = int(height * 0.75)

    # 抓取画面中心区域截图
    monitor = {"top": top, "left": left, "width": right - left, "height": bottom - top}
    img = np.array(sct.grab(monitor))

    # 将图像从BGR格式转换为RGB格式
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 将图像保存为图片
    im = Image.fromarray(img)
    im.save("screenshot.png")
