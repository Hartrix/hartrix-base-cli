import json
import aiofiles
from . import dataPath,pathJoin
import os
import logging
from colorama import Fore
import asyncio
from typing import List

logger=logging.getLogger(Fore.LIGHTMAGENTA_EX+"CONFIG"+Fore.RESET)

configPath=None


# ====================用户管理====================
class User:
    def __init__(self,homeserver="https://matrix.org",username=None,userId=None,deviceId=None,accessToken=None):
       self.homeserver=homeserver
       self.username=username
       self.userId=userId
       self.deviceId=deviceId
       self.accessToken=accessToken

users:List[User]=[]

async def setupUser():
    """(users.json) 读取用户信息，若没有则创建"""
    if not os.path.exists(pathJoin(configPath,"users.json")): 
        logger.warning("(users.json) 无用户登录，正在创建...")
        async with aiofiles.open(pathJoin(configPath,"users.json"),"w",encoding="utf-8") as f:
            await f.write(json.dumps([],indent=2,ensure_ascii=False))
            await f.close()
    
    logger.info("(users.json) 读取用户信息...")
    async with aiofiles.open(pathJoin(configPath,"users.json"),"r",encoding="utf-8") as f:
        usersJson=json.loads(await f.read())
        for user in usersJson:
            users.append(User(**user))
        await f.close()

async def writeUser():
    """(users.json) 将用户信息写入文件"""
    logger.info("(users.json) 写入用户信息...")
    async with aiofiles.open(pathJoin(configPath,"users.json"),"w",encoding="utf-8") as f:
        usersList=[]
        for user in users:
            userDict={
                "homeserver" : user.homeserver,
                "username"   : user.username,
                "userId"     : user.userId,
                "deviceId"   : user.deviceId,
                "accessToken": user.accessToken

            }
            usersList.append(userDict)
        await f.write(json.dumps(usersList,indent=2,ensure_ascii=False))



# ==================全局设置管理==================
async def setup():
    """初始化所有配置"""
    global configPath
    logger.info("初始化配置...")
    configPath=pathJoin(dataPath,"config")

    if not os.path.exists(configPath):
        os.makedirs(configPath,0o777,True)
    
    await asyncio.gather(setupUser())
    logger.info("配置初始化完成!")

async def write():
    """写所有配置"""
    logger.info("写所有配置...")
    if not os.path.exists(configPath):
        os.makedirs(configPath,0o777,True)
    
    await asyncio.gather(writeUser())
    logger.info("配置写入完成!")