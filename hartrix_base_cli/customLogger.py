import logging
from colorama import Fore, Style
import sys

class CustomFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%', validate=True, *,
                 defaults=None, colored=True):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style, validate=validate, defaults=defaults)
        self.colored = colored

    """被修改后的Formatter (虽然我完全能用colorlog.ColoredFormatter lol"""
    def format(self, record):
        # 格式化日志级别
        if record.levelname == 'DEBUG':
            record.levelname = (Fore.LIGHTCYAN_EX + "DBUG" + Style.RESET_ALL) \
                if self.colored else "DBUG"
            
        elif record.levelname == 'INFO':
            record.levelname = (Fore.LIGHTGREEN_EX + "INFO" + Style.RESET_ALL) \
                if self.colored else "INFO"
            
        elif record.levelname == 'WARNING' or record.levelname == 'WARN':
            record.levelname = (Fore.YELLOW + "WARN" + Style.RESET_ALL) \
                if self.colored else "WARN"
            
        elif record.levelname == 'ERROR':
            record.levelname = (Fore.LIGHTRED_EX + "ERR!" + Style.RESET_ALL) \
                if self.colored else "ERR!"
            
        elif record.levelname == 'CRITICAL' or record.levelname == 'FATAL':
            record.levelname = (Style.BRIGHT + Fore.RED + "FALT" + Style.RESET_ALL) \
                if self.colored else "FALT"

        record.levelname = "[" + record.levelname + "]"
        

        # 格式化logger名称
        record.name = ("[" + Fore.LIGHTBLUE_EX + record.name + Style.RESET_ALL + "]") \
            if self.colored else ("[" + record.name + "]")

        # ↓↓↓↓↓↓ 以下代码修改自自logging.Formatter.format的源代码 ↓↓↓↓↓↓
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = "[" + Fore.LIGHTBLACK_EX + self.formatTime(record, self.datefmt) + Style.RESET_ALL + "]" \
                if self.colored else ("[" + self.formatTime(record, self.datefmt) + "]")
        s = self.formatMessage(record)

        # 格式化Traceback
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        return s

def setup(level=logging.INFO):
    """配置自定义的日志格式"""
    formatter = CustomFormatter(
        fmt=(
            '%(asctime)s '
            '%(levelname)s '
            '%(name)s '
            '%(message)s'
        ),
        datefmt='%H:%M:%S',
        style='%'
    )
    
    root_logger = logging.getLogger()
    # 清除所有现有的处理器
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(level)

def fileHandler():
    pass