from tkinter import Label, Button, Entry, filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from .修改时间 import 修改文件时间, 清理资源

root,标签0,按钮,标签1,输入框1,标签2,输入框2 = None, None, None, None, None, None, None

def 拖动部分(event):
	多份文件路径 = root.tk.splitlist(event.data)
	if 多份文件路径:
		修改类型 = 输入框1.get().strip() or "3"
		输入时间 = 输入框2.get().strip()
		修改文件时间(多份文件路径, 修改类型, 输入时间)
 

def 打开文件对话框():
	多份文件路径 = filedialog.askopenfilenames()
	if 多份文件路径:
		修改类型 = 输入框1.get().strip() or "3"
		输入时间 = 输入框2.get().strip()
		修改文件时间(多份文件路径, 修改类型, 输入时间)
  

def 初始化():
    global root, 标签0, 按钮, 标签1, 输入框1, 标签2, 输入框2
	# 创建主窗口
    root = TkinterDnD.Tk()
    root.title("批量更改文件时间属性")

    # 设置窗口大小和位置
    窗口宽度 = 400
    窗口高度 = 220
    屏幕宽度 = root.winfo_screenwidth()
    屏幕高度 = root.winfo_screenheight()
    位置_x = (屏幕宽度 - 窗口宽度) // 2
    位置_y = (屏幕高度 - 窗口高度) // 2
    root.geometry(f"{窗口宽度}x{窗口高度}+{位置_x}+{位置_y}")

    # 控件
    标签0 = Label(root, text="拖放文件到这里\n或")
    标签0.pack(pady=8)

    按钮 = Button(root, text="选择文件", command=打开文件对话框)
    按钮.pack()

    标签1 = Label(root, text="修改类型：1.创建时间、2.修改时间、4.访问时间（可相加）\n（不填就默认为3）")
    标签1.pack()
    输入框1 = Entry(root)
    输入框1.pack()

    标签2 = Label(root, text="修改时间(格式：yyyy-MM-dd HH:mm:ss)\n（不填就默认从文件名中获取时间）")
    标签2.pack()
    输入框2 = Entry(root)
    输入框2.pack()

    # 注册拖放事件
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', 拖动部分)

    root.protocol("WM_DELETE_WINDOW", lambda: (清理资源(), root.destroy()))

    root.mainloop()
