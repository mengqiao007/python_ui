from commons.pandas_util import PandasUtil
from enum import Enum
import random


# class TddEnum(Enum):
#     """
#     tdd枚举类
#     """
#     sales_organization = ("mp_sales_organization")
#
#
# def tdd_organization():
#     table = TddEnum.sales_organization.value
#     sql_list = PandasUtil().table_to_list(table)
#     name_dict = {}
#     for i in sql_list:
#         name_dict[str(i["code"])] = i["name"]
#     org_count = len(sql_list)
#     tail_num_list = random.sample(range(10000, 99999), org_count)
#     params_list = []
#     for i in range(org_count):
#         org = sql_list[i]
#         if org["code"] != "0000100000" and i <= 2:
#             full_code = org["code"]+","+org["parent_code_array"]
#             org_list = full_code.split(",")[:org["level"]]
#             org_list.reverse()
#             org_name = ""
#             for org in org_list:
#                 if org_name:
#                     org_name += ("=>" + name_dict[org])
#                 else:
#                     org_name = name_dict[org]
#             t_phone = 19999900000 + tail_num_list[i]
#             t_str = "TESTDATA" + str(tail_num_list[i])
#             params = org_name, t_str, t_str, t_str, t_str, t_str, t_phone, t_str, t_phone, [org_list]
#             params_list.append(params)
#             print(params)
#     return params_list
