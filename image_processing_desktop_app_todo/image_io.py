# 导入必要的模块
from image_utils import logging
from skimage import io  # skimage.io模块用于读写图像文件
import numpy as np

def load_image(image_path, as_gray=False):
    """
    从文件中载入图像。
    :param image_path: 图像文件路径
    :param as_gray: 是否以灰度图形式载入,默认为False
    :return: 载入的图像数据
    """
    try:
        logging.info(f"开始载入图像: {image_path}")  # 记录开始载入图像的日志
        
        # TODO: 载入图像文件的数据，如果as_gray为True，则载入灰度图像

        if as_gray:
            image = (io.imread(image_path,as_gray=True)*255).astype(np.uint8)
            # image = io.imread(image_path,as_gray=True)
        else:           
            image = io.imread(image_path)
 
        
        logging.info(f"成功载入图像: {image_path}")  # 记录成功载入图像的日志
        return image
    except Exception as e:
        logging.error(f"载入图像时发生错误: {e}")  # 记录载入图像时发生的错误
        return None

def save_image(image, save_path, format='png'):
    """
    将图像保存到文件
    :param image: 要保存的图像数据
    :param save_path: 保存文件的路径
    :param format: 保存图像的格式,默认为'png'
    """
    try:
        logging.info(f"开始保存图像: {save_path}")  # 记录开始保存图像的日志
        
        # TODO: 将图像 image 保存到文件 save_path
        # 将image(Numpy数组)图像 保存到文件 save_path
        io.imsave(save_path, image)
        
        logging.info(f"图像成功保存在: {save_path}")  # 记录成功保存图像的日志
    except Exception as e:
        logging.error(f"保存图像时发生错误: {e}")  # 记录保存图像时发生的错误