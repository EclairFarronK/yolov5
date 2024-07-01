import numpy as np
import cv2
# 用来截屏
import mss
from PIL import Image

with mss.mss() as sct:
    # 抓取全屏幕幕截图
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    img = np.array(sct.grab(monitor))

    # 将图像从BGR格式转换为RGB格式
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 将图像保存为图片
    im = Image.fromarray(img)
    im.save("screenshot.png")
