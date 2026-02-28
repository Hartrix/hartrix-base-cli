from nio import (
    AsyncClient,

    LoginResponse,
    LoginError
)

from typing import Dict,Union

clients:Dict[str,AsyncClient] = {}

async def loginPasswd(homeserver:str,userId:str,passwd:str,deviceId:str) -> Union[LoginResponse,LoginError]:
    """以密码登录Matrix"""
    if userId in clients.keys():
        await clients[userId].close() # 先把已登录会话退出（虽然一般不会出现此情况）

    clients[userId]=AsyncClient(homeserver=homeserver,user=userId)
    resp=await clients[userId].login(password=passwd,device_id=deviceId)

    return resp

async def loginToken(homeserver:str,userId:str,accessToken:str,deviceId:str):
    """用access_token登录Matrix"""
    pass