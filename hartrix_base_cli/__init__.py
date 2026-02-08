from nio import *
import asyncio
import logging
import os

from . import customLogger
from . import config

path=None


def main(prefix:str,data:str,args:tuple) -> int:
    global path
    path=prefix

    os.makedirs(data, exist_ok=True)

    customLogger.setup(level=logging.INFO)

    logger = logging.getLogger(__name__)
    logger.debug("这是一个调试信息")
    logger.info("这是一个普通信息")
    logger.warning("这是一个警告信息")
    logger.error("这是一个错误信息")
    logger.critical("这是一个严重错误信息")


    return 0