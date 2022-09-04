from operator import methodcaller
from commons import case_api
from .pandas_util import PandasUtil
from commons.requests_util import RequestsUtilExcel


class CaseEngine(object):
    def __init__(self):
        self.db_config = "MYSQL_MP"
        self.db = "budtauto"

    def run_case(self, case_id):
        steps = []
        case_info = self.case_info(case_id)
        if case_id:
            steps = self.case_steps(case_id)
        for step in steps:
            if step:
                self.run_step(step, case_info)

    def run_step(self, step, case_info):
        if step["request_id"]:
            api = self.step_api(step)
            case = case_api.CaseApi()
            if step['step_type'] == 'python':
                result = methodcaller(api["method"], step['request_params'])(case)
            else:
                print("\ncase_info\t==>\n", case_info, "\nstep\t==>\n", step, "\napi\t==>\n", api)
                result = RequestsUtilExcel().request_from_db(step["step_name"], case_info, step, api)
        return result

    @staticmethod
    def case_steps(case_id):
        return PandasUtil().get_steps_by_case_id(case_id)

    @staticmethod
    def case_ids(service_name):
        return PandasUtil().get_case_ids_by_service(service_name)

    @staticmethod
    def step_api(step):
        return PandasUtil().get_api_by_step(step)

    @staticmethod
    def case_info(case_id):
        return PandasUtil().get_case_info_by_id(case_id)
