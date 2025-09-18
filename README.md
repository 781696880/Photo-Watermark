# Photo-Watermark

## 项目概述

Photo-Watermark 是一个Python命令行工具，用于自动为照片添加基于拍摄时间的水印。该工具读取图片的EXIF信息，提取拍摄时间，并将该时间作为水印文本添加到图片上。

## 功能

### 核心功能

1. **图片路径输入**
   - 用户提供图片文件路径
   - 支持单个文件或整个目录的处理

2. **EXIF信息读取**
   - 读取图片文件的EXIF元数据
   - 提取拍摄时间信息
   - 将完整拍摄时间解析为年月日格式

3. **水印自定义设置**
   - 字体大小设置
   - 字体颜色设置
   - 水印位置设置（左上角、居中、右下角等）

4. **水印应用与保存**
   - 在原图片上绘制文本水印
   - 将处理后的图片保存到新目录
   - 新目录命名为原目录下的`[原目录名]_watermark`子目录

### 详细功能说明

#### 输入处理
- 支持常见图片格式（JPEG、PNG等）
- 能够处理单个文件或整个目录
- 对于没有EXIF信息或EXIF信息不完整的图片，应有适当的错误处理

#### EXIF信息提取
- 优先提取拍摄时间（DateTimeOriginal）
- 备选时间信息源（DateTime、DateTimeDigitized）
- 时间格式化为`YYYY-MM-DD`或`YYYY-MM-DD HH:MM:SS`格式

#### 水印自定义选项
- 字体大小：支持数字指定字体大小（如12、24、36等）
- 字体颜色：支持常见颜色名称（red、blue、white、black等）或十六进制颜色值
- 位置选项：
  - 左上角（top-left）
  - 顶部中央（top-center）
  - 右上角（top-right）
  - 中央左侧（middle-left）
  - 正中央（center）
  - 中央右侧（middle-right）
  - 左下角（bottom-left）
  - 底部中央（bottom-center）
  - 右下角（bottom-right）

#### 输出处理
- 原文件保持不变
- 处理后的文件保存到`[原目录]_watermark`子目录
- 保持原文件名和格式不变
- 如目标目录不存在则自动创建

### 命令行接口设计

```
photo-watermark [OPTIONS] PATH

OPTIONS:
  -s, --size SIZE          字体大小 (默认: 24)
  -c, --color COLOR        字体颜色 (默认: white)
  -p, --position POSITION  水印位置 (默认: bottom-right)
  -f, --format FORMAT      时间格式 (默认: YYYY-MM-DD)
  --help                   显示帮助信息

PATH: 图片文件或目录路径
```

### 使用示例

```bash
# 为单个文件添加水印，使用默认设置
photo-watermark /path/to/image.jpg

# 为目录中所有图片添加水印，指定字体大小和颜色
photo-watermark -s 36 -c red /path/to/photos/

# 为图片添加水印，指定位置和时间格式
photo-watermark -p top-left -f "YYYY-MM-DD HH:mm:ss" /path/to/image.jpg
```

## 安装说明

### 环境要求
- Python 3.6+

### 安装步骤

1. 克隆或下载项目代码
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

## 使用说明

### 基本使用

直接运行程序并指定图片路径：
```bash
python photo_watermark.py /path/to/image.jpg
```

处理整个目录中的图片：
```bash
python photo_watermark.py /path/to/photos/
```

### 高级选项

自定义水印字体大小：
```bash
python photo_watermark.py -s 36 /path/to/image.jpg
```

自定义水印颜色：
```bash
python photo_watermark.py -c red /path/to/image.jpg
```

自定义水印位置：
```bash
python photo_watermark.py -p top-left /path/to/image.jpg
```

自定义时间格式：
```bash
python photo_watermark.py -f "%Y-%m-%d %H:%M:%S" /path/to/image.jpg
```

### 输出结果

处理后的图片将保存在以下位置：
- 处理单个文件：在文件所在目录创建`[目录名]_watermark`子目录
- 处理目录中的文件：在该目录下创建`[目录名]_watermark`子目录

## 项目结构

```
photo-watermark/
├── photo_watermark.py  # 主程序文件
├── README.md           # 项目说明文档
├── requirements.txt    # 依赖包列表
└── tests/              # 测试文件目录
```

## 后续扩展功能

- 支持自定义时间格式
- 批量处理进度显示
- 支持其他EXIF信息作为水印（如相机型号、光圈等）
- 支持图片水印（而非仅文本水印）
- GUI界面版本