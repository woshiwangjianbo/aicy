import tkinter as tk  # tkinter是Python内置的GUI库,用于创建图形用户界面
from tkinter import filedialog  # filedialog是tkinter中的一个模块,用于显示文件对话框
from tkinter import messagebox  # messagebox是tkinter中的一个模块,用于显示消息框
from PIL import Image, ImageTk  # PIL是Python的图像处理库,用于加载、操作和保存图像
import os  # os模块提供了与操作系统交互的功能,如文件路径操作
import numpy as np  # numpy是Python的数值计算库,用于处理数组和矩阵
import image_channels  # image_channels是一个自定义模块,用于分割和合并图像通道
import image_io  # image_io是一个自定义模块,用于加载和保存图像
import image_transform  # image_transform是一个自定义模块,用于图像变换
import config  # config是一个自定义模块,用于存储应用程序的配置信息
import sys  # sys模块提供了与Python解释器和运行环境相关的变量和函数
from image_utils import language_data, logging  # 从image_utils模块中导入language_data和logging
import image_utils as utils  # 导入image_utils模块并给它一个别名utils
import subprocess  # subprocess模块允许你生成新的进程，连接它们的输入、输出和错误管道，并获取它们的返回码


class ImageProcessor:
    def __init__(self, master):
        """初始化ImageProcessor类的实例"""
        self.master = master  # 主窗口
        self.current_language = language_data["current_language"]  # 默认语言通过JSON文件直接设置
        master.title(language_data[self.current_language]['app_title'])  # 设置初始窗口标题

        self.image = None  # 用于存储当前图像的numpy数组
        self.image_path = ""  # 用于存储当前图像的文件路径
        self.rect_start_x = None  # 用于存储裁剪矩形框起始点的x坐标
        self.rect_start_y = None  # 用于存储裁剪矩形框起始点的y坐标
        self.rect_end_x = None  # 用于存储裁剪矩形框结束点的x坐标
        self.rect_end_y = None  # 用于存储裁剪矩形框结束点的y坐标
        self.is_drawing = False  # 用于标记是否正在绘制裁剪矩形框
        self.current_rect = None  # 用于存储当前绘制的裁剪矩形框对象

        self.create_widgets()  # 创建GUI组件

    def create_widgets(self):
        """创建GUI组件"""
        # 创建菜单栏
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # 创建文件菜单
        file_menu = tk.Menu(menubar)
        file_menu.add_command(label=language_data[self.current_language]['open_original'], command=self.Open_as_original)
        file_menu.add_command(label=language_data[self.current_language]['open_grayscale'], command=self.Open_as_gray)
        file_menu.add_command(label=language_data[self.current_language]['merge_channels'], command=self.merge_channels)
        file_menu.add_command(label=language_data[self.current_language]['save_image'], command=self.save_image)
        file_menu.add_separator()
        
        # 创建一个菜单项,用于切换语言,它应该有两个子菜单项,分别用于切换中文和英文。当前语言用一个勾选标记来表示。
        language_menu = tk.Menu(file_menu)
        self.language_var = tk.StringVar(value=self.current_language)
        language_menu.add_radiobutton(label="中文", variable=self.language_var, value="zh", command=self.change_language)
        language_menu.add_radiobutton(label="English", variable=self.language_var, value="en", command=self.change_language)
        file_menu.add_cascade(label=language_data[self.current_language]['language'], menu=language_menu)
        
        file_menu.add_command(label=language_data[self.current_language]['exit'], command=self.master.quit)
        menubar.add_cascade(label=language_data[self.current_language]['file'], menu=file_menu)

        # 创建信息菜单
        info_menu = tk.Menu(menubar)
        info_menu.add_command(label=language_data[self.current_language]['details'], command=self.show_image_details)
        menubar.add_cascade(label=language_data[self.current_language]['info'], menu=info_menu)

        # 创建编辑菜单
        edit_menu = tk.Menu(menubar)
        edit_menu.add_command(label=language_data[self.current_language]['crop'], command=self.crop_image)
        edit_menu.add_command(label=language_data[self.current_language]['reset'], command=self.reset_image)
        menubar.add_cascade(label=language_data[self.current_language]['edit'], menu=edit_menu)

        # 创建图像分割菜单
        split_menu = tk.Menu(menubar)
        menubar.add_cascade(label=language_data[self.current_language]['split'], menu=split_menu)
        split_menu.add_command(label=language_data[self.current_language]['split_channels'], command=self.split_image_channels)

        # 创建图像显示区域
        self.canvas = tk.Canvas(self.master, width=600, height=400)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
    
    def change_language(self):
        """切换语言"""
        # 把language.json文件中的current_language的值改为当前的self.current_language
        self.current_language = self.language_var.get()  # 获取所选择的语言
        utils.write_language_data(language_data, "current_language", self.current_language)
        logging.info(f"当前语言已切换为{self.current_language}。")
        confirm = messagebox.askyesno(language_data[self.current_language]['confirm_restart'],
                                  language_data[self.current_language]['restart_warning'])
        if confirm:
            self.master.destroy()
            # os.execl(sys.executable, sys.executable, *sys.argv)
            subprocess.Popen([sys.executable] + sys.argv)

    def merge_channels(self):
        """合并多个单通道图像为一个多通道图像"""
        # 打开文件对话框,让用户选择多个图像文件
        file_paths = filedialog.askopenfilenames()
        # 如果用户没有选择文件,直接返回
        if not file_paths:
            return
        
        # 如果只选择了一个文件,显示错误信息并返回
        if len(file_paths) == 1:
            tk.messagebox.showerror(language_data[self.current_language]['error'], language_data[self.current_language]['single_file_error'])
            return
        
        try:
            self.image = image_channels.merge_image_channels(file_paths)
        except ValueError as e:
            tk.messagebox.showerror(language_data[self.current_language]['error'], str(e))
            return
        
        # 显示当前图像
        self.display_image()

    def split_image_channels(self):
        """分割当前图像的通道,并在新窗口中显示每个通道"""
        if self.image is None:
            tk.messagebox.showinfo(language_data[self.current_language]['error'], language_data[self.current_language]['no_image_loaded'])
            return

        if len(self.image.shape) == 2:
            tk.messagebox.showinfo(language_data[self.current_language]['error'], language_data[self.current_language]['single_channel_error'])
            return

        try:
            channels = image_channels.split_image_channels(self.image)
        except ValueError as e:
            tk.messagebox.showinfo(language_data[self.current_language]['error'], str(e))
            return
        
        for i, channel in enumerate(channels):
            window = tk.Toplevel(self.master)
            window.title(language_data[self.current_language]['channel_title'].format(i))
            canvas = tk.Canvas(window, width=300, height=300)
            canvas.pack()

            # 定义内部函数用于保存单个通道
            def save_channel(channel, index):
                save_path = filedialog.asksaveasfilename(defaultextension=config.DEFAULT_SAVE_FORMAT)
                if not save_path:
                    return
                image_io.save_image(channel, save_path)
                tk.messagebox.showinfo(language_data[self.current_language]['success'], language_data[self.current_language]['channel_saved'].format(index, save_path))
            
            save_button = tk.Button(window, text=language_data[self.current_language]['save_channel'], command=lambda channel=channel: save_channel(channel, i))
            save_button.pack()

            window.update()

            # 显示子通道图像
            image = Image.fromarray(channel)  # 将通道数据转换为PIL图像对象
            canvas_width = canvas.winfo_width()  # 获取画布的宽度
            canvas_height = canvas.winfo_height()  # 获取画布的高度
            image_width, image_height = image.size  # 获取图像的宽度和高度
            scale = min(canvas_width / image_width, canvas_height / image_height)  # 计算图像的缩放比例
            if scale < 1:  # 如果图像过大,缩小图像
                new_width = int(image_width * scale)
                new_height = int(image_height * scale)
                image = image.resize((new_width, new_height), Image.LANCZOS)  # 使用Lanczos滤波器进行缩小
            else:  # 如果图像过小,放大图像
                new_width = int(image_width * scale)
                new_height = int(image_height * scale)
                image = image.resize((new_width, new_height), Image.BICUBIC)  # 使用双三次滤波器进行放大

            photo = ImageTk.PhotoImage(image)  # 将PIL图像对象转换为PhotoImage对象
            x = (canvas_width - new_width) // 2  # 计算图像在画布上的水平居中位置
            y = (canvas_height - new_height) // 2  # 计算图像在画布上的垂直居中位置
            canvas.create_image(x, y, anchor=tk.NW, image=photo)  # 在画布上显示图像
            canvas.image = photo  # 将PhotoImage对象保存到画布中,防止被垃圾回收

            # 在子图上添加清晰的标题
            title = f"Channel {i}"
            canvas.create_text(canvas_width//2, 15, text=title, font=("Arial", 15), fill="black")

        logging.info("图像分割操作成功。")  # 记录成功日志

    def show_image_details(self):
        """显示当前图像的详细信息"""
        if self.image is None:  # 如果当前没有图像,显示相应消息并返回
            messagebox.showinfo(language_data[self.current_language]['error'], language_data[self.current_language]['no_image_loaded'])
            logging.info("没有载入任何图像,无法显示图像细节。")  # 记录日志信息
            return

        # 从路径中提取文件名
        filename = os.path.basename(self.image_path)

        # 计算其他基本信息
        """一个颜色通道
        应该使用image.shape[0] * image.shape[1]来计算总像素数
        self.image.size会将颜色通道也计算在"""
        total_pixels = self.image.size  # TODO: 获取图像的总像素数
        # shape = self.image.shape
        # height, width, channels = shape[0], shape[1], shape[2]
        shape = self.image.shape  # TODO: 获取图像的形状(高度,宽度,通道数)
        # channels = self.image.shape[-1]
        """确定self.image总是一个三维数组
        那么使用self.image.shape[2]是没有问题的
        但如果self.image可能是二维或三维的
        那么使用self.image.shape[-1]会更安全"""
        channels = self.image.shape[-1]  # TODO: 获取图像的通道数，注意不是维度，而是通道数
        # dtype = self.image.dtype
        dtype =  self.image.dtype # TODO: 获取图像像素的数据类型

        # 构建信息字符串,包括文件名
        details = language_data[self.current_language]['info_str'].format(filename,total_pixels,shape,channels,dtype)

        # 显示信息
        messagebox.showinfo("INFO", details)
        logging.info("已显示图像细节。")  # 记录成功日志

    def on_mouse_down(self, event):
        """处理鼠标左键按下事件"""
        if self.current_rect and not self.is_drawing:
            # 如果存在矩形框且不是在拖动状态,删除矩形框并重置状态
            self.canvas.delete(self.current_rect)
            self.current_rect = None
        else:
            # 否则,开始绘制新的矩形框
            self.rect_start_x = event.x
            self.rect_start_y = event.y
            self.is_drawing = True

    def on_mouse_move(self, event):
        """处理鼠标左键移动事件"""
        if self.is_drawing:
            if self.current_rect:
                self.canvas.delete(self.current_rect)
            self.current_rect = self.canvas.create_rectangle(self.rect_start_x, self.rect_start_y, event.x, event.y, outline="red")

    def on_mouse_up(self, event):
        """处理鼠标左键释放事件"""
        # 标记矩形的结束点并完成绘制
        self.rect_end_x, self.rect_end_y = event.x, event.y
        self.is_drawing = False
        # 保存裁剪区域的坐标
        self.crop_region = (min(self.rect_start_y, self.rect_end_y), max(self.rect_start_y, self.rect_end_y),
                            min(self.rect_start_x, self.rect_end_x), max(self.rect_start_x, self.rect_end_x))
        logging.info("已绘制裁剪区域。")  # 记录成功日志

    def Open_as_original(self):
        """打开原始图像"""
        logging.info("正在打开原始图像...") 
        self.image_path = filedialog.askopenfilename()  # 打开文件对话框,让用户选择图像文件
        if not self.image_path:
            logging.info("没有选择任何图像文件,打开操作已取消。")  # 记录日志信息
            return  # 如果没有选择任何文件,直接返回
        self.image = image_io.load_image(self.image_path)
        self.display_image()
        logging.info("成功打开原始图像。")  # 记录成功日志
    
    def Open_as_gray(self):
        """将原始图像转换为灰度图像"""
        self.image_path = filedialog.askopenfilename()  # 打开文件对话框,让用户选择图像文件
        if not self.image_path:
            logging.info("没有选择任何图像文件,打开操作已取消。")  # 记录日志信息
            return  # 如果没有选择任何文件,直接返回
        self.image = image_io.load_image(self.image_path, as_gray=True)  # 加载图像文件并转换为灰度图像
        self.display_image()  # 显示图像
        logging.info("成功打开并转换为灰度图像。")  # 记录成功日志

    def display_image(self):
        """在主画布上显示当前图像"""
        if self.image is None:
            logging.info("当前没有图像可显示。")  # 记录日志信息
            return  # 如果当前没有图像,直接返回

        image = Image.fromarray(self.image)  # 将numpy数组转换为PIL图像对象

        # 计算图像的缩放比例
        canvas_width = self.canvas.winfo_width()  # 获取画布的宽度
        canvas_height = self.canvas.winfo_height()  # 获取画布的高度
        image_width, image_height = image.size  # 获取图像的宽度和高度
        scale = min(canvas_width / image_width, canvas_height / image_height)  # 计算图像的缩放比例

        # 缩放图像
        if scale < 1:
            # 图像过大,缩小图像
            new_width = int(image_width * scale)
            new_height = int(image_height * scale)
            image = image.resize((new_width, new_height), Image.LANCZOS)  # 使用Lanczos滤波器进行缩小
        else:
            # 图像过小,放大图像
            new_width = int(image_width * scale)
            new_height = int(image_height * scale)
            image = image.resize((new_width, new_height), Image.BICUBIC)  # 使用双三次滤波器进行放大

        photo = ImageTk.PhotoImage(image)  # 将PIL图像对象转换为PhotoImage对象
        self.canvas.delete("all")  # 清除画布上的所有内容

        # 计算图像在画布上的居中位置
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        self.canvas.create_image(x, y, anchor=tk.NW, image=photo)  # 在画布上显示图像, tk.NW表示图像的左上角对齐画布的左上角
        self.canvas.image = photo  # 将PhotoImage对象保存到画布中,防止被垃圾回收
        logging.info("成功显示图像。")  # 记录成功日志

    def save_image(self):
        """保存当前图像"""
        if self.image is None:
            tk.messagebox.showinfo(language_data[self.current_language]['error'], language_data[self.current_language]['no_image_to_be_saved'])
            logging.error("没有图像可保存,保存操作已取消。")  # 记录错误日志
            return  # 如果当前没有图像,直接返回

        save_path = filedialog.asksaveasfilename(defaultextension=config.DEFAULT_SAVE_FORMAT)  # 打开保存文件对话框
        if not save_path:
            logging.info("没有选择保存路径,保存操作已取消。")  # 记录日志信息
            return  # 如果没有选择保存路径,直接返回

        image_io.save_image(self.image, save_path)  # 将当前图像保存到指定路径
        logging.info(f"图像已成功保存到 {save_path}。")  # 记录成功日志

    def crop_image(self):
        """裁剪当前图像"""
        if self.image is None:
            tk.messagebox.showinfo(language_data[self.current_language]['error'], language_data[self.current_language]['no_image_to_be_cropped'])
            logging.error("没有图像可裁剪,裁剪操作已取消。")  # 记录错误日志
            return  # 如果当前没有图像,直接返回

        # 检查是否有绘制的裁剪区域
        if hasattr(self, 'crop_region') and self.current_rect:
            # 计算实际裁剪区域坐标(考虑图像缩放和偏移)
            image_height, image_width = self.image.shape[:2]  # 获取图像的高度和宽度
            canvas_width = self.canvas.winfo_width()  # 获取画布的宽度
            canvas_height = self.canvas.winfo_height()  # 获取画布的高度
            scale = min(canvas_width / image_width, canvas_height / image_height)  # 计算图像的缩放比例
            offset_x = (canvas_width - image_width * scale) // 2  # 计算图像在画布上的水平偏移量
            offset_y = (canvas_height - image_height * scale) // 2  # 计算图像在画布上的垂直偏移量

            # 计算实际裁剪区域坐标
            real_crop_region = (
                int((self.crop_region[0] - offset_y) / scale),
                int((self.crop_region[1] - offset_y) / scale),
                int((self.crop_region[2] - offset_x) / scale),
                int((self.crop_region[3] - offset_x) / scale)
            )

            cropped_image = image_transform.crop_image(self.image, real_crop_region)  # 裁剪图像
            if cropped_image is not None:
                self.image = cropped_image  # 将裁剪后的图像保存到self.image中
                self.display_image()  # 显示裁剪后的图像
                logging.info("图像裁剪成功。")  # 记录成功日志

                # 清零裁剪框信息
                self.canvas.delete(self.current_rect)  # 删除画布上的裁剪矩形框
                self.current_rect = None  # 将当前裁剪矩形框对象设置为None
                del self.crop_region  # 删除存储裁剪区域坐标的属性
            else:
                tk.messagebox.showinfo(language_data[self.current_language]['error'], language_data[self.current_language]['crop_failed'])
                logging.error("裁剪操作失败。")  # 记录错误日志
        else:
            tk.messagebox.showinfo(language_data[self.current_language]['error'], language_data[self.current_language]['no_crop_area'])
            logging.error("没有选择裁剪区域,裁剪操作已取消。")  # 记录错误日志

    def reset_image(self):
        """重置当前图像为原始状态"""
        if not self.image_path:  # 如果没有图像路径,显示错误消息并返回
            tk.messagebox.showinfo(language_data[self.current_language]['error'], language_data[self.current_language]['no_reset_image'])
            logging.error("没有图像可重置,重置操作已取消。")  # 记录错误日志
            return
        self.image = image_io.load_image(self.image_path)  # 重新加载图像
        self.display_image()  # 显示图像
        logging.info("图像已重置为原始状态。")  # 记录成功日志

# 创建主窗口和应用程序实例
root = tk.Tk()
app = ImageProcessor(root)
root.mainloop()
