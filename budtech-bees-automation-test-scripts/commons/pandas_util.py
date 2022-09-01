import pandas as pd
from commons.mysql_util import mysql_connect


class PandasUtil(object):
    def __init__(self):
        self.tc_engine = mysql_connect("MYSQL_XY", "budauto")
        self.bees_engine = mysql_connect("MYSQL_MP", "abi-cloud-middle-platform-user-test")
        pass

    @staticmethod
    def pd_to_list(panda_data):
        sql_dict = panda_data.to_dict('list')
        sql_list = []
        keys = sql_dict.keys()
        for i in range(0, len(sql_dict['id'])):
            row = {}
            for key in keys:
                row[key] = sql_dict[key][i]
            sql_list.append(row)
        return sql_list

    def table_to_list(self, table):
        """
        convert db table to list with dict item
        :param table: db table name
        :return: [{"column1": "value1", "column2": "value2", "column3": "value3", ...}, {}, {},...]
        """
        res = pd.read_sql_query("select * from {table}".format(table=table), self.bees_engine)
        sql_list = self.pd_to_list(res)
        return sql_list

    def get_steps_by_case_id(self, case_id):
        res = pd.read_sql_query(
            "select * from tc_step where tc_id = {case_id}".format(case_id=case_id),
            self.tc_engine)
        steps = self.pd_to_list(res)
        return steps

    def get_case_ids_by_module(self, module):
        print(self.tc_engine, module)
        case_ids = []
        return case_ids

    def get_case_ids_by_service(self, service):
        print(self.tc_engine, service)
        service_ids_str = 'select id from service where service_name = "{service}"'.format(service=service)
        service_ids = pd.read_sql_query(service_ids_str, self.tc_engine)

        service_id = service_ids.to_dict('list')['id'][0]
        case_ids_str = 'select id from test_case where service_id = service_id and status = 1'.format(service_id=service_id)
        res = pd.read_sql_query(case_ids_str, self.tc_engine)
        case_ids = res.to_dict('list')
        print("service_id\t:", service_id, "\ncase_ids\t:", case_ids)
        return case_ids['id']

    def get_api_by_step(self, step):
        if step['step_type'] and step['request_id']:
            if step['step_type'] == 'http':
                res = pd.read_sql_query(
                    "select * from tc_api where id = {id}".format(id=step['request_id']),
                    self.tc_engine
                )
            else:
                res = pd.read_sql_query(
                    "select * from tc_method where id = {id}".format(id=step['request_id']),
                    self.tc_engine
                )
            return self.pd_to_list(res)[0]

    def get_case_info_by_id(self, case_id):
        info_str = "select * from test_case where id = {case_id}".format(case_id=case_id)
        res = pd.read_sql_query(info_str, self.tc_engine)
        return self.pd_to_list(res)[0]



