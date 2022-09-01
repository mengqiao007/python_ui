import os
import time

import requests
import jsonpath

from businessInfo.wholesaler_business import Wholesaler_Business
from commons.config_util import ConfigUtil
import random

from commons.postposition_util import PostpositionUtil


class BEES_TOOLS():

    def __init__(self, project=0,environment=2,static=0):
        """
        配置文件
        @param project: 0=bees项目，1=mp项目，默认为0
        @param environment: 0=dev环境，1=test环境，2=feature-test环境，默认为2
        @param static: 0=静态token，1=动态token，默认=0
        """
        self.project = project
        self.environment = environment
        self.static = static

        ConfigUtil(project,environment,static).get_environment_config()

    def send_request(self):
        url = "http://abi-cloud-middle-platform-task-center-feature-2.cf56d21c1bce44dcca3b04d4823848fe4.cn-shanghai.alicontainer.com/abi-cloud-middle-platform-task-center/api/tasks/update"
        number = random.randint(1,9999)
        params = {
                  "bizCode": "777",
                  "bizName": "TEST",
                  "code": "T202208041709079140001",
                  "executorTargetCode": f"{number}",
                  "executorTargetName": "烤肉店",
                  "updateBy": "于倩"
                }
        res = requests.post(url=url,json=params)
        time_data = jsonpath.jsonpath(res.json(),"$..timestamp")
        return time_data[0]




if __name__ == '__main__':
    os.system("allure generate ./temps -o ./reports --clean")
    os.system("allure open reports")





