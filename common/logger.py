import logging.handlers
from settings import LOG_DIRECTORY, LOG_LEVEL
import os


const = {
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "CRITICAL": logging.CRITICAL

}


class Logger(logging.Logger):
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        super(Logger, self).__init__(self)
        # 处理指定日志路径不存在问题
        filename = LOG_DIRECTORY
        if not os.path.exists(filename):
            os.makedirs(filename)
        filename = os.path.join(LOG_DIRECTORY, 'log.log')

        # 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)
        fh = logging.handlers.TimedRotatingFileHandler(
            filename, 'MIDNIGHT', 1, 30, encoding='utf-8')
        fh.suffix = "%Y-%m-%d_%H-%M.log"
        fh.setLevel(const[LOG_LEVEL])
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(const[LOG_LEVEL])

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s] - %(filename)s [Line:%(lineno)d] - [%(levelname)s]-[t:%(thread)s]-[p:%(process)s] - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.addHandler(fh)
        self.addHandler(ch)


if __name__ == '__main__':
    log = Logger()
    log.info('无')
