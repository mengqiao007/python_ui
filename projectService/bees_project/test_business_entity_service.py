import allure
import pytest

# from commons.business_util import org_data_ddt
# from commons.ddt_util import ddt_data, read_excel_ddt
from commons.excel_util import read_excel
from commons.postposition_util import PostpositionUtil
from commons.preposition_util import PrepositionUtil
from commons.requests_util import RequestsUtilExcel


@allure.epic("BEES-business-entity-service")
class TestBeesProject:



    # 资源位模块
    @pytest.mark.bees
    @pytest.mark.business_entity_service
    @pytest.mark.resource
    @pytest.mark.parametrize("caseinfo", read_excel("resource", "./caseInfo/bees_business_entity_service.xlsx"))
    def test_bees_business_entity_service_resource(self, caseinfo):
        RequestsUtilExcel().standard_excel(caseinfo)


    # 店铺模块
    @pytest.mark.bees
    @pytest.mark.business_entity_service
    @pytest.mark.store
    @pytest.mark.parametrize("caseinfo", read_excel("store", "./caseInfo/bees_business_entity_service.xlsx"))
    def test_bees_business_entity_service_store(self, caseinfo, store_fixture):
        RequestsUtilExcel().standard_excel(caseinfo)


    # poc-group模块
    @pytest.mark.bees
    @pytest.mark.business_entity_service
    @pytest.mark.group
    @pytest.mark.parametrize("caseinfo", read_excel("poc_group", "./caseInfo/bees_business_entity_service.xlsx"))
    def test_bees_business_entity_service_group(self, caseinfo, group_fixture):
        RequestsUtilExcel().standard_excel(caseinfo)


    #经销商模块
    @pytest.mark.bees
    @pytest.mark.business_entity_service
    @pytest.mark.wholesaler
    @pytest.mark.parametrize("caseinfo", read_excel("wholesaler", "./caseInfo/bees_business_entity_service.xlsx"))
    def test_bees_business_entity_service_wholesaler(self, caseinfo, wholesaler_fixture):
        RequestsUtilExcel().standard_excel(caseinfo)


    # poc模块  服务暂无法连接
    @pytest.mark.bees
    @pytest.mark.business_entity_service
    @pytest.mark.poc
    @pytest.mark.parametrize("caseinfo", read_excel("poc", "./caseInfo/bees_business_entity_service.xlsx"))
    def test_bees_business_entity_service_poc(self, caseinfo):
        RequestsUtilExcel().standard_excel(caseinfo)


    #总部模块
    @pytest.mark.bees
    @pytest.mark.business_entity_service
    @pytest.mark.headquarter
    @pytest.mark.parametrize("caseinfo", read_excel("headquarter", "./caseInfo/bees_business_entity_service.xlsx"))
    def test_bees_business_entity_service_headquarter(self, caseinfo):
        RequestsUtilExcel().standard_excel(caseinfo)


    #销售模块
    @pytest.mark.bees
    @pytest.mark.business_entity_service
    @pytest.mark.salesman
    @pytest.mark.parametrize("caseinfo", read_excel("salesman", "./caseInfo/bees_business_entity_service.xlsx"))
    def test_bees_business_entity_service_salesman(self, caseinfo):
        RequestsUtilExcel().standard_excel(caseinfo)







    # 读取1个sheet页（服务）case=>business_entity_service服务
    # @pytest.mark.parametrize("caseinfo",read_excel("business_entity_service","./caseInfo/bees_business_entity_service.xlsx")[112:])
    # def test_bees_business_entity_service_wholesaler(self,caseinfo):
    #     RequestsUtilExcel().standard_excel(caseinfo)



    # 读取指定表格中的指定行（服务）case
    # def test_one_case(self):
    #     caseinfo = get_sheet_row(113, "business_entity_service", "./caseInfo/bees_business_entity_service.xlsx")
    #     RequestsUtilExcel().standard_excel(caseinfo)

    # @pytest.mark.parametrize("caseinfo",read_excel("business_entity_service","./caseInfo/bees_hw.xlsx")[92:])
    # def test_bees_business_entity_service_hw(self,caseinfo):
    #     RequestsUtilExcel().standard_excel(caseinfo)
    #
    #
    # @pytest.mark.parametrize("caseinfo",read_excel("business_entity_service","./caseInfo/bees_zcl.xlsx")[92:])
    # def test_bees_business_entity_service_zcl(self,caseinfo):
    #     RequestsUtilExcel().standard_excel(caseinfo)


    #读取1个sheet页（服务）case=>bees_product服务
    # @pytest.mark.parametrize("caseinfo",read_excel("bees_product","./caseInfo/bees_business_entity_service.xlsx"))
    # def test_bees_product(self,caseinfo):
    #     RequestsUtilExcel().standard_excel(caseinfo)



    #读取所有sheet页（服务）case
    # @pytest.mark.parametrize("caseinfo", get_all_caseinfo())
    # def test_all_case(self,caseinfo):
    #     RequestsUtilExcel().standard_excel(caseinfo)







    # @pytest.mark.parametrize("caseinfo", read_excel_ddt("bees_ddt", "./caseInfo/bees_business_entity_service.xlsx"))
    # def test_bees_business_entity_service(self,caseinfo):
    #     # new_caseinfo = ddt_data(caseinfo)
    #     # for case in new_caseinfo:
    #     RequestsUtilExcel().standard_excel(caseinfo)




    # @pytest.mark.parametrize("caseinfo", read_excel_ddt("bees_ddt", "./caseInfo/bees_1.xlsx"))
    # def test_bees_business_entity_service_1(self, caseinfo):
    #     # new_caseinfo = ddt_data(caseinfo)
    #     # for case in new_caseinfo:
    #     RequestsUtilExcel().standard_excel(caseinfo)





@pytest.fixture(scope="class")
def wholesaler_fixture():
    PrepositionUtil().wholesaler_format_data()
    yield
    PostpositionUtil().bees_postposition_data()


@pytest.fixture(scope="class")
def group_fixture():
    PrepositionUtil().poc_group_format_data()


@pytest.fixture(scope="class")
def store_fixture():
    PrepositionUtil().store_batch_delete_id()



