import asyncio
import logging
import os,sys
from getpass import getpass
import traceback

from colorama import init as c_init, Fore, Style
c_init()

# 以下部分被其它模块所需要
pathJoin=os.path.join
path:str="."
dataPath:str="./data"
logger=logging.getLogger(Fore.LIGHTRED_EX+"MAIN"+Fore.RESET)

async def clear():
    print('\x1b[H\x1b[2J\x1b[3J', end='')

from . import customLogger
from . import config
from . import login

def traceback2log(exc_type, exc_value, exc_traceback):
    """
    将Traceback转到日志里
    """
    #获取报错信息
    tbdata="".join(traceback.format_exception_only(exc_type,exc_value))
    tbdata += "".join(traceback.format_tb(exc_traceback))
    if tbdata.endswith('\n'):
        tbdata = tbdata[:-1]

    logger.critical(tbdata) #输出

async def selectNum(rangeBegin:int,rangeEnd:int) -> int:
    """引导用户输入数字"""
    while True:
        choiceStr=input("选择: ")
        if choiceStr!="":
            try:
                choice=int(choiceStr)
            except:
                print("输入数字! ")
            else:
                if rangeBegin<=choice<=rangeEnd:
                    break
                else:
                    print(f"输入一个从{rangeBegin}-{rangeEnd}之间的数! ")
    return choice

async def main(prefix:str,data:str,args:tuple) -> int:
    global path,dataPath
    path=prefix
    dataPath=data

    # ====================全局初始化====================
    # 日志初始化
    await customLogger.setup(level=logging.INFO)
    sys.excepthook=traceback2log

    # 数据目录初始化
    try:
        os.makedirs(data, 0o777, True)
        os.chmod(data,0o777)
        for dirpath,dirnames,files in os.walk(data):
            os.chmod(dirpath,0o777)
            for dirname in dirnames:
                os.chmod(pathJoin(dirpath,dirname),0o777)
            for file in files:
                os.chmod(pathJoin(dirpath,file),0o666)
    except PermissionError as e:
        logger.critical("无法为数据分区设置权限！请手动设置它")
        sys.exit(1)

    # 配置初始化
    await config.setup()

    


    return 0