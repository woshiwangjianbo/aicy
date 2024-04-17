import os

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 图像文件默认保存路径
DEFAULT_SAVE_PATH = os.path.join(PROJECT_ROOT, 'output')

# 支持的图像格式
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

# 默认的图像保存格式
DEFAULT_SAVE_FORMAT = 'jpg'

# 默认的图像尺寸
DEFAULT_IMAGE_SIZE = (800, 600)

# 默认的裁剪区域比例
DEFAULT_CROP_RATIO = (0.1, 0.9, 0.1, 0.9)  # (top, bottom, left, right)

# 默认的缩放比例
DEFAULT_SCALE_RATIO = 0.5

# 默认的旋转角度
DEFAULT_ROTATION_ANGLE = 90

# 默认的图像通道
DEFAULT_IMAGE_CHANNELS = 3

# 日志文件路径
LOG_FILE_PATH = os.path.join(PROJECT_ROOT, 'app.log')

# 日志级别
LOG_LEVEL = 'DEBUG'