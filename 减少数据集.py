import os
import shutil
import random

# 定义源文件夹和目标文件夹
src_dir = "D:\\code\\yolo\\datasets\\SOD4BD-2"
dst_dir = "D:\\code\\yolo\\datasets\\SOD4BD-3"

# 获取源文件夹中的所有图片文件
src_images_dir = os.path.join(src_dir, "images", "train")
src_labels_dir = os.path.join(src_dir, "labels", "train")
src_images_files = [f for f in os.listdir(src_images_dir) if f.endswith('.jpg')]

# 随机选择60%的图片
selected_images_files = random.sample(src_images_files, int(len(src_images_files) * 0.6))

# 检查目标文件夹是否存在，如果不存在，创建它
dst_images_dir = os.path.join(dst_dir, "images", "train")
dst_labels_dir = os.path.join(dst_dir, "labels", "train")
os.makedirs(dst_images_dir, exist_ok=True)
os.makedirs(dst_labels_dir, exist_ok=True)

# 复制选定的图片和对应的标签文件到目标文件夹
for image_file in selected_images_files:
    label_file = image_file.replace('.jpg', '.txt')
    shutil.copy(os.path.join(src_images_dir, image_file), os.path.join(dst_images_dir, image_file))
    shutil.copy(os.path.join(src_labels_dir, label_file), os.path.join(dst_labels_dir, label_file))



# 获取源文件夹中的所有图片文件
src_images_dir = os.path.join(src_dir, "images", "val")
src_labels_dir = os.path.join(src_dir, "labels", "val")
src_images_files = [f for f in os.listdir(src_images_dir) if f.endswith('.jpg')]

# 随机选择60%的图片
selected_images_files = random.sample(src_images_files, int(len(src_images_files) * 0.6))

# 检查目标文件夹是否存在，如果不存在，创建它
dst_images_dir = os.path.join(dst_dir, "images", "val")
dst_labels_dir = os.path.join(dst_dir, "labels", "val")
os.makedirs(dst_images_dir, exist_ok=True)
os.makedirs(dst_labels_dir, exist_ok=True)

# 复制选定的图片和对应的标签文件到目标文件夹
for image_file in selected_images_files:
    label_file = image_file.replace('.jpg', '.txt')
    shutil.copy(os.path.join(src_images_dir, image_file), os.path.join(dst_images_dir, image_file))
    shutil.copy(os.path.join(src_labels_dir, label_file), os.path.join(dst_labels_dir, label_file))