import os
from datetime import datetime
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS

def 从文件名中提取时间(文件):
    文件名 = Path(文件).stem # 去除后缀
    文件名 = 文件名.replace(" ", "") # 去除文件名中的空格
    文件名 = "".join([i for i in 文件名 if i.isdigit() or i in "-_"]) # 只保留数字、-、_
    if 文件名 and not 文件名[0].isdigit(): # 如果第一个字符非数字，去除
        文件名 = 文件名[1:]
    if 文件名 and not 文件名[-1].isdigit(): # 如果不为空且最后一个字符非数字，去除
        文件名 = 文件名[:-1]
    
    格式 = ["%Y%m%d_%H%M%S", "%Y%m%d%H%M%S", "%Y%m%d-%H%M%S", "%Y-%m-%d%H%M%S", "%Y-%m-%d_%H-%M-%S", "%Y-%m-%d%H-%M-%S", ]
    for f in 格式:
        try:
            时间 = datetime.strptime(文件名, f)
            return 时间.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass # 如果格式不对，继续尝试下一个格式
    return None # 如果所有格式都不对，返回None

def 从文件属性中提取时间(文件):
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