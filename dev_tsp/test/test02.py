import numpy as np

# 创建第一个三维矩阵
# matrix1 = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
# # 创建第二个三维矩阵
# matrix2 = np.array([[[13, 14, 15], [16, 17, 18]], [[19, 20, 21], [22, 23, 24]]])
# # 矩阵转置，将后面两个维度互换
# matrix2 = np.transpose(matrix2, (1,0))
# print("第一个三维矩阵：\n", matrix1)
# print("第二个三维矩阵：\n", matrix2)
# matrix3 = np.matmul(matrix1, matrix2)
# print("第三个三维矩阵：\n", matrix3)

matrix1 = np.array([[1, 2, 3], [4, 5, 6]])
print(matrix1)
matrix2 = np.transpose(matrix1, (1, 0))
print(matrix2)
