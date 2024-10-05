import time
from tkinter import *
from tkinter import colorchooser, simpledialog, filedialog, messagebox, ttk
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
            x1, y1 = root_window.winfo_rootx() + canvas.winfo_x() + canvas.winfo_width(), \
                     root_window.winfo_rooty() + canvas.winfo_y() + canvas.winfo_height()
            ImageGrab.grab(bbox=(root_window.winfo_rootx() + canvas.winfo_x(),
                                 root_window.winfo_rooty() + canvas.winfo_y(), x1, y1)).save(file_path)
            messagebox.showinfo('提示', '保存成功！')
    except Exception as e:
        messagebox.showerror("错误", f"保存失败: {str(e)}")


# 定义画笔颜色的函数
def change_color():
    global pen_color
    color = colorchooser.askcolor()[1]
    if color:
        pen_color = color


# 定义画笔粗细的函数
def change_thickness():
    global pen_width
    try:
        width = simpledialog.askinteger("粗细", "请输入画笔粗细（1-20）：", minvalue=1, maxvalue=20)
        if width:
            pen_width = width
    except Exception as e:
        messagebox.showerror("错误", f"输入失败: {str(e)}")


# 定义画笔类型选择的函数
def change_pen_type(p_type):
    global pen_type
    pen_type = p_type


# 定义开始绘图的函数
def start_draw(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y


# 定义绘图的函数
def draw(event, c):
    global last_x, last_y
    dash = None
    if pen_type == 'dashed':
        dash = (30, 100)
    elif pen_type == 'dotted':
        dash = (7, 7)

    c.create_line((last_x, last_y, event.x, event.y), fill=pen_color, width=pen_width, dash=dash)
    last_x, last_y = event.x, event.y


# 定义橡皮擦的函数
def eraser():
    global pen_width, pen_type
    try:
        width = simpledialog.askinteger("橡皮擦粗细", "请输入橡皮擦粗细（1-20）：", minvalue=1, maxvalue=20)
        if width:
            pen_width = width
            pen_type = 'eraser'
    except Exception as e:
        messagebox.showerror("错误", f"输入失败: {str(e)}")


# 定义滤镜的函数
def picture_filter(function, root, in_canvas):
    time.sleep(1)
    # 抓取画布图像
    x1 = root.winfo_rootx() + in_canvas.winfo_x() + in_canvas.winfo_width()
    y1 = root.winfo_rooty() + in_canvas.winfo_y() + in_canvas.winfo_height()
    image = ImageGrab.grab().crop((root.winfo_rootx() + in_canvas.winfo_x(),
                                   root.winfo_rooty() + in_canvas.winfo_y(), x1, y1))

    try:
        filters = {
            'blur': ImageFilter.BLUR,
            'contour': ImageFilter.CONTOUR,
            'detail_enhance': ImageFilter.DETAIL,
            'edge_enhance': ImageFilter.EDGE_ENHANCE,
            'emboss': ImageFilter.EMBOSS,
            'sharp': ImageFilter.SHARPEN,
            'smooth': ImageFilter.SMOOTH,
        }

        if function in filters:
            image = image.filter(filters[function])
        elif function == 'brightness':
            bright_num = simpledialog.askfloat("", "请输入画面亮度（0.0-2.0）：", minvalue=0.0, maxvalue=2.0)
            if bright_num is not None:
                image = image.point(lambda i: i * bright_num)
        elif function == 'diaphaneity':
            image = image.convert('RGBA')
            alpha = image.split()[3]
            diaphaneity_num = simpledialog.askfloat("", "请输入画面透明度（0.0-2.0）：", minvalue=0.0, maxvalue=2.0)
            if diaphaneity_num is not None:
                image = alpha.point(lambda i: i * diaphaneity_num)

        # 显示滤镜处理后的图像
        temp_image_path = "D:/temp_filtered_image.png"
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


# 定义关于功能的函数
def about():
    messagebox.showinfo('关于', '图像编辑器\n作者：熊思尧\n版本：v2.0')


# 创建按钮点击事件处理程序
def button_click():
    selected_option = radio_var.get()
    root_1.destroy()
    if selected_option == "涂鸦板创作模式":
        main(canvas_x, canvas_y)
    elif selected_option == "艺术滤镜创作模式":
        main_2()


# 选择图片的函数
def image_selector(image_paths, background_path):
    def display_image(index):
        try:
            image_path = image_paths[index]
            img = Image.open(image_path).resize((400, 300), Image.LANCZOS)
            img_label.img = ImageTk.PhotoImage(img)
            img_label.config(image=img_label.img)
        except Exception as e:
            messagebox.showerror("错误", f"展示图片失败: {str(e)}")

    def next_image():
        nonlocal current_image_index
        current_image_index = (current_image_index + 1) % len(image_paths)
        display_image(current_image_index)

    def select_image():
        nonlocal selected_image_path
        selected_image_path = image_paths[current_image_index]
        win.quit()  # 关闭窗口

    win = Tk()
    win.title("图片展示")
    win.geometry("400x400+600+200")
    win.resizable(False, False)
    current_image_index = 0
    selected_image_path = None
    img_label = Label(win)
    img_label.pack()

    display_image(current_image_index)

    ttk.Button(win, text="下一张", command=next_image).pack(side=LEFT)
    ttk.Button(win, text="我选好了", command=select_image).pack(side=RIGHT)

    win.mainloop()
    return selected_image_path


# 无背景主运行函数
def main(x, y, image_photo=None):
    root = Tk()  # 创建主窗口
    root.title('图像编辑器')
    root.geometry(f'1200x900+{x}+{y}')
    root.resizable(False, False)

    menubar = Menu(root)
    # 创建文件菜单
    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label='新建', command=lambda: new_canvas(x, y))
    file_menu.add_command(label='保存', command=lambda: save_canvas(root, c))
    menubar.add_cascade(label='文件', menu=file_menu)

    # 创建涂鸦大菜单
    doodle_menu = Menu(menubar, tearoff=0)
    pen_menu = Menu(doodle_menu, tearoff=0)
    pen_menu.add_command(label='颜色', command=change_color)
    pen_menu.add_command(label='粗细', command=change_thickness)

    # 添加画笔类型选择作为画笔的子菜单
    pen_type_menu = Menu(pen_menu, tearoff=0)
    pen_type_menu.add_command(label='普通', command=lambda: change_pen_type('normal'))
    pen_type_menu.add_command(label='虚线', command=lambda: change_pen_type('dashed'))
    pen_type_menu.add_command(label='圆点线', command=lambda: change_pen_type('dotted'))
    pen_menu.add_cascade(label='类型', menu=pen_type_menu)

    doodle_menu.add_cascade(label='画笔', menu=pen_menu)
    eraser_menu = Menu(doodle_menu, tearoff=0)
    eraser_menu.add_command(label='粗细', command=eraser)
    doodle_menu.add_cascade(label='橡皮', menu=eraser_menu)
    menubar.add_cascade(label='涂鸦', menu=doodle_menu)

    # 创建滤镜菜单
    filter_menu = Menu(menubar, tearoff=0)
    filter_options = [
        ('模糊', 'blur'),
        ('轮廓', 'contour'),
        ('细节增强', 'detail_enhance'),
        ('边缘增强', 'edge_enhance'),
        ('浮雕', 'emboss'),
        ('锐化', 'sharp'),
        ('平滑', 'smooth'),
        ('亮度', 'brightness'),
        ('透明度', 'diaphaneity')
    ]

    for label, filter_type in filter_options:
        filter_menu.add_command(label=label, command=lambda f=filter_type: picture_filter(f, root, c))

    menubar.add_cascade(label='滤镜', menu=filter_menu)

    # 创建帮助菜单
    help_menu = Menu(menubar, tearoff=0)
    help_menu.add_command(label='关于', command=about)
    menubar.add_cascade(label='帮助', menu=help_menu)

    root.config(menu=menubar)

    c = Canvas(root, width=1200, height=900, bg='white')
    c.pack()
    c.config(cursor="pencil")
    c.bind('<Button-1>', start_draw)
    c.bind('<B1-Motion>', lambda event: draw(event, c))

    if image_photo:
        c.create_image(0, 0, anchor="nw", image=image_photo)
        c.image = image_photo  # 保存引用，避免图片被垃圾回收

    root.mainloop()
    return root, c


# 有背景作画主运行函数
def main_2():
    image_p = image_selector(image_paths, "background2.jpg")
    root_why = Toplevel()
    ImageFilterApp(image_p, root_why)
    root_why.mainloop()


class ImageFilterApp:
    def __init__(self, path, root):
        self.image_path = path
        self.root = root
        self.root.title("图片滤镜对比工具")
        self.root.geometry("1000x600+500+200")
        self.root.resizable(False, False)

        self.canvas_original = Canvas(self.root, width=300, height=300)
        self.canvas_filtered = Canvas(self.root, width=300, height=300)

        self.canvas_original.grid(row=0, column=0, padx=10, pady=10)
        self.canvas_filtered.grid(row=0, column=1, padx=10, pady=10)

        self.img_original = self.open_image(self.image_path)
        self.img_filtered = self.img_original

        self.filter_var = StringVar(value="NONE")
        filters = [("无", "NONE"), ("模糊", "BLUR"), ("轮廓", "CONTOUR"), ("细节", "DETAIL"),
                   ("边缘增强", "EDGE_ENHANCE")]
        for text, filter_type in filters:
            ttk.Radiobutton(self.root, text=text, variable=self.filter_var, value=filter_type,
                        command=self.apply_filter).grid(row=1, column=filters.index((text, filter_type)), padx=5,
                                                        pady=5)

        ttk.Button(self.root, text="保存过滤后的图片", command=self.save_filtered_image).grid(row=2, column=0, columnspan=2, pady=10)


        self.display_images()

    @staticmethod
    def open_image(path):
        try:
            return Image.open(path)
        except Exception as e:
            messagebox.showerror("错误", f"无法打开图片: {str(e)}")
            return None

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

        self.display_images()

    def save_filtered_image(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[("PNG files", '*.png')])
            if file_path:
                self.img_filtered.save(file_path)
                messagebox.showinfo("保存成功", f"图片已保存到: {file_path}")
                self.status_var.set(f"图片已保存到: {file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")
            self.status_var.set("保存失败")

    def display_images(self):
        for canvas, img in zip([self.canvas_original, self.canvas_filtered], [self.img_original, self.img_filtered]):
            img_resized = img.resize((300, 300), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_resized)
            canvas.create_image(0, 0, anchor="nw", image=img_tk)
            canvas.image = img_tk  # 防止图片被垃圾回收


if __name__ == '__main__':
    # 创建主窗口
    root_1 = Tk()
    root_1.geometry("500x300+700+300")
    root_1.title("请选择")
    root_1.resizable(False, False)

    # 加载并设置背景图片
    image = Image.open("background1.jpg")  # 替换为你自己的图片路径
    image = image.resize((500, 300))  # 调整图片大小以适应窗口
    background_image1 = ImageTk.PhotoImage(image)

    # 创建一个Label控件用于显示背景图片
    background_label1 = Label(root_1, image=background_image1)
    background_label1.place(x=0, y=0, relwidth=1, relheight=1)  # 将图片铺满整个窗口

    # 保持引用，避免图片被垃圾回收
    background_label1.image = background_image1

    # 使用place()来精确放置控件
    label = Label(
        root_1,
        text='图 像 编 辑 器',
        font=("Helvetica", 16, "bold"),
        foreground="yellow",
        background="lightblue"
    )
    label.place(x=175, y=50)  # 放置在窗口的指定位置

    radio_var = StringVar()
    radio_var.set("")  # 设置初始状态为空

    # 使用ttk.Radiobutton
    radio1 = ttk.Radiobutton(root_1, text="涂鸦板创作模式", variable=radio_var, value="涂鸦板创作模式")
    radio1.place(x=185, y=100)

    radio2 = ttk.Radiobutton(root_1, text="艺术滤镜创作模式", variable=radio_var, value="艺术滤镜创作模式")
    radio2.place(x=180, y=130)

    # 使用ttk.Button
    button = ttk.Button(root_1, text="获取选择", command=button_click)
    button.place(x=192, y=200)

    root_1.mainloop()
