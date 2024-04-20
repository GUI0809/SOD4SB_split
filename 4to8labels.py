import os

def convert_to_yolo_format(label_dir):
    for filename in os.listdir(label_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(label_dir, filename), 'r') as f_in:
                lines = f_in.readlines()
            with open(os.path.join(label_dir, filename), 'w') as f_out:
                for line in lines:
                    data = line.strip().split()
                    cls = data[0]
                    cx = float(data[1])
                    cy = float(data[2])
                    w = float(data[3])
                    h = float(data[4])
                    # 计算四个角的坐标
                    x1 = cx - w / 2
                    y1 = cy - h / 2
                    x2 = cx + w / 2
                    y2 = cy - h / 2
                    x3 = cx + w / 2
                    y3 = cy + h / 2
                    x4 = cx - w / 2
                    y4 = cy + h / 2
                    # 将类别和四个角的坐标写入新的txt文件
                    f_out.write(f"{cls} {x1} {y1} {x2} {y2} {x3} {y3} {x4} {y4}\n")

convert_to_yolo_format("D:\\code\\yolo\\datasets\\SOD4BD-1\\labels")