# SOD4SB数据集处理

## 1. 数据集下载

数据集介绍地址：https://paperswithcode.com/dataset/sod4sb

下载地址：https://drive.google.com/drive/folders/1vTHiIelagbzPO795yhOdNUFh9u2XxZP-

## 2. 数据集格式转换
该数据集使用的是coco格式，需要将其转换为yolo格式，使用`coco2yolo.py`进行转换。

```
#这里根据自己的json文件位置，换成自己的就行
parser.add_argument('--json_path', default=r"D:\code\yolo\datasets\SOD4BD\annotations\merged_train.json",type=str, help="input: coco format(json)")
#这里设置.txt文件保存位置
parser.add_argument('--save_path', default=r"D:\code\yolo\datasets\SOD4BD\labels", type=str, help="specify where to save the output dir of labels")
```

将路径换成自己的路径即可。

## 3. 数据集抽样

考虑训练成本，仅选取了部分数据进行训练，这个依照个人需求选择是否进行数据集的缩减。ps：该数据集仅包含一个类别。
使用的是`随机选取图片和标签.py`进行数据集的抽样。

``````
# 随机选择文件,在此选择保留的图片张数
selected_files = random.sample(image_files, 500)
``````

## 4. 图像切割

使用`imagesplit_for4labels.py`进行图像切割，包括图像和标签

![3.png](img%2F3.png)

修改切割图片的参数

``basepath = 'example1'
    outpath = 'examplesplit'``
对应的原根目录和处理后的根目录
，对应的处理包括：图像切割，标签切割，标签坐标转换，去除不包含目标的图片和标签。

可以调用`测试标注是否正确.py`对转换后的标注进行测试。代码在处理边缘的目标时判断比较粗糙，可能存在目标在边缘边界框丢失的问题，可以根据自己的需求进行修改。

## 5. 数据集划分

使用`划分数据集.py`进行数据集的划分，包括训练集和测试集。


***注意：*** 上述对应的均为yolo格式标注，标注格式为：`class x_center y_center width height`，其中x_center,y_center,width,height均为相对于图像的比例。
代码参考：DOTA_devkit,其yolo格式标注和上述格式不同。