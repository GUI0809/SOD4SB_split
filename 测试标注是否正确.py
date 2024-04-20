import cv2
import numpy as np

# img = cv2.imread(r"D:\code\yolo\datasets\SOD4BD-1\images\00026.jpg")
# h, w, _ = img.shape
#
#
# # yolo标注数据文件名为786_rgb_0616.txt
# with open(r"D:\code\yolo\datasets\SOD4BD-1\labels\00026.txt", 'r') as f:
# 	temp = f.read()
# 	temp = temp.split()
# 	# ['1', '0.43906', '0.52083', '0.34687', '0.15']
#
# # 4
# # # 根据第1部分公式进行转换
# # x_, y_, w_, h_ = eval(temp[1]), eval(temp[2]), eval(temp[3]), eval(temp[4])
# #
# # x1 = w * x_ - 0.5 * w * w_
# # x2 = w * x_ + 0.5 * w * w_
# # y1 = h * y_ - 0.5 * h * h_
# # y2 = h * y_ + 0.5* h * h_
# #
# # # 画图验证，注意画图坐标要转换成int格式
# # cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0))
#
# # 定义四个点
# pts = np.array([[temp[1]*w, temp[2]*h], [temp[3]*w, temp[4]*h], [temp[5]*w, temp[6]*h], [temp[7]*w, temp[8]*h]], np.int32)
#
# # 重塑为形状 (number_vertex, 1, 2)
# pts = pts.reshape((-1, 1, 2))
#
# # 绘制多边形
# cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=3)
#
#
# # cv2.imshow('windows', img)
# cv2.imwrite('./re.jpg',img)
# cv2.waitKey(0)



import cv2
import numpy as np

# # 加载图片
# img = cv2.imread(r"examplesplit/images/00017__924__924.jpg")
#
# # 读取标记
# with open(r"examplesplit/labels/00017__924__924.txt", 'r') as f:
#     lines = f.readlines()
#
# labels = []
# for line in lines:
#     labels.append(list(map(float, line.strip().split())))
#
# # 获取图片的宽度和高度
# h, w = img.shape[:2]
#
# for label in labels:
#     # 将标记框的坐标转换为像素坐标
#     pts = np.array([[int(label[i]*w), int(label[i+1]*h)] for i in range(1, len(label), 2)], np.int32)
#     # 重塑为形状 (number_vertex, 1, 2)
#     pts = pts.reshape((-1, 1, 2))
#     # 绘制多边形
#     cv2.polylines(img, [pts], isClosed=True, color=(0, 0, 255), thickness=2)
#
# # 保存做完标记的图片
# cv2.imwrite('image_with_boxes.jpg', img)


# x1 y1 w h
import cv2
import matplotlib.pyplot as plt

# 读取图像
img = cv2.imread(r"D:\code\yolo\datasets\SOD4BD-2\images\02987__1620__1520.jpg")  # 替换为你的图像文件路径
height, width, _ = img.shape

# 读取标记数据
with open(r"D:\code\yolo\datasets\SOD4BD-2\labels\02987__1620__1520.txt", 'r') as f:
    lines = f.readlines()

for line in lines:
    # 解析数据
    parts = line.strip().split()
    cls, x_center, y_center, w, h = int(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])

    # 计算边框的左上角和右下角坐标
    x1 = int((x_center - w / 2) * width)
    y1 = int((y_center - h / 2) * height)
    x2 = int((x_center + w / 2) * width)
    y2 = int((y_center + h / 2) * height)

    # 在图像上绘制边框
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 使用绿色绘制边框

# 保存并显示图像
cv2.imwrite('output.jpg', img)  # 保存图像
