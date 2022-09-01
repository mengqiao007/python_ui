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


class Wholesaler_Business():

    def __init__(self):
        """
        配置文件
        @param project: 0=bees项目，1=mp项目，默认为0
        @param environment: 0=dev环境，1=test环境，2=feature-test环境，默认为0
        @param static: 0=静态token，1=动态token，默认=0
        """
        # self.project = project
        # self.environment = environment
        # self.static = static
        #
        # ConfigUtil(project,environment,static).get_environment_config()

        self.wholesaler_name = "BusinessX" + FunctionUtil().random_code()
        self.wholesaler_phone = FunctionUtil().get_phone()
        self.header = {'authentoken': read_environment_yaml("bees_console_token_abi"), 'type': '1'}
        self.header_t1 = {'authentoken': read_environment_yaml("bees_console_token_t1"), 'type': '1'}
        self.parent_id = "1334065882783073822"
        self.salsesman_code = "w0001673"


    def wholesaler_business(self,type):
        """
        经销商流程
        @param type: 1=一级经销商； 2=二级经销商
        @return:
        """
        #1、创建经销商=====返回经销商id
        loggingUtil().get_info_log(f"{type}级经销商业务流程")
        loggingUtil().get_info_log("创建经销商==========================>>>>>>>>>>>>>>>>>>")
        wholesaler_id = self.create_wholesaler(type)

        #查询经销商名称
        wholesalerName = self.select_wholesaler_data(wholesaler_id,"..wholesalerName")
        loggingUtil().get_info_log("通过经销商id查询名称==========================>>>>>>>>>>>>>>>>>>")
        loggingUtil().get_info_log("经销商查询名称："+wholesalerName)

        #断言经销商名称
        loggingUtil().get_info_log("断言经销商名称==========================>>>>>>>>>>>>>>>>>>")
        self.assert_data(self.wholesaler_name, wholesalerName, "断言名称")
        loggingUtil().get_info_log("--------------------------------------------------------")


        #2、修改经销状态改为启用
        loggingUtil().get_info_log("修改经销商状态为启用==========================>>>>>>>>>>>>>>>>>>")
        self.update_wholesaler_status(wholesaler_id,3)

        #查询经销商状态
        loggingUtil().get_info_log("查询经销商状态==========================>>>>>>>>>>>>>>>>>>")
        status = self.select_wholesaler_data(wholesaler_id,".data.status")
        loggingUtil().get_info_log("经销商状态："+str(status))

        #断言经销商状态
        loggingUtil().get_info_log("断言经销商状态==========================>>>>>>>>>>>>>>>>>>")
        self.assert_data(3,status,"断言状态")
        loggingUtil().get_info_log("--------------------------------------------------------")

        #3、编辑经销商
        loggingUtil().get_info_log("编辑经销商==========================>>>>>>>>>>>>>>>>>>")
        self.edit_wholesaler(wholesaler_id,self.wholesaler_name,self.wholesaler_phone,type)

        # 编辑经销商后查询名称
        loggingUtil().get_info_log("编辑经销商后查询名称==========================>>>>>>>>>>>>>>>>>>")
        wholesalerName = self.select_wholesaler_data(wholesaler_id,".data.wholesalerName")
        loggingUtil().get_info_log("编辑经销商后查询名称：" + wholesalerName)
        loggingUtil().get_info_log("断言经销商编辑后名称==========================>>>>>>>>>>>>>>>>>>")

        # 断言编辑后名称
        self.assert_data(read_extract_yaml("edit_name"),wholesalerName,"断言编辑后名称")
        loggingUtil().get_info_log("--------------------------------------------------------")

        #4、修改经销商解冻状态
        if type == 2:

            loggingUtil().get_info_log("type类型为2，解冻经销商==========================>>>>>>>>>>>>>>>>>>")
            self.freeze_wholesaler_status(wholesaler_id,0)
            loggingUtil().get_info_log("查询经销商解冻状态==========================>>>>>>>>>>>>>>>>>>")

            # 查询经销商解冻状态
            freezed = self.select_wholesaler_data(wholesaler_id,".data.freezed")
            loggingUtil().get_info_log("查询经销商解冻状态：" + str(freezed))
            loggingUtil().get_info_log("断言经销商解冻状态==========================>>>>>>>>>>>>>>>>>>")

            # 断言经销商解冻状态
            self.assert_data(0,freezed,"断言经销商解冻状态")
            loggingUtil().get_info_log("--------------------------------------------------------")
        else:
            pass

        # 5、修改经销商状态为未完善
        loggingUtil().get_info_log("修改经销商状态为未完善==========================>>>>>>>>>>>>>>>>>>")
        self.update_wholesaler_status(wholesaler_id,1)

        # 查询经销商状态
        loggingUtil().get_info_log("查询经销商状态==========================>>>>>>>>>>>>>>>>>>")
        status = self.select_wholesaler_data(wholesaler_id,".data.status")
        loggingUtil().get_info_log("经销商状态：" + str(status))

        # 断言经销商状态
        loggingUtil().get_info_log("断言经销商状态为1未完善==========================>>>>>>>>>>>>>>>>>>")
        self.assert_data(1,status,"断言经销商状态为1未完善")
        loggingUtil().get_info_log("--------------------------------------------------------")

        #6、删除经销商
        loggingUtil().get_info_log("删除经销商==========================>>>>>>>>>>>>>>>>>>")
        self.delete_wholesaler(wholesaler_id)

        # 查询删除的经销商信息
        loggingUtil().get_info_log("查询删除的经销商信息==========================>>>>>>>>>>>>>>>>>>")
        delete_message = self.select_wholesaler_data(wholesaler_id,".message")
        loggingUtil().get_info_log("断言查询删除的经销商信息==========================>>>>>>>>>>>>>>>>>>")

        # 断言查询删除的经销商信息
        self.assert_data("经销商不存在！",delete_message,"断言查询删除的经销商信息")
        loggingUtil().get_info_log("--------------------------------------------------------")

        # 生成报告
        self.allure_reports(f"{type}级经销商业务流程", "经销商管理", "business_Test")


    def assert_data(self,expect_result,actual_result,description):
        loggingUtil().get_info_log("预期结果为："+ str(expect_result))
        loggingUtil().get_info_log("实际结果为：" + str(actual_result))
        assert expect_result == actual_result, f"{description}失败，预期结果为：" + str(expect_result) + "实际结果为：" + str(actual_result)



    def allure_reports(self,title,casename,module):
        RequestsUtilExcel().allure_title(title,casename,module)


    def update_delete_wholesaler(self,wholesaler_id):
        self.update_wholesaler_status(wholesaler_id,1)
        self.delete_wholesaler(wholesaler_id)

    def create_wholesaler(self,wholesaler_type):
        """
        创建经销商
        @param wholesaler_type:经销商类型
        @return: 经销商id
        """
        name_data = self.wholesaler_name
        phone_data = self.wholesaler_phone

        url = read_environment_yaml("business_entity_service") + "wholesaler"
        params = ""
        if wholesaler_type == 1:
            params = self.t1_params(name_data,phone_data)
        elif wholesaler_type ==2:
            params =self.t2_params(name_data,phone_data)
        else:
            loggingUtil().get_info_log("经销商类型传参错误，类型为：" + str(wholesaler_type))
            exit()
        res = requests.post(url,json=params,headers=self.header)
        try:
            wholesaler_id = jsonpath.jsonpath(res.json(),"$.data")[0]
        except Exception as e:
            loggingUtil().get_info_log("创建经销商异常，返回结果为：" + str(res.json()))
            raise e
        if wholesaler_id !=False:
            loggingUtil().get_info_log("创建经销商成功,返回参数：" + str(res.json()))
            return wholesaler_id
        else:
            loggingUtil().get_error_log("创建经销商失败,返回结果为："+ str(res.json()))
            exit()






    def edit_wholesaler(self,wholesaler_id,wholesaler_format_name,wholesaler_format_phone,wholesaler_type):
        """
        经销商编辑
        @param wholesaler_id: 经销商id
        @param wholesaler_wsAccountId: 经销商账号id
        @param wholesaler_format_name: 经销商名称
        @param wholesaler_format_phone: 经销商手机
        @return:
        """
        params = ""
        header = ""
        url = read_environment_yaml("business_entity_service") + "wholesaler"
        if wholesaler_type == 1:
            params = self.edit_t1_params(wholesaler_id, wholesaler_format_name, wholesaler_format_phone)
            header = self.header
        elif wholesaler_type == 2:
            params = self.edit_t2_params(wholesaler_id, wholesaler_format_name, wholesaler_format_phone)
            header = self.header_t1
        else:
            loggingUtil().get_info_log("经销商类型传参错误，类型为："+ str(wholesaler_type))
            exit()

        res = requests.put(url,json=params,headers=header)
        if res.status_code == 200:
            loggingUtil().get_info_log("经销商编辑成功，返回结果："+ str(res.json()))
        else:
            loggingUtil().get_error_log("查询经销商失败,查询结果为："+ str(res.json()))
            exit()


    def update_wholesaler_status(self,wholesaler_id,status_code):
        """
        修改经销商状态
        @param wholesaler_id: 经销商id
        @param status_code: 1待完善，2停用，3启用
        @return:
        """
        url = read_environment_yaml("business_entity_service") + "wholesaler/updateStatus"
        params = {"status": status_code, "wholesalerId": wholesaler_id}
        res = requests.put(url, json=params, headers=self.header)
        status = jsonpath.jsonpath(res.json(), "$..status")[0]
        if status == "SUCCESS":
            pass
        else:
            loggingUtil().get_info_log("更新状态错误,返回结果为："+ str(res.json()))
            exit()

    def freeze_wholesaler_status(self,wholesaler_id,type):
        """
        经销商冻结解冻状态
        @param wholesaler_id:经销商id
        @param type: 1：冻结，0：解冻
        @return:
        """
        url = ""
        if type == 1:
            url = read_environment_yaml("business_entity_service") + "wholesaler/forbid"
        elif type ==0:
            url = read_environment_yaml("business_entity_service") + "wholesaler/forbid-cancel"
        else:
            loggingUtil().get_info_log("经销商freeze状态类型错误,类型为：" + str(type))
            exit()
        params = {"wholesalerId": wholesaler_id}
        res = requests.put(url,json=params,headers=self.header_t1)
        status = jsonpath.jsonpath(res.json(), "$..status")[0]
        if status == "SUCCESS":
            pass
        else:
            loggingUtil().get_info_log("更新状态错误,返回结果为："+ str(res.json()))
            exit()

    def select_wholesaler_data(self,wholesalerId,key):
        """
        查询经销商
        @param wholesalerId: 经销商
        @return: 查询结果
        """

        url = read_environment_yaml("business_entity_service") + "wholesaler"
        params = {"wholesalerId":wholesalerId}
        res = requests.get(url,params=params,headers=self.header)
        try:
            select_data = jsonpath.jsonpath(res.json(),f"${key}")[0]
            if res.status_code == 200:
                return select_data
            else:
                loggingUtil().get_error_log("查询经销商失败,查询结果为："+ str(res.json()))
                exit()
        except Exception as e:
            loggingUtil().get_error_log("查询经销商失败")
            raise e


    def delete_wholesaler(self,wholesalerId):
        """
        删除经销商
        @param wholesalerId:
        @return:
        """
        url = read_environment_yaml("business_entity_service") + "wholesaler"
        params = {"wholesalerId": wholesalerId}
        res = requests.delete(url, params=params, headers=self.header)
        status = jsonpath.jsonpath(res.json(), "$.status")[0]
        if status == "SUCCESS":
            loggingUtil().get_info_log("接口删除成功")
        else:
            loggingUtil().get_error_log("接口删除失败,返回结果为："+ str(res.json()))
            exit()




    def edit_t1_params(self,wholesaler_id,wholesaler_format_name,wholesaler_format_phone):
        num = random.randint(1,999)
        name = "自动化T1编辑" + str(num)
        edit_name = {"edit_name":name}
        write_extract_yaml(edit_name)
        params = {
        "id": wholesaler_id,
        "discountRate": 55,
        "wholesalerName": name,
        "wholesalerCode": wholesaler_format_name,
        "wholesalerType": 1,
        "wsWechatBizCode": wholesaler_format_name,
        "wsWechatMainName": wholesaler_format_name,
        "wsAccountName": wholesaler_format_name,
        "wsTelphoneNum": wholesaler_format_phone,
        "wholesalerRtms": [{
            "rtmPattern": 1
        }],
        "contactsName": wholesaler_format_name,
        "contactsTelphoneNum": wholesaler_format_phone,
        "orgCustomCodes": [
            ["0000104650", "0000106366", "0000106368"]
        ],
        "freezed": 0
    }
        return params

    def edit_t2_params(self,wholesaler_id,wholesaler_format_name,wholesaler_format_phone):
        num = random.randint(1,999)
        name = "自动化T2编辑" + str(num)
        edit_name = {"edit_name": name}
        write_extract_yaml(edit_name)
        params = {
        "id": wholesaler_id,
        "discountRate": 55,
        "wholesalerName": name,
        "wholesalerCode": wholesaler_format_name,
        "wholesalerType": 1,
        "wsWechatBizCode": wholesaler_format_name,
        "wsWechatMainName": wholesaler_format_name,
        "wsAccountName": wholesaler_format_name,
        "wsTelphoneNum": wholesaler_format_phone,
        "wholesalerSalesmanCode": "w0001673",
        "wholesalerRtms": [{
            "rtmPattern": 1
        }],
        "contactsName": wholesaler_format_name,
        "contactsTelphoneNum": wholesaler_format_phone,
        "orgCustomCodes": [
            ["0000104650", "0000106366", "0000106368"]
        ],
        "freezed": 0
    }
        return params


    def t2_params(self,name_data,phone_data):
        """
        经销商2t参数
        @param name_data: 经销商初始参数
        @param phone_data: 经销商初始电话
        @return: 参数
        """
        params = {
        "discountRate": 50,
        "wholesalerName": name_data,
        "wholesalerType": 2,
        "wsWechatBizCode": name_data,
        "wsWechatMainName": name_data,
        "wsAccountName": name_data,
        "wsTelphoneNum": phone_data,
        "wholesalerRtms": [{
            "rtmPattern": 1
        }],
        "contactsName": name_data,
        "contactsTelphoneNum": phone_data,
        "erpType": 4,
        "erpName": "",
        "parentId": self.parent_id,
        "wholesalerSalesmanCode": self.salsesman_code,
        "mallEnabled": 1,
        "creditValidate": "",
        "adjustBillingEnabled": 0,
        "minBuyNum": 1,
        "includeDeduction": 0,
        "minDeliveryNum": 1,
        "handleMethod": 1,
        "selectWarehouse": True,
        "officeAddress": {
            "provinceCode": "310000",
            "cityCode": "310100",
            "districtCode": "310101",
            "province": "上海市",
            "city": "上海城区",
            "district": "黄浦区",
            "detailAddress": "华旭大厦11F"
        },
        "warehouseAddresses": [{
            "addressName": "仓库01",
            "provinceCode": "310000",
            "cityCode": "310100",
            "districtCode": "310101",
            "province": "上海市",
            "city": "上海城区",
            "district": "黄浦区",
            "detailAddress": "华旭大厦01"
        }, {
            "addressName": "仓库02",
            "provinceCode": "310000",
            "cityCode": "310100",
            "districtCode": "310101",
            "province": "上海市",
            "city": "上海城区",
            "district": "黄浦区",
            "detailAddress": "华旭大厦02"
        }]
    }
        return params

    def t1_params(self0,name_data,phone_data):
        """
        经销商t1参数
        @param name_data: 经销商初始参数
        @param phone_data: 经销商初始电话
        @return: 参数
        """

        params = {
        "discountRate": 55,
        "wholesalerName": name_data,
        "wholesalerCode": name_data,
        "wholesalerType": 1,
        "wsWechatBizCode": name_data,
        "wsWechatMainName": name_data,
        "wsAccountName": name_data,
        "wsTelphoneNum": phone_data,
        "wholesalerRtms": [{
            "rtmPattern": 1
        }],
        "contactsName": name_data,
        "contactsTelphoneNum": phone_data,
        "erpType": 1,
        "erpName": "",
        "abiSalesmanCode": "",
        "wholesalerSalesmanCode": "",
        "mallEnabled": 0,
        "creditValidate": "",
        "adjustBillingEnabled": 0,
        "minBuyNum": 1,
        "includeDeduction": 0,
        "minDeliveryNum": 1,
        "handleMethod": 1,
        "selectWarehouse": True,
        "orgCustomCodes": [["0000104650", "0000106366", "0000106368"]],
        "warehouseAddresses": [{
            "addressName": "仓库01",
            "provinceCode": "110000",
            "cityCode": "110100",
            "districtCode": "110101",
            "province": "北京市",
            "city": "北京城区",
            "district": "东城区",
            "detailAddress": "华旭大厦01"
        }, {
            "addressName": "仓库02",
            "provinceCode": "310000",
            "cityCode": "310100",
            "districtCode": "310101",
            "province": "上海市",
            "city": "上海城区",
            "district": "黄浦区",
            "detailAddress": "华旭大厦02"
        }]
    }
        return params










