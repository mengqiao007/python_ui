import json
import re

import allure
import jsonpath
import requests

from commons.excel_util import get_Excel_All_index
from commons.function_util import FunctionUtil
from commons.logging_util import loggingUtil
from commons.mysql_util import mysql_select, mysql_rollback
from commons.yaml_util import write_extract_yaml, read_config_yaml, get_object_path, read_extract_yaml, \
    read_environment_yaml


# 请求工具类
class RequestsUtilExcel:

    session = requests.session()

    def __init__(self):
        self.flag = 0
        self.url = ""
        self.method = ""
        self.param = {}
        self.mysql_name = ""
        self.request_extract = ""
        self.mysql_extract = ""
        self.mysql_assert = ""
        self.mysql_rollback = ""
        self.service = ""
        self.response_extract = ""

    def mark_text_fail(self, msg):
        self.flag += 1
        loggingUtil().get_info_log(msg)

    # excel测试用例数据标准
    def standard_excel(self, case_info):

        method, url, param, header, extract, code, text, download, upload = self.data_format(case_info)

        res = self.send_request(method, url, param, header, download, upload)

        # 断言
        if download:
            loggingUtil().get_info_log("此接口为下载接口，不做响应码及文本断言")
        else:
            response_time = res.elapsed.total_seconds()
            return_json = self.res_json(res)

            if extract is not None:
                self.extract_value(extract, res)

            self.assert_result(code, text, return_json, response_time)

    # 数据格式化
    def data_format(self, case_info):

        loggingUtil().get_info_log("--------------接口测试开始--------------")
        loggingUtil().get_info_log("用例标题：" + str(case_info["用例标题"]))

        self.mysql_name = case_info["数据库名称"]
        self.request_extract = case_info["请求报文提取"]
        self.response_extract = case_info["响应报文提取"]
        self.mysql_extract = case_info["数据库提取"]
        self.mysql_assert = case_info["数据库断言报文"]
        self.mysql_rollback = case_info["数据回滚"]
        self.service = case_info["所属服务"]
        method = case_info["请求方式"]
        url = case_info["请求地址"]
        param = case_info["请求参数"]
        header = case_info["请求头"]
        extract = case_info["提取表达式"]
        code = case_info["响应码断言"]
        text = case_info["响应文本断言"]
        download = case_info["下载文件路径"]
        upload = case_info["上传文件路径"]
        title = case_info["用例标题"]
        medule = case_info["接口模块"]
        version = case_info["版本号"]

        # allure报告数据
        self.allure_title(title, medule, version)

        return method, url, param, header, extract, code, text, download, upload

    @allure.step('{step_name}')
    def request_from_db(self, step_name, case_info, step, api):
        # allure报告数据
        self.allure_title(case_info["name"], case_info["module_name"], case_info["version"])

        self.mysql_name = step["database_name"]
        self.request_extract = step["request_pick"]
        self.mysql_extract = step["request_pick"]
        self.mysql_assert = step["database_assert_text"]
        self.mysql_rollback = step["rollback"]
        self.service = case_info["service_name"]
        # 发送请求
        loggingUtil().get_info_log("--------------接口测试开始--------------")
        loggingUtil().get_info_log("用例标题：" + case_info["name"] + ":" + step_name)
        res = self.send_request(
            api["method"],
            api["uri"],
            step["request_params"],
            step["request_header"],
            step["download_path"],
            step["upload_path"]
        )

        # 断言
        if step["download_path"]:
            loggingUtil().get_info_log("此接口为下载接口，不做响应码及文本断言")
        else:
            response_time = res.elapsed.total_seconds()
            return_json = self.res_json(res)

            if step["expression"] is not None:
                self.extract_value(step["expression"], res)

            self.assert_result(step["assert_code"], step["assert_text"], return_json, response_time)

    # 统一请求封装
    def send_request(self, method, url, param, header, download, upload):

        method = str(method).upper()

        url = read_environment_yaml(str(self.service)) + self.replace_value(url)
        self.url = url

        if param:
            if "null" or "false" or "true" in param:
                param = str(param).replace("null", "None")
                param = str(param).replace("false", "False")
                param = str(param).replace("true", "True")
                param = self.replace_value(param)
                param = eval(param)
            else:
                param = self.replace_value(param)
                param = eval(param)

        self.method = method.upper()
        self.param = param
        loggingUtil().get_info_log("请求方式：" + str(method).upper())
        loggingUtil().get_info_log("请求路径：" + str(url))
        loggingUtil().get_info_log("请求参数：" + str(param))

        return self.header_replace(header, url, method, param, download, upload)

    # 判断请求头
    def header_replace(self, header, url, method, param, download, upload):
        try:

            if download:
                self.download_request(method, url, header, download, param)

            elif upload:
                if header:
                    header = self.replace_value(eval(header))
                    upload = get_object_path() + "/files/" + upload
                    loggingUtil().get_info_log("请求头：" + str(header))
                    file = {'file': open(upload, 'rb')}
                    if param:
                        return RequestsUtilExcel.session.request(method=method, url=url, files=file, headers=header,
                                                                 data=param)
                    else:
                        return RequestsUtilExcel.session.request(method=method, url=url, files=file, headers=header)
                else:
                    upload = get_object_path() + "/files/" + upload
                    file = {'file': open(upload, 'rb')}
                    if param:
                        return RequestsUtilExcel.session.request(method, url, files=file, data=param)
                    else:
                        return RequestsUtilExcel.session.request(method, url, files=file)
            else:
                if header:
                    header = self.replace_value(eval(header))
                    loggingUtil().get_info_log("请求头：" + str(header))
                    if method.lower() == "post" or method.lower() == "put":
                        return RequestsUtilExcel.session.request(method, url, json=param, headers=header)
                    elif method.lower() == "get":
                        return RequestsUtilExcel.session.request(method=method, url=url, params=param, headers=header)
                    elif method.lower() == "delete":
                        if "Content-Type" in header:
                            return RequestsUtilExcel.session.request(method=method, url=url, params=param,
                                                                     headers=header)
                        else:
                            return RequestsUtilExcel.session.request(method, url, json=param, headers=header)
                else:
                    if method.lower() == "post" or method.lower() == "put":
                        return RequestsUtilExcel.session.request(method, url, json=param)
                    elif method.lower() == "get":
                        return RequestsUtilExcel.session.request(method, url, params=param)
                    elif method.lower() == "delete":
                        if "Content-Type" in header:
                            return RequestsUtilExcel.session.request(method=method, url=url, params=param)
                        else:
                            return RequestsUtilExcel.session.request(method, url, json=param)
        except Exception as e:
            loggingUtil().get_error_log(str(e) + "请求头替换并发送请求header_replace异常")
            raise e

    # 下载发送请求
    def download_request(self, method, url, header, download, param):
        try:
            if header:
                header = self.replace_value(eval(header))
                loggingUtil().get_info_log("请求头：" + str(header))
                download = get_object_path() + "/files/" + download

                # 判断参数
                if param:
                    if method.lower() == "get":
                        res = RequestsUtilExcel.session.request(method=method, url=url, headers=header,
                                                                params=param).content
                        self.read_execl_input_log(download, res)
                    else:
                        res = RequestsUtilExcel.session.request(method=method, url=url, headers=header,
                                                                json=param).content
                        self.read_execl_input_log(download, res)
                else:
                    res = RequestsUtilExcel.session.request(method=method, url=url, headers=header).content
                    self.read_execl_input_log(download, res)

            else:
                loggingUtil().get_info_log("无请求头")
                download = get_object_path() + "/files/" + download
                res = RequestsUtilExcel.session.request(method=method, url=url).content
                self.read_execl_input_log(download, res)

        except Exception as e:
            loggingUtil().get_error_log(str(e) + "下载发送请求download_request异常")
            raise e

    # 读取excel数据并输出到log
    @staticmethod
    def read_execl_input_log(download, res):
        with open(download, "wb") as f:
            f.write(res)
        lis = get_Excel_All_index(download)
        if lis:
            loggingUtil().get_info_log("下载接口，获取文件内容：" + str(lis))
        else:
            assert lis != []
            loggingUtil().get_error_log("下载接口，获取文件内容为空：")

    # 返回文本判断
    @staticmethod
    def res_json(res):
        try:
            return_json = res.json()
            return return_json
        except Exception as e:
            loggingUtil().get_error_log(str(e) + "返回文本判断res_json异常，返回结果不是JSON数据格式")
            raise e

    # 替换数据
    @staticmethod
    def replace_value(data):
        try:
            if data:

                data_type = type(data)

                if isinstance(data, dict) or isinstance(data, list):
                    str_data = json.dumps(data)

                else:
                    str_data = str(data)

                for counts in range(1, str_data.count("${") + 1):
                    if "${" in str_data and "}" in str_data:
                        start_index = str_data.index("${")
                        end_index = str_data.index("}", start_index)
                        old_value = str_data[start_index:end_index + 1]

                        function_name = old_value[2:old_value.index('(')]
                        args_value1 = old_value[old_value.index('(') + 1:old_value.index(')')]

                        if args_value1 != "":
                            args_value2 = args_value1.split(',')
                            new_value = getattr(FunctionUtil(), function_name)(*args_value2)
                        else:
                            new_value = getattr(FunctionUtil(), function_name)()

                        if isinstance(new_value, int) or isinstance(new_value, float):
                            str_data = str_data.replace('"' + old_value + '"', str(new_value))
                        else:
                            str_data = str_data.replace(old_value, str(new_value))

                # 还原数据类型
                if isinstance(data, dict) or isinstance(data, list):
                    data = json.loads(str_data)

                else:
                    data = data_type(str_data)

            return data
        except Exception as e:
            loggingUtil().get_error_log(str(e) + "封装替换数据replace_value异常")
            raise e

    # 提取变量
    @staticmethod
    def extract_value(extract, res):
        try:
            for key, value in eval(extract).items():

                if "(.*?)" in value or "(.+?)" in value:
                    zz_value = re.search(value, res.text)

                    if zz_value:
                        extract_value = {key: zz_value.group(1)}
                        write_extract_yaml(extract_value)

                else:
                    js_value = jsonpath.jsonpath(res.json(), value)

                    if js_value:
                        extract_value = {key: js_value[0]}
                        write_extract_yaml(extract_value)
        except Exception as e:
            loggingUtil().get_error_log(str(e) + "提取关联值并写入extract。yaml文件异常")
            raise e

    # 断言结果
    def assert_result(self, code, text, sj_result, response_time):
        loggingUtil().get_info_log("实际结果：" + str(sj_result))
        loggingUtil().get_info_log("响应时间：" + str(response_time) + "秒")

        # 断言响应码
        self.assert_code(code, sj_result)
        # 断言文本
        self.assert_text(text, sj_result)
        # 断言数据库
        self.assert_mysql(sj_result)
        # 生成报告
        self.allure_report(text, sj_result, response_time)

        loggingUtil().get_info_log("接口测试通过")
        loggingUtil().get_info_log("--------------接口测试结束--------------\n")

    # 断言响应码
    def assert_code(self, code, sj_result):

        return_code = sj_result["code"]

        assert eval(code)["code"] == return_code, "断言响应码失败" + "\n" + "断言响应码: " + str(
            eval(code)["code"]) + "\n" + "实际响应码：" + str(return_code)

        if eval(code)["code"] == return_code:
            loggingUtil().get_info_log("断言响应码成功")

        else:
            self.mark_text_fail("断言响应码失败")
            loggingUtil().get_error_log(
                "\n断言响应码为：\t" + str(eval(code)["code"]) +
                "\n实际响应码为：\t" + str(return_code) + "\n"
            )

    # 断言响应文本
    def assert_text(self, text, sj_result):

        if text:
            for key, value in eval(text).items():
                value = self.replace_value(value)
                assert_value = jsonpath.jsonpath(sj_result, f"$..{key}")

                if len(assert_value) == 1:
                    assert_value = str(assert_value[0])

                    assert str(value) == str(assert_value), "断言文本失败" + "\n" + "断言文本内容：" + str(
                        value) + "\n" + "实际本文内容:" + str(assert_value)

                    if str(value) == str(assert_value):
                        loggingUtil().get_info_log("断言文本成功")
                        loggingUtil().get_info_log(f"断言文本=======预期结果{str(key)}值：" + str(value))
                        loggingUtil().get_info_log(f"断言文本=======实际结果{str(key)}值：" + str(assert_value))
                    else:
                        self.mark_text_fail("断言文本失败")
                        loggingUtil().get_error_log(
                            "断言文本为：" + str(key) + ":" + str(value) + "\n" +
                            "实际响应文本为：" + str(key) + ":" + str(assert_value) + "\n")

                        assert str(value) in str(assert_value), "断言文本失败"

                elif len(assert_value) > 1:

                    assert str(value) in str(assert_value), "断言文本失败" + "\n" + "断言文本内容：" + str(
                        value) + "\n" + "实际本文内容:" + str(assert_value)

                    if str(value) in str(assert_value):
                        loggingUtil().get_info_log("断言文本成功")
                        loggingUtil().get_info_log(f"断言文本=======预期结果{str(key)}值：" + str(value))
                        loggingUtil().get_info_log(f"断言文本=======实际结果{str(key)}值：" + str(assert_value))

                    else:
                        self.mark_text_fail("断言文本失败")
                        loggingUtil().get_error_log(
                            "断言文本为：" + str(key) + ":" + str(value) + "\n" +
                            "实际响应文本为：" + str(assert_value) + ":" + str(value) + "\n")

                        assert str(value) in str(assert_value), "断言文本失败"

                else:
                    self.mark_text_fail("断言文本失败")
                    loggingUtil().get_error_log(
                        "断言文本为：" + str(key) + ":" + str(value) + "\n" +
                        "实际响应文本为：" + str(assert_value) + ":" + str(value) + "\n")

                    assert str(value) in str(assert_value), "断言文本失败"
        else:
            loggingUtil().get_info_log("未断言响应文本")


    # 断言数据库
    def assert_mysql(self,sj_result):
        if self.mysql_name:
            mysql_name = self.database_environment(self.mysql_name)

            # 判断服务
            mysql_service = self.database_service(self.service)

            # 请求参数提取
            request_text = ""
            x = ""
            if self.response_extract:
                try:
                    request_text = jsonpath.jsonpath(sj_result, f"$..{self.response_extract}")[0]
                except Exception as e:
                    loggingUtil().get_error_log("响应报文提取错误，请检查" + "提取字段：" + str(self.response_extract) + "响应报文："+str(sj_result))
                    raise e
                x = 1
            elif self.request_extract:
                try:
                    request_text = jsonpath.jsonpath(self.param, f"$..{self.request_extract}")[0]
                except Exception as e:
                    loggingUtil().get_error_log("请求报文提取错误，请检查" + "提取字段：" + str(self.request_extract) + "请求报文："+str(self.param))
                    raise e
                x = 2
            elif self.response_extract == None and self.request_extract == None:
                try:
                    lis = str(self.mysql_extract).split("=")
                    self.mysql_extract = lis[0]
                    request_text = lis[1]
                except Exception as e:
                    loggingUtil().get_error_log("数据库提取字段错误，请检查" + "提取字段：" + str(self.mysql_extract) )
                    raise e
                x = 3
            else:
                loggingUtil().get_error_log("未找到数据库提取参数")

            try:
                mysql_text = self.mysql_extract
                mysql_assert = self.replace_value(self.mysql_assert)
                mysql_res = mysql_select(mysql_service, mysql_name, mysql_assert)
                loggingUtil().get_info_log(f"sql执行=======语句：" + str(mysql_assert))
                loggingUtil().get_info_log(f"sql执行=======结果：" + str(mysql_res))
                res_text = mysql_res[0][mysql_text]
            except Exception as e:
                loggingUtil().get_error_log("数据库执行sql语句异常")
                raise e

            if len(mysql_res) == 1:
                if str(res_text) == str(request_text):
                    loggingUtil().get_info_log("数据库断言成功")
                    if x == 1:
                        loggingUtil().get_info_log(f"数据库断言=======预期结果{self.response_extract}值为：" + str(request_text))
                    elif x == 2:
                        loggingUtil().get_info_log(f"数据库断言=======预期结果{self.request_extract}值为：" + str(request_text))
                    elif x == 3:
                        loggingUtil().get_info_log(
                            f"数据库断言=======预期结果{self.mysql_extract}值为：" + str(request_text))
                    loggingUtil().get_info_log(f"数据库断言=======实际结果{mysql_text}值为：" + str(res_text))

                    if self.mysql_rollback:
                        try:
                            rollback_replact = self.replace_value(self.mysql_rollback)
                            loggingUtil().get_info_log("开始执行回滚")
                            mysql_rollback(mysql_service, mysql_name, rollback_replact)
                            rollback_text = mysql_select(mysql_service, mysql_name, mysql_assert)
                            loggingUtil().get_info_log("执行回滚语句：" + str(rollback_replact))
                            if not rollback_text:
                                loggingUtil().get_info_log("查询回滚之后的结果为==空==,执行回滚成功")
                            else:
                                loggingUtil().get_info_log("修改后的执行回滚结果：" + str(rollback_text))
                        except Exception as e:
                            loggingUtil().get_error_log(f"数据库回滚异常：" + str(mysql_res))
                            raise e

                else:
                    assert mysql_res == request_text
                    loggingUtil().get_error_log("查询结果不相同，请确认")

            elif len(mysql_res) > 1:
                loggingUtil().get_error_log(f"数据非唯一，查询数据库结果为：" + str(mysql_res))
                assert len(mysql_res) == 1

            else:
                assert len(mysql_res) == 1
                loggingUtil().get_error_log("未找到相关数据，请确认" + str(mysql_res))


    # 选择数据局连接服务
    def database_service(self,service):
        try:
            if service == "isales_service":
                return "MYSQL_CONNECT"
            elif service == "business_entity_service":
                return "MYSQL_CONNECT"
            elif service == "products_service":
                return "MYSQL_CONNECT"
        except Exception as e:
            loggingUtil().get_error_log("获取数据库服务异常" + str(service))
            raise e


    # 选择数据库环境
    def database_environment(self,data_name):
        try:
            if data_name == "bees_business_entity":
                environment = read_environment_yaml("environment").lower()
                if environment == "dev" or environment == "feature5":
                    return data_name + "_" + "dev"
                elif environment == "featuretest" :
                    return data_name + "_" + environment
            elif data_name == "bees_products":
                environment = read_environment_yaml("environment").lower()
                if environment == "dev" or environment == "feature5":
                    return data_name + "_" + "dev"
                elif environment == "featuretest" :
                    return data_name + "_" + environment
            else:
                environment = read_environment_yaml("environment").lower()
                return data_name + "_" + environment
        except Exception as e:
            loggingUtil().get_error_log("选择数据库环境异常" + str(data_name))
            raise e


    # 生成报告
    def allure_report(self, text, sj_result, response_time):
        try:
            return_code = sj_result["code"]
            # 判断断言是否成功
            if self.flag == 0:
                allure.attach(
                    "测试结果：" + "通过" + "\n" +
                    "响应状态码：" + str(return_code) + "\n" +
                    "响应时间：" + str(response_time) + "秒" + "\n" +
                    f"请求类型：{self.method}" + " \n" +
                    f"接口地址：{self.url}", "测试结果")

                if text:
                    for key, value in eval(text).items():
                        assert_value = jsonpath.jsonpath(sj_result, f"$..{key}")

                        if len(assert_value) == 1:
                            assert_value = assert_value[0]
                            allure.attach("断言描述：" + "断言响应报文中的" + key + "参数 \n" +
                                          "参数值：" + str(assert_value) + "\n" +
                                          "断言结果：" + "断言成功", "响应断言")
                        else:
                            allure.attach("断言描述：" + "断言响应报文中的" + key + "参数 \n" +
                                          "参数值：" + str(assert_value) + "\n" +
                                          "断言结果：" + "断言成功", "响应断言")
                else:
                    allure.attach("断言描述：" + "未做文本断言" + "\n" +
                                  "参数值：" + "未做文本断言" + "\n" +
                                  "断言结果：" + "未做文本断言", "响应断言")

                allure.attach(str(sj_result), "响应报文")
                allure.attach(str(self.param), "请求报文")

            else:
                allure.attach(
                    "测试结果：" + "不通过" + "\n" +
                    "响应状态码：" + str(return_code) + "\n" +
                    f"请求类型：{self.method}" + " \n" +
                    f"接口地址：{self.url}", "测试结果")
                allure.attach(str(self.param), "请求报文")
                allure.attach(str(sj_result), "响应报文")

                for key, value in eval(text).items():
                    assert_value = jsonpath.jsonpath(sj_result, f"$..{key}")
                    allure.attach("断言描述：" + "断言响应报文中的" + key + "参数 \n" +
                                  "参数值：" + str(assert_value) + "\n" +
                                  "断言结果：" + "断言失败，未找到参数", "响应断言")
        except Exception as e:
            loggingUtil().get_error_log(str(e) + "生成报告allure_report异常\n")
            raise e

    # 测试报告
    @staticmethod
    def allure_title(title, case_name, module):

        allure.dynamic.title(title)
        allure.dynamic.description(title)
        allure.dynamic.story(case_name)
        allure.dynamic.feature(module)

    @staticmethod
    def allure_step(return_code, response_time, method, url, param, sj_result, assert_text, assert_test_result):

        allure.attach(
            "响应状态码：" + str(return_code) + "\n" +
            "响应时间：" + str(response_time) + "秒" + "\n" +
            f"请求类型：{method}" + " \n" +
            f"接口地址：{url}", "测试结果")
        allure.attach(str(assert_text), "预期断言文本")
        allure.attach(str(assert_test_result), "实际断言结果")
        allure.attach(str(sj_result), "响应报文")
        allure.attach(str(param), "请求报文")
