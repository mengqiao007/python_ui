import os
import random
import time

import openpyxl
import requests
import jsonpath
from commons.yaml_util import write_extract_yaml, read_extract_yaml, read_environment_yaml


# 后置方法类
class PostpositionUtil():




    def bees_postposition_data(self):

        self.select_update_delete_wholesaler("ABIimportT2_name")
        self.select_update_delete_wholesaler("T1importT2_name")



    def select_update_delete_wholesaler(self,name):
        """
        删除经销商流程
        @param name: 字段名
        @return:
        """
        name_data = read_extract_yaml(name)
        id = int(self.get_wholesaler_id(name_data))
        self.update_status(id)
        self.delete_wholesaler(id)


    def get_wholesaler_id(self,  name):
        """
        查询经销商
        @param name:
        @return:
        """

        base_url = read_environment_yaml("business_entity_service")
        header_t1 = {"authentoken": read_environment_yaml("bees_console_token_t1"), "type": "1"}


        url = base_url + "wholesaler/paging"
        params = {"wsAccountName":name}
        res = requests.post(url,json=params,headers=header_t1)
        w_id = jsonpath.jsonpath(res.json(),"$..id")
        if len(w_id) == 2:
            return w_id[1]
        else:
            return "获取经销商错误",res.json()


    def get_wholesaler_id_and_parent_id(self,  name):
        """
        查询经销商
        @param name:
        @return:
        """
        base_url = read_environment_yaml("business_entity_service")
        header_t1 = {"authentoken": read_environment_yaml("bees_console_token_t1"), "type": "1"}
        url = base_url + "wholesaler/paging"
        params = {"wsAccountName":name}
        res = requests.post(url,json=params,headers=header_t1)
        w_id = jsonpath.jsonpath(res.json(),"$..id")
        p_id = jsonpath.jsonpath(res.json(),"$..parentId")
        if len(w_id) == 2:
            return w_id[1],p_id[0]
        else:
            return "获取经销商错误",res.json()


    def update_status(self,id,status_code=1):
        """
        修改状态
        @param id:
        @return:
        """
        base_url = read_environment_yaml("business_entity_service")
        header_t1 = {"authentoken": read_environment_yaml("bees_console_token_t1"), "type": "1"}
        url = base_url + "wholesaler/updateStatus"
        params = {"status": status_code, "wholesalerId": id}
        res = requests.put(url,json=params,headers=header_t1)
        status = jsonpath.jsonpath(res.json(),"$..status")[0]
        if status == "SUCCESS":
            return "更新成功"
        else:
            return "更新状态错误,返回结果为：", res.json()

    def delete_wholesaler(self,id):
        """
        删除经销商
        @param id:
        @return:
        """
        base_url = read_environment_yaml("business_entity_service")
        header_t1 = {"authentoken": read_environment_yaml("bees_console_token_t1"), "type": "1"}
        url = base_url + "wholesaler"
        params = {"wholesalerId":id}
        res = requests.delete(url,params=params,headers=header_t1)
        status = jsonpath.jsonpath(res.json(), "$..status")[0]

        if status == "SUCCESS":
            return "删除成功"
        else:
            return "删除错误,返回结果为：", res.json()


    def postposition_allure_data(self):
        time.sleep(2)
        os.system("allure generate ./temps -o ./reports --clean")
        time.sleep(1)
        os.system("allure open reports")




