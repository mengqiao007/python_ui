import json

import jsonpath
import requests
import commons.function_util as function_util

from commons.excel_util import read_data_excel, read_excel

#读取excel数据驱动case
def read_excel_ddt(Sheet1, path):
    """
    读取excel数据驱动case
    :param Sheet1: sheet页名称
    :param path: 路径
    :return: caseinfo
    """
    caseinfo = read_excel(Sheet1, path)

    for case in caseinfo:
        if case["数据驱动"]:
            new_caseinfo = ddt_data(case)
            return new_caseinfo
        else:
            return case
    return caseinfo

#遍历数据驱动data
def ddt_data(caseinfo):
    caseinfo_str = json.dumps(caseinfo)
    ddt = caseinfo["数据驱动"]
    ddt = eval(ddt)

    for param_key, param_value in ddt.items():
        key_list = param_key.split("~")
        length_flag = True
        data_list = read_data_excel(param_value)
        for data in data_list:
            if len(data) - 1 != len(key_list):
                length_flag = False
                break

        new_caseinfo = []
        if length_flag:
            for x in range(1, len(data_list)):
                temp_caseinfo = caseinfo_str
                for y in range(1, len(data_list[x])):
                    if data_list[0][y] in key_list:
                        temp_caseinfo = temp_caseinfo.replace("$ddt{" + data_list[0][y] + "}", str(data_list[x][y]))
                new_caseinfo.append(json.loads(temp_caseinfo))
        return new_caseinfo
    return caseinfo



if __name__ == '__main__':
    pass





