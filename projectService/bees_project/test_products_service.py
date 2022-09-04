import allure
import pytest

# from commons.business_util import org_data_ddt
# from commons.ddt_util import ddt_data, read_excel_ddt
from commons.excel_util import read_excel
from commons.postposition_util import PostpositionUtil
from commons.preposition_util import PrepositionUtil
from commons.requests_util import RequestsUtilExcel


@allure.epic("BEES-products-service")
class TestBeesProject:

    @pytest.mark.bees
    @pytest.mark.products_service
    @pytest.mark.brand
    @pytest.mark.parametrize("caseinfo", read_excel("brand", "./caseInfo/bees_products_service.xlsx"))
    def test_bees_business_entity_service_brand(self, caseinfo,product_fixture):
        RequestsUtilExcel().standard_excel(caseinfo)



    @pytest.mark.bees
    @pytest.mark.products_service
    @pytest.mark.category
    @pytest.mark.parametrize("caseinfo", read_excel("category", "./caseInfo/bees_products_service.xlsx"))
    def test_bees_business_entity_service_category(self, caseinfo,product_fixture):
        RequestsUtilExcel().standard_excel(caseinfo)





@pytest.fixture(scope="class")
def product_fixture():
    PrepositionUtil().product_preposition()










