from nio import *
import asyncio
import logging
import os
from getpass import getpass

pathJoin=os.path.join

from colorama import init as c_init, Fore, Style
c_init()

from . import customLogger
from . import config
from . import login

path=None

async def clear():
    print('\x1b[H\x1b[2J\x1b[3J', end='')

async def main(prefix:str,data:str,args:tuple) -> int:
    global path
    path=prefix

    # ====================全局初始化====================
    # 日志初始化
    await customLogger.setup(level=logging.INFO)
    logger = logging.getLogger(Fore.LIGHTRED_EX+"MAIN"+Fore.RESET)

    # 数据目录初始化
    try:
        os.makedirs(data, 666, True)
        os.chmod(data,0o666)
        for _,_,file in os.walk(data):
            os.chmod(file,0o666)
    except OSError:
        logger.critical("无法为数据分区设置权限！请手动设置它")
        return 1

    # 配置初始化
    await config.setup()

    if len(config.users)==0: # 以下内容计划放到login.py里
        await clear()
        print("看来你没有登录任何账号，让我们登录一个")

        homeserver=input("家服务器 [https://matrix.org]: ")
        if not homeserver: homeserver="https://matrix.org"
        if not (homeserver.startswith("https://") or homeserver.startswith("http://")):
            homeserver = "https://" + homeserver

        user_id = input("用户 ID [@user:example.org]: ")
        if not user_id: user_id="@user:example.org"


    return 0