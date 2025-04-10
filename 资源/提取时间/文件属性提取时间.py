import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

def 提取时间(文件):
    图片扩展名 = ['.jpg', '.jpeg', '.png', '.tiff', '.bmp'] # 暂时不包括 .git 等文件
    if not os.path.splitext(文件)[1].lower() in 图片扩展名:
        return None
    try:
        图片 = Image.open(文件)
        exif = 图片._getexif()
        if exif:
            for tag, value in exif.items():
                if TAGS.get(tag, tag) == "DateTimeOriginal":
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"[错误]: {文件}: {e}")
    return None