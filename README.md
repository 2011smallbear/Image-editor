### 图像编辑器 - 介绍文档

#### 1. 简介
本图像编辑器是一个基于 `Tkinter` 和 `Pillow` 库的简单绘图工具，支持基础的绘画、图像处理和滤镜功能。用户可以通过该工具进行自由绘画、选择滤镜处理图片并保存为 PNG 文件。

#### 2. 功能概述

- **新建画布**: 用户可以创建一个新的画布进行绘图。
- **保存画布**: 将当前画布内容保存为 PNG 格式图片。
- **画笔设置**: 选择画笔的颜色、粗细和类型。
- **橡皮擦**: 使用橡皮擦功能清除画布上的部分内容，橡皮擦粗细可调。
- **图像滤镜**: 提供模糊、轮廓、锐化等多种滤镜，用户可实时查看效果。
- **背景图片选择**: 支持从预定义的图片库中选择背景进行绘画。
- **关于与帮助**: 提供软件版本信息和使用指南。

#### 3. 使用说明

1. **无背景绘画**  
   用户可以选择无背景的纯白画布进行自由绘画。画笔颜色、粗细和类型可以根据需要进行调整。
   
2. **有背景绘画**  
   用户可以从预定义的图片库中选择一张图片作为背景，应用滤镜后进行绘画。选择的背景图将加载到画布上。

3. **画笔设置**  
   - 颜色选择：用户通过颜色选择器更改画笔颜色。
   - 粗细选择：用户可以设置画笔粗细，范围在 1 到 20 之间。
   - 画笔类型：提供普通、虚线、圆点线等多种画笔类型，满足不同绘画需求。

4. **橡皮擦**  
   橡皮擦用于清除画布上的部分内容，用户可以调整其粗细。

5. **滤镜功能**  
   提供多种滤镜选项，包括：
   - 模糊（Blur）
   - 轮廓（Contour）
   - 细节增强（Detail）
   - 边缘增强（Edge Enhance）
   - 浮雕（Emboss）
   - 锐化（Sharpen）
   - 亮度调节和透明度调节

   选择滤镜后，用户可以实时预览并应用到画布上的图像。

6. **保存画布**  
   用户可以将当前的绘图内容保存为 PNG 格式的图片文件。保存成功后会弹出提示框确认。

#### 4. 菜单说明

- **文件**: 提供新建和保存画布的功能。
- **涂鸦**: 包含画笔颜色、粗细和类型的设置，并提供橡皮擦选项。
- **滤镜**: 各种图像处理滤镜功能，用户可根据需要进行选择。
- **帮助**: 提供使用指南及关于软件的信息。

#### 5. 代码结构
- **主窗口**: 负责创建画布、管理菜单栏以及响应用户的操作。
- **绘图功能**: 基于 `Canvas` 的鼠标事件绑定，支持自由绘画。
- **滤镜处理**: 使用 `Pillow` 库实现图像的滤镜效果，并实时更新画布内容。
- **图像选择器**: 提供预设图片供用户选择作为绘画背景。

#### 6. 依赖库
- `Tkinter`: 用于创建用户界面和实现绘图功能。
- `Pillow`: 用于处理图像和应用滤镜效果。

#### 7. 运行程序
确保已安装 `Tkinter` 和 `Pillow` 库后，直接运行代码即可启动图像编辑器。

```bash
pip install pillow
python editor.py
```

#### 8. 关于
作者：熊思尧  
版本：v2.0

#### 9. 未来改进方向
- 增加更多滤镜效果
- 支持更多格式的图片保存
- 提供撤销和重做功能
