import requests
import jsonpath

from commons.logging_util import loggingUtil
from commons.yaml_util import write_environment_yaml, read_environment_yaml, clear_extract_yaml, clear_environment_yaml
from commons.yaml_util import read_config_yaml
from commons.function_util import FunctionUtil


# 环境配置方法类
class ConfigUtil():

    def __init__(self, project=0, environment=0, static=0):
        """
        配置文件
        @param project: 0=bees项目，1=mp项目，默认为0
        @param environment: 0=dev环境，1=test环境，2=feature-test环境，默认为0 5=feature-5环境
        @param static: 0=静态token，1=动态token，默认=0
        """
        clear_extract_yaml()
        clear_environment_yaml()

        self.project = project
        self.environment = environment
        self.static = static


    def get_login_token_by_smscode(self, PHONE, SMSCODE):
        """
        通过短信验证码登录，获取验证码
        @param PHONE: 手机号
        @param SMSCODE: 验证码
        @return: token
        """
        base_url = read_environment_yaml("bees_user_service")
        url = base_url + f"user-service/login/login-by-smscode"
        login_json = {"phone": PHONE, "smsCode": SMSCODE}
        res = requests.post(url, json=login_json)
        authentoken = FunctionUtil().jsonpath_field(res.json(),"..token")
        return authentoken


    def get_login_token_by_pwd(self, userNameOrPhone, password):
        """
        通过账号密码登录，获取token
        @param userNameOrPhone: 账号
        @param password: 密码
        @return: token
        """
        base_url = read_environment_yaml("bees_user_service")
        url = base_url + f"user-service/login/login-by-pwd"
        login_json = {"userNameOrPhone": userNameOrPhone, "password": FunctionUtil().rsa_encrpt(password)}
        res = requests.post(url, json=login_json)
        authentoken = FunctionUtil().jsonpath_field(res.json(), "..token")
        return authentoken


    def write_extract_bees_token(self, static_data):

        if self.environment == 0 or self.environment ==5:
            for token in static_data:
                PHONE = static_data[token]["PHONE"]
                SMSCODE = static_data[token]["SMSCODE"]
                value = self.get_login_token_by_smscode(PHONE, SMSCODE)
                token_dict = {token: value}
                write_environment_yaml(token_dict)



        elif self.environment == 2:
            for token in static_data:
                userNameOrPhone = static_data[token]["userNameOrPhone"]
                password = static_data[token]["password"]
                value = self.get_login_token_by_pwd(userNameOrPhone, password)
                token_dict = {token: value}
                write_environment_yaml(token_dict)

        else:
            loggingUtil().get_error_log(f"未找到对应环境：write_extract_bees_token")


    def write_environment_base_url(self, url_data):
        for url in url_data:
            url_dict = {url: url_data[url]}
            write_environment_yaml(url_dict)

    def get_environment_config(self):
        """
        获取环境配置
        project 0为bees项目，1为mp项目        默认为0：bees项目
        environment 0为dev环境，1为test环境，2为feature-test环境  默认为2：feature-test环境
        static 0为静态token，1为动态token    默认为0：静态token
        """

        # 判断项目
        if self.project == 0:

            project_data = read_config_yaml("PROJECT_BBES")
            write_environment_yaml({"project" : "Bees"})
            environment_data = ""
            # 判断环境
            if self.environment == 0:
                environment_data = "ENVIRONMENT_DEV"
                write_environment_yaml({"environment": "Dev"})
            elif self.environment == 2:
                environment_data = "ENVIRONMENT_FEATURE_TEST"
                write_environment_yaml({"environment": "FeatureTest"})
            elif self.environment == 5:
                environment_data = "ENVIRONMENT_FEATURE_5"
                write_environment_yaml({"environment": "Feature5"})
            else:
                loggingUtil().get_error_log(f"未找到对应环境：get_environment_config")
                exit()

            base_url = project_data[environment_data]["BASE_URL"]
            self.write_environment_base_url(base_url)
            write_environment_yaml({"MYSQL_CONNECT": project_data[environment_data]["MYSQL_CONNECT"]})

            # 判断静态动态
            if self.static == 0:
                static_data = project_data[environment_data]["STATIC_TOKEN"]
                write_environment_yaml({"token_method": "Static"})
                self.get_static_token(static_data)

            elif self.static == 1:
                static_data = project_data[environment_data]["DYNAMIC_TOKEN"]
                write_environment_yaml({"token_method": "Dynamic"})
                self.write_extract_bees_token(static_data)
                write_environment_yaml({"bees_m1_token": project_data[environment_data]["STATIC_TOKEN"]["bees_m1_token"]})
            else:
                loggingUtil().get_error_log(f"未找到对应选项：self.static")
                exit()


        elif self.project == 1:

            project_data = read_config_yaml("PROJECT_MP")
            write_environment_yaml({"project": "MP"})
            environment_data = ""

            # 判断环境
            if self.environment == 0:
                environment_data = "ENVIRONMENT_DEV"
                write_environment_yaml({"environment": "Dev"})
            elif self.environment == 1:
                environment_data = "ENVIRONMENT_TEST"
                write_environment_yaml({"environment": "Test"})
            elif self.environment == 2:
                environment_data = "ENVIRONMENT_FEATURE_TEST"
                write_environment_yaml({"environment": "FeatureTest"})
            else:
                loggingUtil().get_error_log(f"未找到对应环境：get_environment_config")
                exit()

            base_url = project_data[environment_data]["BASE_URL"]
            self.write_environment_base_url(base_url)
            write_environment_yaml({"MYSQL_CONNECT":project_data[environment_data]["MYSQL_CONNECT"]})

            # 判断静态动态
            if self.static == 0:
                self.get_static_token(project_data[environment_data]["STATIC_TOKEN"])
                write_environment_yaml({"token_method": "Static"})
            elif self.static == 1:
                self.write_extract_mp_token(project_data[environment_data]["DYNAMIC_TOKEN"])
                write_environment_yaml({"token_method": "Dynamic"})
            else:
                loggingUtil().get_error_log(f"未找到对应选项：self.static")
                exit()



        else:
            loggingUtil().get_error_log(f"未找到对应项目：self.project")
            exit()

    def get_static_token(self, token_data):
        """
        获取token
        """
        for token in token_data:
            token_dict = {token: token_data[token]}
            write_environment_yaml(token_dict)


    def write_extract_mp_token(self,token_data):
        for token in token_data:
            USER_NAME = token_data[token]["USER_NAME"]
            PASSWORD = token_data[token]["PASSWORD"]
            base_url = read_environment_yaml("mp_base_url")
            url = base_url + "abi-cloud-middle-platform-auth-service/login/password"

            login_json = {"account": USER_NAME, "password": FunctionUtil().rsa_encrpt(PASSWORD)}
            res = requests.post(url=url, json=login_json)

            satoken = jsonpath.jsonpath(res.json(), f"$..tokenValue")

            token_dict = {token: satoken[0]}
            write_environment_yaml(token_dict)
