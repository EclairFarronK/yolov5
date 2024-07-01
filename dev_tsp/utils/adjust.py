import cv2
import numpy as np


def on_trackbar(val):
    pass


# 加载图像并转换为所选颜色空间
image = cv2.imread('2.png')
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 创建窗口并创建滑块
cv2.namedWindow('Thresholding')
cv2.createTrackbar('Hue Min', 'Thresholding', 0, 179, on_trackbar)
cv2.createTrackbar('Hue Max', 'Thresholding', 0, 179, on_trackbar)
cv2.createTrackbar('Saturation Min', 'Thresholding', 0, 255, on_trackbar)
cv2.createTrackbar('Saturation Max', 'Thresholding', 0, 255, on_trackbar)
cv2.createTrackbar('Value Min', 'Thresholding', 0, 255, on_trackbar)
cv2.createTrackbar('Value Max', 'Thresholding', 0, 255, on_trackbar)

while True:
    # 读取滑块值
    hue_min = cv2.getTrackbarPos('Hue Min', 'Thresholding')
    hue_max = cv2.getTrackbarPos('Hue Max', 'Thresholding')
    saturation_min = cv2.getTrackbarPos('Saturation Min', 'Thresholding')
    saturation_max = cv2.getTrackbarPos('Saturation Max', 'Thresholding')
    value_min = cv2.getTrackbarPos('Value Min', 'Thresholding')
    value_max = cv2.getTrackbarPos('Value Max', 'Thresholding')

    # 设定下界和上界阈值
    lowerb = np.array([hue_min, saturation_min, value_min])
    upperb = np.array([hue_max, saturation_max, value_max])

    # 应用颜色范围阈值
    mask = cv2.inRange(hsv_image, lowerb, upperb)

    # 显示阈值图像
    cv2.imshow('Thresholding', mask)

    # 按下 ESC 键退出循环
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
