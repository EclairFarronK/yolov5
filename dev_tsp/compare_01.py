import cv2
import numpy as np
from skimage.metrics import mean_squared_error as compare_mse

# 加载两幅图像
image1 = cv2.imdecode(np.fromfile('./source/微信图片_20240701152345.jpg', dtype=np.uint8), cv2.IMREAD_COLOR)
image2 = cv2.imdecode(np.fromfile('./source/微信图片_20240701151835.jpg', dtype=np.uint8), cv2.IMREAD_COLOR)
# image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
# image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
# 确保两幅图像具有相同的尺寸
# if image1.shape != image2.shape:
#     image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))
# 计算 MSE
# mse = np.mean((image1 - image2) ** 2)
# print(f"MSE: {mse}")
mse2 = compare_mse(image1, image2)
print(f"MSE: {mse2}")
