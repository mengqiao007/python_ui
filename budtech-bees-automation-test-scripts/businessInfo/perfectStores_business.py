import json

import requests
import jsonpath
from commons.config_util import ConfigUtil
import random
from commons.logging_util import loggingUtil
from commons.requests_util import RequestsUtilExcel
from commons.yaml_util import read_environment_yaml, write_extract_yaml, read_extract_yaml
from commons.function_util import FunctionUtil
from commons.postposition_util import PostpositionUtil


class PerfectStores_Business():
    pass
    #一、无交易版创建
        #1、调用无交易版邀请码
        #2、完美门店创建， 使用1获得的邀请码


        # 先扫码加入使用尊享会小程序-要权限
        # 登录M1账号 ==>> 完美门店  ==>> 生成邀请码  ==>> 创建售点 ==>>q