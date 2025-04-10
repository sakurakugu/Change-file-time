from pathlib import Path
from datetime import datetime

def 时间戳转换为时间(时间戳):
    try:
        时间 = datetime.fromtimestamp(int(时间戳)).strftime("%Y-%m-%d %H:%M:%S")
        return 时间
    except ValueError:
        return None # 如果转换失败，返回None

def 提取时间(文件):
    文件名 = Path(文件).stem # 去除后缀
    文件名 = 文件名.strip() # 去除文件名前后的空格
    文件名 = 文件名.replace("_", "-").replace(" ", "-") # 去除文件名中的空格
    
    
    # 如果开头是“img-”/“IMG-”,查看后面的是不是时间戳，并转换为时间格式
    
    ###
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