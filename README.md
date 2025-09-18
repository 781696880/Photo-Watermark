# Photo-Watermark

Photo-Watermark 是一个轻量级的 Python 命令行工具，用于自动为照片添加基于拍摄时间的文本水印。该工具读取图片的 EXIF 元数据，提取拍摄时间，并将该时间作为水印文本添加到图片上。

## 功能特性

- 自动读取图片 EXIF 信息中的拍摄时间（优先使用 DateTimeOriginal）
- 支持自定义水印的字体大小、颜色和位置
- 支持处理单个文件或整个目录
- 将处理后的图片保存到 `[原目录]_watermark` 子目录中，保留原图不变
- 支持 JPEG、PNG 等主流图像格式
- 命令行友好，易于脚本集成

## 安装说明

### 环境要求

- Python 3.6+
- Pillow >= 8.0.0
- piexif >= 1.1.3

### 安装步骤

1. 克隆或下载项目代码
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

### 基本用法

处理单个图片文件：
```bash
python photo_watermark.py /path/to/image.jpg
```

处理整个目录中的所有图片：
```bash
python photo_watermark.py /path/to/photos/
```

### 高级选项

| 选项 | 全称 | 默认值 | 描述 |
|------|------|--------|------|
| `-s` | `--size` | 24 | 字体大小 |
| `-c` | `--color` | white | 字体颜色 |
| `-p` | `--position` | bottom-right | 水印位置 |
| `-f` | `--format` | %Y-%m-%d | 时间格式 |

### 位置选项

支持以下水印位置：
- `top-left` - 左上角
- `top-center` - 顶部中央
- `top-right` - 右上角
- `middle-left` - 中央左侧
- `center` - 正中央
- `middle-right` - 中央右侧
- `bottom-left` - 左下角
- `bottom-center` - 底部中央
- `bottom-right` - 右下角（默认）

### 使用示例

为单个文件添加水印，使用默认设置：
```bash
python photo_watermark.py /path/to/image.jpg
```

为目录中所有图片添加水印，指定字体大小和颜色：
```bash
python photo_watermark.py -s 36 -c red /path/to/photos/
```

为图片添加水印，指定位置和时间格式：
```bash
python photo_watermark.py -p top-left -f "%Y-%m-%d %H:%M:%S" /path/to/image.jpg
```

## 输出结果

处理后的图片将保存在以下位置：
- 处理单个文件：在文件所在目录创建 `[目录名]_watermark` 子目录
- 处理目录中的文件：在该目录下创建 `[目录名]_watermark` 子目录

例如，处理位于 `/home/user/photos/vacation/` 目录中的图片时，输出将保存在 `/home/user/photos/vacation/vacation_watermark/` 目录中。

## 项目结构

```
photo-watermark/
├── photo_watermark.py     # 主程序文件
├── README.md              # 项目说明文档
├── requirements.txt       # 依赖包列表
├── tests/                 # 测试文件目录
│   ├── __init__.py
│   └── test_photo_watermark.py
└── WORKPLAN.md            # 工作计划文档
```

## 开发与测试

运行测试：
```bash
python -m pytest tests/
```

或者直接运行测试文件：
```bash
python tests/test_photo_watermark.py
```
