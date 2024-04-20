# import os
# import shutil
# import random
#
# # 源数据集和目标数据集的路径
# src_dataset_dir = "D:\\code\\yolo\\datasets\\DOTAv1.5"
# dst_dataset_dir = "D:\\code\\yolo\\datasets\\DOTAv1.5-T"
#
# # 获取每个子文件夹中的所有图片文件名
# def get_filenames(subfolder):
#     return os.listdir(os.path.join(src_dataset_dir, "images", subfolder))
#
# # 随机选择每个子文件夹中的10%的图片
# def select_files(filenames):
#     num_files = len(filenames)
#     num_select = int(num_files * 0.1)
#     return random.sample(filenames, num_select)
#
# # 复制选定的图片和对应的标签文件到新的文件夹
# def copy_files(subfolder, selected_files):
#     for filename in selected_files:
#         # 复制图片
#         src_image_path = os.path.join(src_dataset_dir, "images", subfolder, filename)
#         dst_image_path = os.path.join(dst_dataset_dir, "images", subfolder, filename)
#         shutil.copyfile(src_image_path, dst_image_path)
#
#         # 如果子文件夹不是'test'，则复制标签
#         if subfolder != 'test':
#             label_filename = filename.replace(".jpg", ".txt")
#             src_label_path = os.path.join(src_dataset_dir, "labels", subfolder, label_filename)
#             dst_label_path = os.path.join(dst_dataset_dir, "labels", subfolder, label_filename)
#             shutil.copyfile(src_label_path, dst_label_path)
#
# # 对每个子文件夹执行上述步骤
# for subfolder in ["test", "train", "val"]:
#     filenames = get_filenames(subfolder)
#     selected_files = select_files(filenames)
#     copy_files(subfolder, selected_files)


import os
import shutil
import random

# 源文件夹路径
src_image_dir = r"D:\code\yolo\datasets\SOD4BD\images"
src_label_dir = r"D:\code\yolo\datasets\SOD4BD\labels"

# 目标文件夹路径
dst_image_dir = r"D:\code\yolo\datasets\SOD4BD-1\images"
dst_label_dir = r"D:\code\yolo\datasets\SOD4BD-1\labels"

# 获取所有图片文件
image_files = [f for f in os.listdir(src_image_dir) if f.endswith('.jpg')]

# 随机选择文件
selected_files = random.sample(image_files, 500)

# 检查目标文件夹是否存在，如果不存在则创建
os.makedirs(dst_image_dir, exist_ok=True)
os.makedirs(dst_label_dir, exist_ok=True)

# 将选中的图片和标签文件复制到新的目录
for file in selected_files:
    # 复制图片文件
    shutil.copy(os.path.join(src_image_dir, file), dst_image_dir)

    # 复制对应的标签文件
    label_file = file.replace('.jpg', '.txt')
    shutil.copy(os.path.join(src_label_dir, label_file), dst_label_dir)