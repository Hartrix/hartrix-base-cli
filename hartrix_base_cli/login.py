from . import clear,config,selectNum
from . import matrix
from getpass import getpass
import platform

async def userList():
    """输出用户列表"""
    await clear()
    userNum=len(config.users)

    for i in range(userNum):
        print(f"{i+1}. {config.users[i].username} ({config.users[i].userId})")
    print(f"\n{userNum+1}. 登录新用户\n")

    choice=selectNum(1,userNum+1)
    if choice==userNum+1:
        await loginNew()

async def loginNew():
    """登录新用户"""
    homeserver=input("家服务器 [https://matrix.org]: ")
    if not homeserver: homeserver="https://matrix.org"
    if not (homeserver.startswith("https://") or homeserver.startswith("http://")):
        homeserver = "https://" + homeserver

    userId = input("用户 ID [@user:example.org]: ")
    if not userId: userId="@user:example.org"
    username = userId[userId.find("@")+1:userId.find(":")]
    print("用户名:",username)

    passwd=""
    while not passwd:
        passwd=getpass("密码：")

    nodename="Hartrix-Base "+platform.node()
    deviceId=input(f"设备 ID [{nodename}]: ")
    if not deviceId: deviceId=nodename

    resp=await matrix.users.loginPasswd(homeserver,userId,passwd,deviceId)

    if isinstance(resp, matrix.users.LoginResponse):
        config.users.append(config.User(
            homeserver=homeserver,
            username=username,
            userId=resp.user_id,
            deviceId=resp.device_id,
            accessToken=resp.access_token
        ))
        await config.writeUser()