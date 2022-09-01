import json

import allure
import pytest

from commons.ddt_util import ddt_data, read_excel_ddt
from commons.excel_util import read_excel, get_all_caseinfo, get_sheet_row, read_data_excel
from commons.requests_util import RequestsUtilExcel

#中台用户服务
@allure.epic("MP-Service")
class TestSaleDealer:

    #中台用户组织架构遍历用例
    @pytest.mark.parametrize("caseinfo", read_excel_ddt("base_data", "./caseInfo/mp_org_case.xlsx"))
    def test_mp_user_org(self, caseinfo):
        RequestsUtilExcel().standard_excel(caseinfo)








