import json

import allure
import pytest

from commons.ddt_util import ddt_data, read_excel_ddt
from commons.excel_util import read_excel, get_all_caseinfo, get_sheet_row, read_data_excel
from commons.requests_util import RequestsUtilExcel


@allure.epic("BEES-business-entity-service")
class TestSaleDealer:
    pass

    # 读取1个sheet页（服务）case=>business_entity_service服务
    # @pytest.mark.parametrize("caseinfo",read_excel("business_entity_service","./caseInfo/bees.xlsx"))
    # def test_bees_business_entity_service(self,caseinfo):
    #     RequestsUtilExcel().standard_excel(caseinfo)



    #读取1个sheet页（服务）case=>bees_product服务
    # @pytest.mark.parametrize("caseinfo",read_excel("bees_product","./caseInfo/bees.xlsx"))
    # def test_bees_product(self,caseinfo):
    #     RequestsUtilExcel().standard_excel(caseinfo)



    #读取所有sheet页（服务）case
    # @pytest.mark.parametrize("caseinfo", get_all_caseinfo())
    # def test_all_case(self,caseinfo):
    #     RequestsUtilExcel().standard_excel(caseinfo)



    # 读取指定表格中的指定行（服务）case
    # def test_one_case(self):
    #     caseinfo = get_sheet_row(53, "business_entity_service", "./caseInfo/bees.xlsx")
    #     RequestsUtilExcel().standard_excel(caseinfo)



    # @pytest.mark.parametrize("caseinfo", read_excel_ddt("bees_ddt", "./caseInfo/bees.xlsx"))
    # def test_bees_business_entity_service(self,caseinfo):
    #     # new_caseinfo = ddt_data(caseinfo)
    #     # for case in new_caseinfo:
    #     RequestsUtilExcel().standard_excel(caseinfo)




    # @pytest.mark.parametrize("caseinfo", read_excel_ddt("bees_ddt", "./caseInfo/bees_1.xlsx"))
    # def test_bees_business_entity_service_1(self, caseinfo):
    #     # new_caseinfo = ddt_data(caseinfo)
    #     # for case in new_caseinfo:
    #     RequestsUtilExcel().standard_excel(caseinfo)





        


