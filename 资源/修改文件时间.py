import os
from datetime import datetime
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from tqdm import tqdm
import 资源.ps_cli as ps_cli

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
    图片扩展名 = ['.jpg', '.jpeg', '.png', '.tiff', '.bmp'] # 跳过 .git 等文件
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
        print(f"Error processing {文件}: {e}")
    return None

# 切换目录为当前文件所在目录
当前目录 = os.path.dirname(os.path.abspath(__file__))
os.chdir(当前目录)

ps_cli.初始化_ps()

def 修改文件时间(多份文件路径, 修改类型="3", 输入时间=""):
    for 文件 in 多份文件路径:
        文件 = os.path.abspath(文件)
        修改时间 = 输入时间 or 从文件名中提取时间(文件) or 从文件属性中提取时间(文件)
        if not 修改时间:
            print(f"\033[31m{文件}中未找到时间！, 跳过\033[0m")
            continue
        命令 = f'xgsj "{文件}" "{修改时间}" "{修改类型}"\n'
        ps_cli.运行命令(命令)
        print(f"\033[32m{文件}修改为 {修改时间} \033[0m")



# 在窗口关闭前先关闭 PowerShell 窗口
def 清理资源():
    ps_cli.清理资源()

if __name__ == '__main__':
    pass


