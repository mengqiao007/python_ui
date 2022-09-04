import os
import time

import allure
import pytest

# from commons.business_util import org_data_ddt
# from commons.ddt_util import ddt_data, read_excel_ddt
from businessInfo.wholesaler_business import Wholesaler_Business
from commons.excel_util import read_excel, get_all_caseinfo, get_sheet_row, read_data_excel
from commons.postposition_util import PostpositionUtil
from commons.preposition_util import PrepositionUtil
from commons.requests_util import RequestsUtilExcel





# @allure.epic("BEES-Business-process")
# class TestBeesBusiness:
#
#     @pytest.mark.business_process
#     @pytest.mark.business_wholesaler_t2
#     def test_bees_business_process_wholesaler_t2(self):
#         Wholesaler_Business().wholesaler_business(2)
#
#
#     @pytest.mark.business_process
#     @pytest.mark.business_wholesaler_t1
#     def test_bees_business_process_wholesaler_t1(self):
#         Wholesaler_Business().wholesaler_business(1)
#
#
#
#
#
#
# # @pytest.fixture(scope="class")
# # def whoelsaler_business_fixture():
# #     yield
# #     os.system("allure generate ./temps -o ./reports --clean")
# #     os.system("allure open reports")
