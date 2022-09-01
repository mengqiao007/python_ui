import json

import allure
import pytest

# from commons.business_util import org_data_ddt
from commons.excel_util import read_excel, get_all_caseinfo, get_sheet_row, read_data_excel
from commons.requests_util import RequestsUtilExcel
from .tdd_beesService import tdd_organization

#
# @pytest.mark.parametrize("params", tdd_organization())
# @allure.epic("BEES-Org-Tracersal")
# class TestOrg:
#     def test_demo_wholesaler(self, params):
#         org_data_ddt().wholesaler_business(params)