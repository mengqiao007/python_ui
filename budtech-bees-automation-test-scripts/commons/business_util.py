import jsonpath
import requests

import commons.function_util as function_util
import commons.requests_util as requests_util
from commons.yaml_util import read_config_yaml, read_extract_yaml


# class org_data_ddt():
#     # 创建经销商
#     url = "https://bees-server-dev.ab-inbev.cn/business-entity-service/wholesaler"
#     header = {'authentoken': read_extract_yaml("bees_console_token_abi"), 'type': '1'}
#
#     def create_wholesaler(self, params):
#
#         params = {
#             "discountRate": 50,
#             "wholesalerName": params[0],
#             "wholesalerCode": params[1],
#             "wholesalerType": 1,
#             "wsWechatBizCode": params[2],
#             "wsWechatMainName": params[3],
#             "wsAccountName": params[4],
#             "wsTelphoneNum": params[5],
#             "wholesalerRtms": [{
#                 "rtmPattern": 1
#             }],
#             "contactsName": params[6],
#             "contactsTelphoneNum": params[7],
#             "erpType": 1,
#             "erpName": "",
#             "abiSalesmanCode": "",
#             "wholesalerSalesmanCode": "",
#             "mallEnabled": 0,
#             "creditValidate": "",
#             "adjustBillingEnabled": 0,
#             "minBuyNum": 1,
#             "includeDeduction": 0,
#             "minDeliveryNum": None,
#             "orgCustomCodes":
#                 params[8]
#             ,
#             "warehouseAddresses": []
#         }
#
#         res = requests.post(url=self.url, json=params, headers=self.header)
#         self.create_method = "POST"
#         self.create_response_time = res.elapsed.total_seconds()
#         self.create_param = params
#         self.create_code = res.json()["code"]
#         self.create_result = res.json()
#
#         wholesaler_id = jsonpath.jsonpath(res.json(), f"$..data")
#
#         if wholesaler_id:
#             return wholesaler_id[0]
#         else:
#             return "未在响应中找到data数据"
#
#     # 通过经销商id查询组织架构
#     def by_wholesalerId_select_org(self, wholesaler_id):
#
#         params = {"wholesalerId": wholesaler_id}
#
#         res = requests.get(url=self.url, params=params, headers=self.header)
#
#         self.select_method = "GET"
#         self.select_response_time = res.elapsed.total_seconds()
#         self.select_param = params
#         self.select_code = res.json()["code"]
#         self.select_result = res.json()
#         orgCustomCodes = jsonpath.jsonpath(res.json(), f"$..orgCustomCodes")
#
#         if orgCustomCodes:
#             return orgCustomCodes[0]
#         else:
#             return "未在响应中找到响应数据"
#
#     # 经销商遍历组织架构业务流程
#     def wholesaler_business(self, params):
#         medule, version = ["经销商管理", "遍历组织架构"]
#         requests_util.RequestsUtilExcel().allure_title(params[0], medule, version)
#
#         wholesaler_id = self.create_wholesaler(params[1:])
#
#         assert_text, assert_test_result = "SUCCESS", self.create_result["status"]
#         requests_util.RequestsUtilExcel().    allure_step(self.create_code, self.create_response_time, self.create_method, self.url, self.create_param, self.create_result,assert_text,assert_test_result)
#
#         select_orglist = self.by_wholesalerId_select_org(wholesaler_id)
#         requests_util.RequestsUtilExcel().allure_step(self.select_code, self.select_response_time, self.select_method, self.url, self.select_param, self.select_result,params[-1], select_orglist)
#
#         assert select_orglist == params[-1] and assert_text == assert_test_result, "查询组织架构的结果与创建组织架构的结果不一致"
#
#     def edit_wholesaler(self, wholesaler_id):
#         params = {
#             "id": wholesaler_id,
#             "wsAccountId": "1542088473603022850",
#             "discountRate": 50,
#             "wholesalerName": "ThisIsTest",
#             "wholesalerCode": "ThisIsTest",
#             "wholesalerType": 1,
#             "wsWechatBizCode": "updata",
#             "wsWechatMainName": "ThisIsTest",
#             "wsAccountName": "ThisIsTest",
#             "wsTelphoneNum": "13312345678",
#             "wholesalerRtms": [{
#                 "id": "1556",
#                 "deleted": 0,
#                 "createdAt": "2022-06-29 18:11:57",
#                 "createdBy": "1384416613905731585",
#                 "updatedAt": "2022-06-29 18:11:57",
#                 "updatedBy": "1384416613905731585",
#                 "wholesalerId": wholesaler_id,
#                 "rtmPattern": 1,
#                 "supplierId": None,
#                 "payToId": None,
#                 "logisticsModel": 1
#             }],
#             "contactsName": "吴",
#             "contactsTelphoneNum": "13312345678",
#             "erpType": 4,
#             "erpName": "",
#             "parentId": None,
#             "abiSalesmanCode": "",
#             "wholesalerSalesmanCode": "",
#             "mallEnabled": 0,
#             "erpId": None,
#             "creditValidate": "",
#             "adjustBillingEnabled": 0,
#             "minBuyNum": 1,
#             "includeDeduction": 0,
#             "minDeliveryNum": 1,
#             "allocationMethod": 2,
#             "commodityAttributeSplitOrder": 1,
#             "selectWarehouse": False,
#             "orgCustomCodes": [
#                 ["0000104650", "0000105138", "0000105381"]
#             ],
#             "status": 2,
#             "store": {
#                 "id": "788",
#                 "deleted": 0,
#                 "createdAt": "2022-06-29 18:11:57",
#                 "createdBy": "1384416613905731585",
#                 "updatedAt": "2022-06-29 18:11:57",
#                 "updatedBy": "1384416613905731585",
#                 "storeCode": "1334065882783073956",
#                 "wholesalerId": "1334065882783073956",
#                 "storeName": "ThisIsTest",
#                 "storeDetails": None,
#                 "storeLogoUrl": None
#             },
#             "wholesalerNameSecond": None,
#             "deliveryInfoList": [],
#             "officeAddress": None,
#             "warehouseAddresses": [],
#             "freezed": 0,
#             "creditPeriod": None,
#             "creditPeriodInfo": None,
#             "rebates": False,
#             "wholesalerPayCode": "0030002790",
#             "wholesalerNameFromMiddle": "上海道尔贸易有限公司"
#         }
#
