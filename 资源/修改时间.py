import os
from tqdm import tqdm
from 资源 import CLI页面
from .提取时间 import 文件名称提取时间, 文件属性提取时间


def 修改文件时间(多份文件路径, 修改类型="3", 输入时间=""):
    print(修改类型)
    for 文件 in 多份文件路径:
        文件 = os.path.abspath(文件)

        修改时间 = 输入时间 or 文件名称提取时间.提取时间(文件) or 文件属性提取时间.提取时间(文件)
        if not 修改时间:
            print(f"\033[31m{文件}中未找到时间！, 跳过\033[0m")
            continue
        # 加载powershell中的函数“修改时间”
        命令 = f'修改时间 "{文件}" "{修改时间}" "{修改类型}"\n'
        # 命令 = f'修改时间 -path "{文件}" -time "{修改时间}" -Type {修改类型}\n'
        CLI页面.运行命令(命令)
        
        # 获取ps1的错误
        # ps_错误 = CLI页面.ps_进程.stderr.read()
        ps_返回码 = CLI页面.ps_进程.returncode
        if ps_返回码:
            # print(f"\033[31m{文件}修改失败！  \n[错误]: {ps_错误}\033[0m" , end="")
            continue
        
        print(f"\033[32m{文件}修改为 {修改时间} \033[0m")



# 在窗口关闭前先关闭 PowerShell 窗口
def 清理资源():
    CLI页面.清理资源()

