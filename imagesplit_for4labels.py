import glob
import os
import codecs
import shutil
import sys
import numpy as np
import math
import cv2
import shapely.geometry as shgeo
import copy
import time
from tqdm import tqdm


# 删除文件夹中的所有文件
def delete_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def custombasename(fullname):
    return os.path.basename(os.path.splitext(fullname)[0])


def parse_dota_poly(filename):
    """


        0 0.345052 0.603009 0.010937 0.014352
        0 0.372135 0.605324 0.010937 0.011574
    """
    objects = []
    f = []
    if (sys.version_info >= (3, 5)):
        fd = open(filename, 'r')
        f = fd
    elif (sys.version_info >= 2.7):
        fd = codecs.open(filename, 'r')
        f = fd
    # count = 0
    while True:
        line = f.readline()
        if line:
            splitlines = line.strip().split(' ')
            object_struct = {}

            if len(splitlines) != 5:
                # 抛出警告
                print('warning: in %s, 标签维度有问题' % filename)
                continue
            if len(splitlines) == 5:
                object_struct['name'] = splitlines[0]
                object_struct['poly'] = [float(splitlines[1]), float(splitlines[2]), float(splitlines[3]),
                                         float(splitlines[4])]

            objects.append(object_struct)
        else:
            break
    return objects


def parse_dota_poly2(filename):
    """
        0 0.345052 0.603009 0.010937 0.014352
    """
    objects = parse_dota_poly(filename)
    for obj in objects:
        obj['poly'] = list(map(float, obj['poly']))
    return objects


# 获取图片的列表
def GetFileFromThisRootDir(dir, ext=None):
    allfiles = []
    needExtFilter = (ext != None)
    for root, dirs, files in os.walk(dir):
        for filespath in files:
            filepath = os.path.join(root, filespath)
            extension = os.path.splitext(filepath)[1][1:]
            if needExtFilter and extension in ext:
                allfiles.append(filepath)
            elif not needExtFilter:
                allfiles.append(filepath)
    return allfiles


def cal_line_length(point1, point2):
    return math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2))


def del_x(label_dir, image_dir):
    # 获取所有的txt文件
    txt_files = glob.glob(os.path.join(label_dir, "*.txt"))

    for txt_file in txt_files:
        # 读取文件的每一行
        with open(txt_file, 'r') as f:
            lines = f.readlines()
        # 检查是否存在符合条件的行
        valid_lines = [line for line in lines if len(line.strip().split()) == 5]
        if not valid_lines:
            # 删除txt文件
            os.remove(txt_file)
            # 删除对应的jpg文件
            jpg_file = os.path.join(image_dir, os.path.splitext(os.path.basename(txt_file))[0] + ".jpg")
            if os.path.exists(jpg_file):
                os.remove(jpg_file)


class splitbase():
    def __init__(self,
                 basepath,
                 outpath,
                 code='utf-8',
                 gap=100,                          # 修改重叠的像素大小
                 subsize=640,                     # 修改分割图片的尺寸大小
                 thresh=0.7,
                 ext='.jpg'
                 ):
        """
        :param basepath: base path for dota data
        :param outpath: output base path for dota data,
        the basepath and outputpath have the similar subdirectory, 'images' and 'labels'
        :param code: encodeing format of txt file
        :param gap: overlap between two patches
        :param subsize: subsize of patch
        :param thresh: the thresh determine whether to keep the instance if the instance is cut down in the process of split
        :param choosebestpoint: used to choose the first point for the
        :param ext: ext for the image format
        """
        self.basepath = basepath
        self.outpath = outpath
        self.code = code
        self.gap = gap
        self.subsize = subsize
        self.slide = self.subsize - self.gap
        self.thresh = thresh
        self.imagepath = os.path.join(self.basepath, 'images')
        self.labelpath = os.path.join(self.basepath, 'labels')
        self.outimagepath = os.path.join(self.outpath, 'images')
        self.outlabelpath = os.path.join(self.outpath, 'labels')
        # self.choosebestpoint = choosebestpoint
        self.ext = ext
        if not os.path.exists(self.outimagepath):
            os.makedirs(self.outimagepath)
        if not os.path.exists(self.outlabelpath):
            os.makedirs(self.outlabelpath)

    def polyorig2sub(self, left, up, poly):
        polyInsub = np.zeros(len(poly))
        for i in range(int(len(poly) / 2)):
            polyInsub[i * 2] = float(poly[i * 2] - left)
            polyInsub[i * 2 + 1] = float(poly[i * 2 + 1] - up)
        return polyInsub

    def calchalf_iou(self, poly1, poly2):
        """
            It is not the iou on usual, the iou is the value of intersection over poly1
        """
        inter_poly = poly1.intersection(poly2)
        inter_area = inter_poly.area
        poly1_area = poly1.area
        half_iou = inter_area / poly1_area
        return inter_poly, half_iou

    def saveimagepatches(self, img, subimgname, left, up):
        subimg = copy.deepcopy(img[up: (up + self.subsize), left: (left + self.subsize)])
        outdir = os.path.join(self.outimagepath, subimgname + self.ext)
        cv2.imwrite(outdir, subimg)

    def GetPoly4FromPoly5(self, poly):
        distances = [cal_line_length((poly[i * 2], poly[i * 2 + 1]), (poly[(i + 1) * 2], poly[(i + 1) * 2 + 1])) for i
                     in range(int(len(poly) / 2 - 1))]
        distances.append(cal_line_length((poly[0], poly[1]), (poly[8], poly[9])))
        pos = np.array(distances).argsort()[0]
        count = 0
        outpoly = []
        while count < 5:
            # print('count:', count)
            if (count == pos):
                outpoly.append((poly[count * 2] + poly[(count * 2 + 2) % 10]) / 2)
                outpoly.append((poly[(count * 2 + 1) % 10] + poly[(count * 2 + 3) % 10]) / 2)
                count = count + 1
            elif (count == (pos + 1) % 5):
                count = count + 1
                continue

            else:
                outpoly.append(poly[count * 2])
                outpoly.append(poly[count * 2 + 1])
                count = count + 1
        return outpoly

    def savepatches(self, resizeimg, objects, subimgname, left, up, right, down):
        l = left
        u = up
        weight = np.shape(resizeimg)[1]
        height = np.shape(resizeimg)[0]
        outdir = os.path.join(self.outlabelpath, subimgname + '.txt')
        mask_poly = []
        imgpoly = shgeo.Polygon([(left, up), (right, up), (right, down),
                                 (left, down)])
        with codecs.open(outdir, 'w', self.code) as f_out:
            for obj in objects:
                # 由[x1,y1,w,h]转换得到四个坐标点
                cx = float(obj['poly'][0])
                cy = float(obj['poly'][1])
                w = float(obj['poly'][2])
                h = float(obj['poly'][3])
                # 计算四个角的坐标
                x1 = int((cx - w / 2) * weight)
                y1 = int((cy - h / 2) * height)
                x2 = int((cx + w / 2) * weight)
                y2 = int((cy - h / 2) * height)
                x3 = int((cx + w / 2) * weight)
                y3 = int((cy + h / 2) * height)
                x4 = int((cx - w / 2) * weight)
                y4 = int((cy + h / 2) * height)
                gtpoly = shgeo.Polygon([(x1, y1),
                                        (x2, y2),
                                        (x3, y3),
                                        (x4, y4)])
                if (gtpoly.area <= 0):
                    continue
                inter_poly, half_iou = self.calchalf_iou(gtpoly, imgpoly)

                if (half_iou == 1):
                    # 将坐标转换到分割后的图像的坐标系
                    cx = (cx * weight - left) / self.subsize
                    cy = (cy * height - up) / self.subsize
                    w = w * weight / self.subsize
                    h = h * height / self.subsize
                    outline = '0 ' + ' '.join([str(cx), str(cy), str(w), str(h)])
                    f_out.write(outline + '\n')
                elif half_iou > 0:
                    if cx > right or cx < left or cy > down or cy < up:
                        continue
                    else:
                        # 将坐标转换到分割后的图像的坐标系
                        cx = (cx * weight - left) / self.subsize
                        cy = (cy * height - up) / self.subsize
                        w = w * weight / self.subsize
                        h = h * height / self.subsize
                        outline = '0 ' + ' '.join([str(cx), str(cy), str(w), str(h)])
                        f_out.write(outline + '\n')

        self.saveimagepatches(resizeimg, subimgname, l, u)

    def SplitSingle(self, name, extent):
        """
            split a single image and ground truth
        :param name: image name
        :param extent: the image format
        :return:
        """
        start_time = time.time()
        img = cv2.imread(os.path.join(self.imagepath, name + extent))
        if np.shape(img) == ():
            return
        fullname = os.path.join(self.labelpath, name + '.txt')
        objects = parse_dota_poly2(fullname)
        # for obj in objects:
        #     obj['poly'] = list(map(lambda x: rate * x, obj['poly']))
        #     # obj['poly'] = list(map(lambda x: ([2 * y for y in x]), obj['poly']))

        # else:
        resizeimg = img
        outbasename = name + '__'
        weight = np.shape(resizeimg)[1]
        height = np.shape(resizeimg)[0]

        left, up = 0, 0
        while (left < weight):
            if (left + self.subsize >= weight):
                left = max(weight - self.subsize, 0)
            up = 0
            while (up < height):
                if (up + self.subsize >= height):
                    up = max(height - self.subsize, 0)
                right = min(left + self.subsize, weight - 1)
                down = min(up + self.subsize, height - 1)
                subimgname = outbasename + str(left) + '__' + str(up)
                # self.f_sub.write(name + ' ' + subimgname + ' ' + str(left) + ' ' + str(up) + '\n')
                self.savepatches(resizeimg, objects, subimgname, left, up, right, down)
                if (up + self.subsize >= height):
                    break
                else:
                    up = up + self.slide
            if (left + self.subsize >= weight):
                break
            else:
                left = left + self.slide
        end_time = time.time()
        elapsed_time = end_time - start_time
        return elapsed_time

    def splitdata(self):

        imagelist = GetFileFromThisRootDir(self.imagepath)
        imagenames = [custombasename(x) for x in imagelist if (custombasename(x) != 'Thumbs')]
        total_time = 0
        for name in tqdm(imagenames):
            elapsed_time = self.SplitSingle(name, self.ext)
            total_time += elapsed_time
        print("预计剩余时间：", total_time / len(imagenames) * (len(imagenames) - len(tqdm(imagenames))))


# if __name__ == '__main__':
#
#     # 先删除之前的数据
#     delete_files_in_folder(r"D:\code\yolo\datasets\SOD4BD-2\labels")
#     delete_files_in_folder(r"D:\code\yolo\datasets\SOD4BD-2\images")
#
#     split = splitbase(r"D:\code\yolo\datasets\SOD4BD-1",
#                       r"D:\code\yolo\datasets\SOD4BD-2")
#     split.splitdata()
#     # 将没有对象的图片删除
#     del_x(r"D:\code\yolo\datasets\SOD4BD-2\labels", r"D:\code\yolo\datasets\SOD4BD-2\images")

if __name__ == '__main__':

    basepath = 'example1'
    outpath = 'examplesplit'

    output_labels_dir = outpath + r"\labels"
    output_images_dir = outpath + r"\images"

    # 检查文件夹是否存在，如果不存在则创建
    if not os.path.exists(output_labels_dir):
        os.makedirs(output_labels_dir)
    if not os.path.exists(output_images_dir):
        os.makedirs(output_images_dir)

    # 检查文件夹是否为空
    if not os.listdir(output_labels_dir):
        pass
    else:
        delete_files_in_folder(output_labels_dir)

    if not os.listdir(output_images_dir):
        pass
    else:
        delete_files_in_folder(output_images_dir)

    split = splitbase(basepath, outpath)
    split.splitdata()

    # 将没有对象的图片删除
    del_x(output_labels_dir, output_images_dir)
