	当前目录 = os.path.dirname(os.path.abspath(__file__))
	print(f"当前目录: {当前目录}")
	os.chdir(当前目录)
	CLI页面.初始化()