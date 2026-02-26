import logging
from colorama import Fore, Style
import sys

class CustomFormatter(logging.Formatter):
    """被修改后的Formatter (虽然我完全能用colorlog.ColoredFormatter lol"""
    
    def __init__(self, fmt=None, datefmt=None, style='%', validate=True, *,
                 defaults=None, colored=True):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style, validate=validate, defaults=defaults)
        self.colored = colored
    
    def _stripConsoleFormat(self, text):
        """
        清理文本中的 ANSI 转义序列
        """
        result = []
        i = 0
        n = len(text)
        
        while i < n:
            # 检查是否是 ANSI 转义序列的开始
            if i + 1 < n and text[i] == '\x1b' and text[i+1] == '[':
                # 跳过整个转义序列，直到找到 'm'
                j = i + 2
                while j < n and text[j] != 'm':
                    j += 1
                if j < n:
                    i = j + 1  # 跳过 'm'
                    continue
            
            # 添加普通字符
            result.append(text[i])
            i += 1
            
        return ''.join(result)

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
            record.levelname = (Style.BRIGHT + Fore.RED + "FAIL" + Style.RESET_ALL) \
                if self.colored else "FAIL"

        record.levelname = "[" + record.levelname + "]"
        

        # 格式化logger名称
        if self.colored:
            record.name = "[" + Fore.LIGHTBLUE_EX + record.name + Style.RESET_ALL + "]"
        else:
            # 如果 self.colored 为 False，清理 record.name 中可能存在的 ANSI 转义序列
            record.name = "[" + self._stripConsoleFormat(record.name) + "]"

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

async def setup(level=logging.INFO):
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