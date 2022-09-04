import logging

# 创建一个日志器
import time

from commons.yaml_util import get_object_path

#日志类
class loggingUtil:

    def getlogger(self):
        self.logger = logging.getLogger("logger")
        if not self.logger.handlers:
            # 日志输出默认级别Warning及以上级别信息
            self.logger.setLevel(logging.DEBUG)
            # 创建一个处理器  StreamHandler()控制台实现日志输出
            sh = logging.StreamHandler()
            # 创建一个格式器（日志内容：时间 文件 日志级别  日志描述信息）
            formatter = logging.Formatter(fmt="%(asctime)s | %(filename)s(%(lineno)d 行) | %(levelname)s| %(message)s",
                                          datefmt="%Y/%m/%d %H:%M:%S")
            # 创建一个处理器  文件处理器 文件写入日志
            fh = logging.FileHandler(filename="{}_log.txt".format(
                get_object_path() + "/logs/" + time.strftime("%Y%m%d%H%M%S", time.localtime())), encoding="utf-8")

            formatter2 = logging.Formatter(fmt="%(asctime)s | %(filename)s | %(levelname)s| %(message)s",
                                           datefmt="%Y/%m/%d %H:%M:%S")

            # 控制台输出
            # self.logger.addHandler(sh)
            # sh.setFormatter(formatter2)
            # sh.setLevel(logging.INFO)

            # 日志输出
            self.logger.addHandler(fh)
            fh.setFormatter(formatter2)
        return self.logger

    # 错误信息日志
    def get_error_log(self, message):
        self.getlogger().error(message)
        raise Exception(message)

    # 信息日志
    def get_info_log(self, message):
        self.getlogger().info(message)
