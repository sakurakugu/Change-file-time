import os
import subprocess  # 用于生成持久 PowerShell 实例
from tkinter import Label, Button, Entry
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog
from datetime import datetime
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from tqdm import tqdm

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
# 检查文件扩展名
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

# 生成持久 PowerShell 实例
ps_进程 = subprocess.Popen(
    ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "-"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
# 加载修改时间脚本，并定义一个可复用的函数
ps_进程.stdin.write('. "./资源/修改时间.ps1"\n')
ps_进程.stdin.write('function 修改时间Persistent { param($文件, $修改时间, $修改类型) . "./资源/修改时间.ps1" $文件 $修改时间 $修改类型 }\n')
ps_进程.stdin.flush()

def 修改文件时间(多份文件路径):
    global ps_进程
    修改类型 = 输入框1.get().strip() or "3"
    输入时间 = 输入框2.get().strip()  # 优化：提前读取输入时间
    for 文件 in tqdm(多份文件路径, desc="修改文件进度"):
        文件 = os.path.abspath(文件)
        修改时间 = 输入时间 or 从文件名中提取时间(文件) or 从文件属性中提取时间(文件)
        if not 修改时间:
            标签.config(text="文件中未找到时间！", fg="red")
            print(f"\033[31m{文件}中未找到时间！, 跳过\033[0m")
            continue
        # 调用持久 PowerShell 实例执行修改任务
        命令 = f'修改时间Persistent "{文件}" "{修改时间}" "{修改类型}"\n'
        ps_进程.stdin.write(命令)
        ps_进程.stdin.flush()
        print(f"\033[32m{文件}修改为{修改时间} \033[0m")

def 拖动部分(event):
    多份文件路径 = root.tk.splitlist(event.data)
    文件数量 = len(多份文件路径) # 获取文件数量
    print(f"拖入文件数量: {文件数量}") # 在CLI上输出文件数量
    标签.config(text=f"拖入文件数量: {文件数量}\n", fg="black") # 在GUI上显示文件数量
    if 多份文件路径:
        修改文件时间(多份文件路径)
    标签.config(text="拖放文件到这里\n或", fg="black") # 重置标签文本

def 打开文件对话框():
    多份文件路径 = filedialog.askopenfilenames()
    if 多份文件路径:
        修改文件时间(多份文件路径) 

# 在窗口关闭前先关闭 PowerShell 窗口
def 清理资源():
    global ps_进程
    if ps_进程:
        ps_进程.stdin.close()
        ps_进程.kill()
        
### GUI部分 ###

# 创建主窗口
root = TkinterDnD.Tk()
root.title("批量更改文件时间属性")

# 设置窗口大小
窗口宽度 = 400
窗口高度 = 220

# 获取屏幕宽度和高度
屏幕宽度 = root.winfo_screenwidth()
屏幕高度 = root.winfo_screenheight()

# 计算窗口位置
位置_x = (屏幕宽度 - 窗口宽度) // 2
位置_y = (屏幕高度 - 窗口高度) // 2

# 设置窗口大小和位置
root.geometry(f"{窗口宽度}x{窗口高度}+{位置_x}+{位置_y}")

# 标签
标签 = Label(root, text="拖放文件到这里\n或")
标签.pack(pady=8) # 将标签放置在主窗口上, pady是垂直方向的间距

# 按钮-选择文件
按钮 = Button(root, text="选择文件", command=打开文件对话框)
按钮.pack() # 将按钮放置在主窗口上

# 输入框-修改类型
标签1 = Label(root, text="修改类型：1.创建时间、2.修改时间、4.访问时间（可相加）\n（不填就默认为3）")
标签1.pack()
输入框1 = Entry(root)
输入框1.pack()

# 输入框-修改时间
标签2 = Label(root, text="修改时间(格式：yyyy-MM-dd HH:mm:ss)\n（不填就默认从文件名中获取时间）")
标签2.pack()
输入框2 = Entry(root)
输入框2.pack()

# 注册拖放事件
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', 拖动部分) # “<<Drop>>” 是拖放事件的标志

root.protocol("WM_DELETE_WINDOW", lambda: (清理资源(), root.destroy()))

if __name__ == '__main__':
    root.mainloop()  # 启动消息循环


