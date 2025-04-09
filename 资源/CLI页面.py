import subprocess

ps_进程 = None

def 初始化():
    global ps_进程
    ps_进程 = subprocess.Popen(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "-"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    ps_进程.stdin.write('. "./资源/修改属性.ps1"\n')
    ps_进程.stdin.flush()

def 运行命令(cmd):
    global ps_进程
    if ps_进程:
        ps_进程.stdin.write(cmd)
        ps_进程.stdin.flush()

def 清理资源():
    global ps_进程
    if ps_进程:
        ps_进程.stdin.close()
        ps_进程.kill()
        ps_进程 = None
