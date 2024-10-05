### Image Editor - Documentation

#### 1. Introduction
This image editor is a simple drawing tool based on the `Tkinter` and `Pillow` libraries. It supports basic drawing, image processing, and filter functions. Users can freely draw, apply filters to images, and save them as PNG files.

#### 2. Features Overview
- **New Canvas**: Users can create a new canvas to start drawing.
- **Save Canvas**: Save the current canvas content as a PNG image.
- **Brush Settings**: Choose brush color, thickness, and type.
- **Eraser**: Use the eraser to remove parts of the drawing, with adjustable thickness.
- **Image Filters**: Provides various filters like blur, contour, sharpen, and more. Users can preview the effects in real-time.
- **Background Image Selection**: Users can select a background from a predefined image library for drawing.
- **About & Help**: Provides software version information and usage guide.

#### 3. Instructions
1. **Drawing without a Background**  
   Users can select a plain white canvas to draw freely. The brush color, thickness, and type can be adjusted as needed.

2. **Drawing with a Background**  
   Users can choose an image from the predefined library as a background. After applying filters, they can draw over it. The selected background will be loaded onto the canvas.

3. **Brush Settings**  
   - Color Selection: Change the brush color using the color picker.
   - Thickness Selection: Set the brush thickness, ranging from 1 to 20.
   - Brush Type: Provides different types such as solid, dashed, and dotted lines to meet various drawing needs.

4. **Eraser**  
   The eraser is used to remove parts of the drawing, and its thickness can be adjusted.

5. **Filter Functionality**  
   Offers several filter options, including:
   - Blur
   - Contour
   - Detail Enhancement
   - Edge Enhancement
   - Emboss
   - Sharpen
   - Brightness and Transparency adjustment  
   Users can preview and apply the selected filters in real-time.

6. **Save Canvas**  
   Users can save the current drawing as a PNG image. A confirmation message will pop up after saving successfully.

#### 4. Menu Explanation
- **File**: Options to create a new canvas or save the current one.
- **Draw**: Brush settings including color, thickness, and type, along with the eraser option.
- **Filters**: Various image processing filters for the user to choose from.
- **Help**: Provides a usage guide and information about the software.

#### 5. Code Structure
- **Main Window**: Manages the canvas, menu bar, and responds to user actions.
- **Drawing Functionality**: Supports free drawing with mouse event binding on the `Canvas`.
- **Filter Processing**: Uses the `Pillow` library to apply filters and update the canvas in real-time.
- **Image Selector**: Offers preset images for users to choose as the drawing background.

#### 6. Dependencies
- `Tkinter`: Used to create the user interface and implement drawing functionality.
- `Pillow`: Used to handle images and apply filter effects.

#### 7. Running the Program
Make sure `Tkinter` and `Pillow` libraries are installed, then run the code to launch the image editor:
```bash
pip install pillow
python editor.py
```

#### 8. About
Author: 2011smallbear  
Version: v6.0

#### 9. Recent Changes
- The interface is greatly optimized, and ttk is used
- Authoring mode name change
