# Image Processor
- Image Processor 是一个用于处理图像的 Python 应用程序。它提供了一系列的图像处理功能，包括打开原始图像，打开灰度图像，合并通道，保存当前图像等。

## 代码效果视频: 图像处理APP（基础处理）
链接：https://lusun.com/v/WEVdJLzEKFG

## 文件结构
- `main.py`: 应用程序的主入口文件。
- `image_io.py`: 处理图像输入输出的相关代码。
- `image_channels.py`: 处理图像通道的相关代码。
- `image_transform.py`: 处理图像转换的相关代码。
- `image_utils.py`: 图像处理的工具函数。
- `language.json`: 应用程序的多语言支持文件。
- `config.py`: 配置文件。
- `readme.md`: 项目的说明文件。
- `tests/`: 包含所有测试图片文件
  - `dog.jpg` RGB图
  - `dog_gray.jpg` 单通道灰度图
  - `dog_0.jpg`，`dog_1.jpg`，`dog_2.jpg` R,G,B通道单通道灰度图

## 环境需求
本项目需要在Python 3.x环境下运行,并需要安装以下库:
- tkinter (通常包含在Python标准库中)
- Pillow (PIL)
- numpy
- scikit-image (skimage)

可以使用以下命令确保在运行项目之前已经安装了所有必需的库。
```bash
pip install scikit-image
```


## 如何运行
```python
python main.py
```

## 项目中的 `#TODO`
对应**Numpy图像处理基础**部分课程内容，在以下函数中对应有 `#TODO` 的内容需要完成
- `main.py`
  - `show_image_details` 获取图像Numpy数组的基本属性
- `image_io.py`
  - `save_image` 把Numpy数组图像保存到硬盘
  - `load_image` 从硬盘载入图像到Numpy数组中
- `image_transform.py`
  - `crop_image` 对图像Numpy数组切片实现裁剪功能
- `image_channels.py`
  - `merge_image_channels` 合并多通道子图
  - `split_image_channels` 拆分多通道图的所有子图

## 个人信息
[TODO: 此处填写个人信息]
- 学号: 202252320419
- 年级: 2022
- 专业: 智能科学与技术
- 班级: 4 班

