import time
import sys
from tkinter import *
from tkinter import colorchooser, simpledialog, filedialog, messagebox

from PIL import ImageGrab, ImageFilter, Image, ImageTk

image_paths = ['1.png', '2.png', '3.png', '4.png']
canvas_x, canvas_y = 350, 20  # 画布大小
pen_color = 'black'  # 初始颜色
pen_width = 2  # 初始粗细
pen_type = 'normal'
last_x, last_y = None, None


# 定义新建文件功能的函数
def new_canvas(x, y):
    global canvas_x, canvas_y
    canvas_x = x + 20
    canvas_y = y + 20
    main(canvas_x, canvas_y)  # 创建新的窗口和画布


# 定义保存文件功能的函数
def save_canvas(root_window, canvas):
    try:
        file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[("PNG files", '*.png')])
        if file_path:
            x = root_window.winfo_rootx() + canvas.winfo_x()
            y = root_window.winfo_rooty() + canvas.winfo_y()
            x1 = x + canvas.winfo_width()
            y1 = y + canvas.winfo_height()
            ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)
            messagebox.showinfo('提示', '保存成功！')
    except Exception as e:
        messagebox.showerror("错误", f"保存失败: {str(e)}")


def change_color():
    global pen_color
    color = colorchooser.askcolor()[1]
    if color:
        pen_color = color


def change_thickness():
    global pen_width
    try:
        width = int(simpledialog.askinteger("", "请输入画笔粗细（1-20）：", minvalue=1, maxvalue=20))
        pen_width = width
    except TypeError:  # 用户取消输入
        pass


def change_pen_type(p_type):
    global pen_type
    pen_type = p_type


def start_draw(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y


def draw(event, c):
    global last_x, last_y, pen_color, pen_width, pen_type
    dash = None
    if pen_type == 'dashed':
        dash = (30, 100)
    elif pen_type == 'dotted':
        dash = (7, 7)

    c.create_line((last_x, last_y, event.x, event.y), fill=pen_color, width=pen_width, dash=dash)
    last_x, last_y = event.x, event.y


def eraser():
    global pen_width, pen_type
    try:
        width = int(simpledialog.askinteger("", "请输入橡皮擦粗细（1-20）：", minvalue=1, maxvalue=20))
        pen_width = width
        pen_type = 'eraser'
    except TypeError:  # 用户取消输入
        pass


def picture_filter(function, root, in_canvas):
    time.sleep(1)
    try:
        x = root.winfo_rootx() + in_canvas.winfo_x()
        y = root.winfo_rooty() + in_canvas.winfo_y()
        x1 = x + in_canvas.winfo_width()
        y1 = y + in_canvas.winfo_height()
        image = ImageGrab.grab().crop((x, y, x1, y1))

        filter_map = {
            'blur': ImageFilter.BLUR,
            'contour': ImageFilter.CONTOUR,
            'detail_enhance': ImageFilter.DETAIL,
            'edge_enhance': ImageFilter.EDGE_ENHANCE,
            'emboss': ImageFilter.EMBOSS,
            'sharp': ImageFilter.SHARPEN,
            'smooth': ImageFilter.SMOOTH
        }

        if function in filter_map:
            image = image.filter(filter_map[function])
        elif function == 'brightness':
            bright_num = float(simpledialog.askinteger("", "请输入画面亮度（0.0-2.0）：", minvalue=0.0, maxvalue=2.0))
            image = image.point(lambda i: i * bright_num)
        elif function == 'diaphaneity':
            image = image.convert('RGBA')
            alpha = image.split()[3]
            diaphaneity_num = float(
                simpledialog.askinteger("", "请输入画面透明度（0.0-2.0）：", minvalue=0.0, maxvalue=2.0))
            image = alpha.point(lambda i: i * diaphaneity_num)

        temp_image_path = "temp_filtered_image.png"
        image.save(temp_image_path)
        in_canvas.delete("all")
        img = PhotoImage(file=temp_image_path)
        in_canvas.create_image(0, 0, anchor=NW, image=img)
        in_canvas.image = img  # 保持对图片的引用
        messagebox.showinfo('提示', '滤镜处理成功！')
        import os
        os.remove(temp_image_path)
    except Exception as e:
        messagebox.showerror("错误", f"滤镜处理失败: {str(e)}")


# 定义关于有关的函数
def about():
    messagebox.showinfo('关于', '图像编辑器\n作者：熊思尧\n版本：v2.0')


# 定义关于功能的函数
def help_us():
    messagebox.showinfo('使用',
                        '1. 新建文件：创建一个新的画布，并清空画布内容。\n 2. 保存文件：将画布内容保存为PNG格式图片。\n 3. 画笔颜色：选择画笔颜色。\n 4. 画笔粗细：选择画笔粗细。\n '
                        '5. 画笔类型：选择画笔类型。\n 6. 橡皮擦：选择橡皮擦粗细。\n 7. 滤镜：选择图像滤镜。\n 8. 关于：查看软件信息。\n 11. 使用：查看软件使用说明。')


# 创建按钮点击事件处理程序
def button_click():
    selected_option = radio_var.get()
    root_1.destroy()
    if selected_option == "无背景作画":
        main(canvas_x, canvas_y)
    elif selected_option == "有背景滤镜作画":
        main_2()


# 定义选择图片的函数
def image_selector(image_paths):
    import tkinter as tk

    # 内部函数：加载和显示图片
    def display_image(index):
        try:
            image_path = image_paths[index]
            image = Image.open(image_path).resize((400, 300), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(image)
            img_label.config(image=img)
            img_label.image = img  # 防止垃圾回收
        except Exception as e:
            messagebox.showerror("错误", f"展示图片失败: {str(e)}")

    # 内部函数：切换到下一张图片
    def next_image():
        nonlocal current_image_index
        current_image_index = (current_image_index + 1) % len(image_paths)
        display_image(current_image_index)

    # 内部函数：选好图片
    def select_image():
        nonlocal selected_image_path
        selected_image_path = image_paths[current_image_index]
        win.quit()  # 关闭窗口

    # 初始化主窗口
    win = tk.Tk()
    win.title("图片展示")
    win.geometry("420x400+600+200")
    # 初始状态
    current_image_index = 0
    selected_image_path = None

    # 图片标签
    img_label = tk.Label(win)
    img_label.pack()

    # 显示初始图片
    display_image(current_image_index)

    # 切换按钮
    next_button = tk.Button(win, text="下一张", command=next_image)
    next_button.pack(side=tk.LEFT)

    # 选好了按钮
    select_button = tk.Button(win, text="我选好了", command=select_image)
    select_button.pack(side=tk.RIGHT)

    # 启动主循环
    win.mainloop()

    # 返回选中的图片路径
    return selected_image_path


# 定义无背景主运行函数
def main(x, y, image_photo=None):
    root = Tk()  # 创建主窗口
    root.title('图像编辑器')
    root.geometry(f'1200x900+{x}+{y}')
    root.resizable(False, False)
    menubar = Menu(root)
    '''创建文件菜单'''
    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label='新建', command=lambda: new_canvas(x, y))
    file_menu.add_command(label='保存', command=lambda: save_canvas(root, c))
    menubar.add_cascade(label='文件', menu=file_menu)

    '''创建涂鸦大菜单'''
    doodle_menu = Menu(menubar, tearoff=0)
    '''创建画笔菜单'''
    pen_menu = Menu(doodle_menu, tearoff=0)
    pen_menu.add_command(label='颜色', command=change_color)
    pen_menu.add_command(label='粗细', command=change_thickness)
    '''添加画笔类型选择作为画笔的子菜单'''
    pen_type_menu = Menu(pen_menu, tearoff=0)
    pen_type_menu.add_command(label='普通', command=lambda: change_pen_type('normal'))
    pen_type_menu.add_command(label='虚线', command=lambda: change_pen_type('dashed'))
    pen_type_menu.add_command(label='圆点线', command=lambda: change_pen_type('dotted'))
    pen_menu.add_cascade(label='类型', menu=pen_type_menu)
    doodle_menu.add_cascade(label='画笔', menu=pen_menu)
    '''创建橡皮擦菜单'''
    eraser_menu = Menu(doodle_menu, tearoff=0)
    eraser_menu.add_command(label='粗细', command=eraser)
    doodle_menu.add_cascade(label='橡皮', menu=eraser_menu)
    menubar.add_cascade(label='涂鸦', menu=doodle_menu)

    '''创建滤镜菜单'''
    filter_menu = Menu(menubar, tearoff=0)
    for filter_name in ['模糊', '轮廓', '细节增强', '边缘增强', '浮雕', '锐化', '平滑', '亮度', '透明度']:
        filter_func_name = filter_name.replace('增强', 'enhance').lower()
        filter_menu.add_command(label=filter_name, command=lambda fn=filter_func_name: picture_filter(fn, root, c))
    menubar.add_cascade(label='滤镜', menu=filter_menu)
    '''创建帮助菜单'''
    help_menu = Menu(menubar, tearoff=0)
    help_menu.add_command(label='关于', command=about)
    help_menu.add_command(label='使用', command=help_us)
    menubar.add_cascade(label='帮助', menu=help_menu)

    root.config(menu=menubar)
    root['menu'] = menubar
    """创建画布"""
    # 创建画布
    c = Canvas(root, width=1200, height=900, bg='white')
    c.pack()
    c.config(cursor="pencil")
    # 绑定鼠标事件
    c.bind('<Button-1>', start_draw)
    c.bind('<B1-Motion>', lambda event: draw(event, c))

    # 如果提供了图像路径，则加载并显示图像
    if image_photo:
        c.create_image(0, 0, anchor="nw", image=image_photo)
        c.image = image_photo  # 保存引用，避免图片被垃圾回收

    root.mainloop()

    return root, c


# 定义有背景作画主运行函数
def main_2():
    IMAGE_PATH = image_selector(image_paths)
    root_why = Toplevel()
    ImageFilterApp(IMAGE_PATH, root_why)
    root_why.mainloop()


# 定义滤镜的功能类
class ImageFilterApp:
    def __init__(self, path, root):
        # 固定路径
        self.image_path = path

        # 初始化 Tkinter 窗口
        self.root = root
        self.root.title("图片滤镜对比工具")
        self.root.geometry("1000x600+500+200")

        # 创建画布显示图片
        self.canvas_original = Canvas(self.root, width=300, height=300)
        self.canvas_filtered = Canvas(self.root, width=300, height=300)

        self.canvas_original.grid(row=0, column=0, padx=10, pady=10)
        self.canvas_filtered.grid(row=0, column=1, padx=10, pady=10)

        # 初始化图片
        self.img_original = self.open_image(self.image_path)
        self.img_filtered = self.img_original

        # 创建单选框选择滤镜
        self.filter_var = StringVar(value="NONE")
        filters = [("无", "NONE"), ("模糊", "BLUR"), ("轮廓", "CONTOUR"), ("细节", "DETAIL"),
                   ("边缘增强", "EDGE_ENHANCE")]

        for text, filter_type in filters:
            rb = Radiobutton(self.root, text=text, variable=self.filter_var, value=filter_type,
                             command=self.apply_filter)
            rb.grid(row=1, column=filters.index((text, filter_type)), padx=5, pady=5)

        # 创建保存按钮
        save_button = Button(self.root, text="保存过滤后的图片", command=self.save_filtered_image)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

        # 显示初始图片
        self.display_images()

    # 打开图片函数
    @staticmethod
    def open_image(path):
        if not path:
            messagebox.showerror("错误", f"图片路径不存在: {path}")
            sys.exit(1)
        try:
            img = Image.open(path)
            return img
        except Exception as e:
            messagebox.showerror("错误", f"无法打开图片: {str(e)}")
            return None

    # 应用滤镜函数
    def apply_filter(self):
        filter_type = self.filter_var.get()
        filter_map = {
            "BLUR": ImageFilter.BLUR,
            "CONTOUR": ImageFilter.CONTOUR,
            "DETAIL": ImageFilter.DETAIL,
            "EDGE_ENHANCE": ImageFilter.EDGE_ENHANCE,
        }

        if filter_type in filter_map:
            self.img_filtered = self.img_original.filter(filter_map[filter_type])
        else:
            self.img_filtered = self.img_original  # 默认不处理

        # 更新画布显示处理后的图片
        self.display_images()

    # 保存过滤后的图片
    def save_filtered_image(self):
        if self.img_filtered:
            try:
                file_path = filedialog.asksaveasfilename(defaultextension='.png',
                                                         filetypes=[("PNG files", '*.png')])
                if file_path:
                    self.img_filtered.save(file_path)
                    messagebox.showinfo("保存成功", f"图片已保存到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")

    # 在 Tkinter 界面上显示原图和处理后的图片
    def display_images(self):
        for canvas, img in zip([self.canvas_original, self.canvas_filtered], [self.img_original, self.img_filtered]):
            img_resized = img.resize((300, 300), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_resized)
            canvas.create_image(0, 0, anchor="nw", image=img_tk)
            canvas.image = img_tk  # 防止图片被垃圾回收


if __name__ == '__main__':
    # 创建Tkinter窗口
    root_1 = Tk()
    root_1.geometry("500x300+500+300")
    root_1.title("请选择")

    # 创建一个StringVar变量以存储单选按钮的值
    radio_var = StringVar()

    # 设置默认值为空
    var = StringVar(value="")

    # 创建单选按钮1
    radio_button1 = Radiobutton(root_1, text="无背景作画", variable=radio_var, value="无背景作画")

    # 创建单选按钮2
    radio_button2 = Radiobutton(root_1, text="有背景滤镜作画", variable=radio_var, value="有背景滤镜作画")

    # 创建按钮
    button = Button(root_1, text="获取选择", command=button_click)

    # 创建标签
    label = Label(root_1, text="")

    # 将单选按钮、按钮和标签添加到窗口
    radio_button1.pack()
    radio_button2.pack()
    button.pack()

    # 启动Tkinter主事件循环
    root_1.mainloop()
