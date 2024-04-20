import os
import shutil
import random

# 数据集路径
dataset_path = "D:\\code\\yolo\\datasets\\SOD4BD-2"

# 创建所需的文件夹
os.makedirs(os.path.join(dataset_path, "images", "train"), exist_ok=True)
os.makedirs(os.path.join(dataset_path, "images", "val"), exist_ok=True)
os.makedirs(os.path.join(dataset_path, "labels", "train"), exist_ok=True)
os.makedirs(os.path.join(dataset_path, "labels", "val"), exist_ok=True)

# 列出所有的图像文件
image_files = [f for f in os.listdir(os.path.join(dataset_path, "images")) if f.endswith(".jpg")]

# 随机打乱图像文件
random.shuffle(image_files)

# 取前80%的图像文件作为训练集
num_train = int(len(image_files) * 0.8)
train_files = image_files[:num_train]
val_files = image_files[num_train:]

# 将图像文件和对应的标签文件移动到相应的文件夹中
for filename in train_files:
    shutil.move(os.path.join(dataset_path, "images", filename), os.path.join(dataset_path, "images", "train", filename))
    shutil.move(os.path.join(dataset_path, "labels", filename.replace(".jpg", ".txt")), os.path.join(dataset_path, "labels", "train", filename.replace(".jpg", ".txt")))

for filename in val_files:
    shutil.move(os.path.join(dataset_path, "images", filename), os.path.join(dataset_path, "images", "val", filename))
    shutil.move(os.path.join(dataset_path, "labels", filename.replace(".jpg", ".txt")), os.path.join(dataset_path, "labels", "val", filename.replace(".jpg", ".txt")))