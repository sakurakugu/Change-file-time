import os
from 资源 import GUI页面
from 资源 import CLI页面

def 初始化():
	"""初始化函数"""
	# 切换目录为当前目录
	os.chdir(os.path.dirname(os.path.abspath(__file__)))
	CLI页面.初始化()
	GUI页面.初始化()

if __name__ == '__main__':
    
	初始化()