import numpy as np
import image_io #导入image_io模块(image_io.py文件)
from image_utils import logging


def split_image_channels(image):
    '''
    该函数用于分割图像的颜色通道
    :param image: 输入图像,numpy数组
    :return: 图像的颜色通道列表
    '''
    try:
        logging.info("开始分割图像颜色通道")
        
        # TODO: 1. 检测多通道图像 image 是否真多通道的，如果是，显示错误信息并返回
        # 提示: 使用 raise 抛出异常信息：图像通道数必须大于等于2
        """ 如果 image.ndim < 3 
        那么image就没有足够的维度来表示一个图像（至少需要两个维度来表示图像的高度和宽度，
        还需要一个维度来表示颜色通道）
        如果 image.shape[2] < 2
        那么image就没有足够的颜色通道。
        """
        if image.ndim < 3 or image.shape[2] < 2:
            raise ValueError("图像通道数必须大于等于2")
        
        
        # TODO: 2. 使用numpy的split函数，沿着通道维度分割图像
        """
        第一个参数 image 为要分割的数组 (image)
        image.shape[2],即image的第三个维度的大小,也就是颜色通道的数量。
        参数axis=2表示沿着第三个维度进行分割。
        """
        channel_list_1 = np.split(image, image.shape[2], axis=2)
        
        
        # TODO: 3. 把分割后的通道图像添加到一个列表 channel_list 中，注意要去掉多余的维度
        """np.squeeze用于将每个颜色通道的数组从三维降低到二维。
        如果一个颜色通道的数组的形状是(height, width, 1)
        那么np.squeeze会将其形状改为(height, width)"""
        # channel_list = [np.squeeze(channel) for channel in channel_list]
        channel_list = [np.squeeze(channel) for channel in channel_list_1]
        
        logging.info(f"成功分割图像颜色通道")
        return channel_list
    except Exception as e:
        # print(f"在分割图像颜色通道时发生错误: {e}")
        raise ValueError(f"在分割图像颜色通道时发生错误: {e}")

def merge_image_channels(file_paths):
    '''
    该函数用于合并多个单通道图像，创建一个多通道图像
    :param file_paths: 包含单通道图像文件路径的列表
    :return: 合并后的多通道图像
    '''
    try:
        logging.info("开始合并图像通道")
        
        # TODO: 想办法加载每个图像文件，然后将它们合并成一个多通道图像 merged_image
        # 注意: 检查每个图像是否是单通道的，如果不是，raise 一个异常信息: 要合并子图像必须是单通道图像，不能是多通道图像

        # 创建一个空列表，用于存储每个图像的单通道图像
        channel_images = []
        
        # 遍历每个图像文件路径
        for image_path in file_paths:
            # 加载图像文件
            #image_io.load_image(file_path) 调用image_io.py文件中的load_image函数
            image = image_io.load_image(image_path)
           
            # 检查图像是否是单通道的
            if image.ndim > 2 and image.shape[2] > 1:
                raise ValueError("要合并子图像必须是单通道图像，不能是多通道图像")
            
            # 将单通道图像添加到列表中
            channel_images.append(image)
        
        # 使用numpy的stack函数，沿着通道维度合并图像
        merged_image = np.stack(channel_images, axis=2)

        
        logging.info("成功合并图像通道")
        return merged_image
    except Exception as e:
        raise ValueError(f"在合并图像通道时发生错误: {e}")