import cv2
import numpy as np
import os
from skimage.metrics import mean_squared_error as compare_mse


def mse(img1, img2):
    # 将图像转换为灰度图像
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    print(gray_img2.__class__)
    if gray_img1.shape[0] != gray_img2.shape[0]:
        gray_img2 = gray_img2.T
    # 当转置解决不了的时候，去resize
    # 计算图像的均值和方差
    # mean1, mean2 = np.mean(gray_img1), np.mean(gray_img2)
    # var1, var2 = np.var(gray_img1), np.var(gray_img2)

    # 计算协方差和SSIM指数
    # cov = np.cov(gray_img1.flatten(), gray_img2.flatten())[0, 1]
    # c1 = (0.01 * 255) ** 2
    # c2 = (0.03 * 255) ** 2
    # ssim = (2 * mean1 * mean2 + c1) * (2 * cov + c2) / ((mean1 ** 2 + mean2 ** 2 + c1) * (var1 + var2 + c2))
    mse = compare_mse(gray_img1, gray_img2)
    return mse


if __name__ == '__main__':
    folder_path = './source/徐涛照片'
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        image1 = cv2.imdecode(np.fromfile(folder_path + '/' + file_names[0], dtype=np.uint8), cv2.IMREAD_COLOR)
        image2 = cv2.imdecode(np.fromfile(folder_path + '/' + file_name, dtype=np.uint8), cv2.IMREAD_COLOR)
        print(image1.shape, ' ', image2.shape)
        ssim_index = mse(image1, image2)
        # if ssim_index > 0.5:
        print("SSIM Index:", ssim_index, ' ', file_name)
        # print(file_name)
    # 第一张图片和之后的每一张对比

    # 将所有的图片放到一个文件夹里面

    # 递归

    # 读取两幅图像

    # image3 = cv2.imdecode(np.fromfile('./source/微信图片_20240701151835.jpg', dtype=np.uint8), cv2.IMREAD_COLOR)
    # image4 = cv2.imdecode(np.fromfile('./source/微信图片_20240701152345.jpg', dtype=np.uint8), cv2.IMREAD_COLOR)
    #
    # # 计算两幅图像的SSIM指数
    # ssim_index = ssim(image3, image4)
    #
    # # 打印SSIM指数
    # print("SSIM Index:", ssim_index)
