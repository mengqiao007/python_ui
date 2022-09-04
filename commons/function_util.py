import json
import random
import base64
import jsonpath
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from commons.yaml_util import read_environment_yaml, write_extract_yaml
from commons.logging_util import loggingUtil
from commons.yaml_util import get_object_path
from commons.yaml_util import read_extract_yaml
from faker import Faker
import time
from commons.postposition_util import PostpositionUtil


# 功能方法类
class FunctionUtil:


    # 获取随机数
    def get_random_number(self, min, max):
        try:
            rm = random.randint(int(min), int(max))
            return str(rm)
        except Exception as e:
            print(e, "获取随机数get_random_number异常")
            raise e

    # 获取当前时间字符串
    def get_localtime_str(self):
        str_time = time.strftime("%Y-%m-%d %H:%M:%S")
        return str_time

    # 指定时间戳转为日期格式
    def assgin_str_format_date(self,time_str):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_str/1000))


    # 读取extract.yaml文件中的值
    def read_extract_data(self, key):
        return read_extract_yaml(key)

    # 读取environment.yaml文件中的值
    def read_environment_data(self, key):
        return read_environment_yaml(key)

    # 转换全局变量的数据类型int
    def read_extract_data_int(self, key):
        try:
            num = self.read_extract_data(key)
            num_int = int(num)
            return num_int
        except Exception as e:
            loggingUtil().get_error_log(str(e) + "转换全局变量的数据类型read_extract_data_int异常")
            raise e

    # 转换全局变量的数据类型str
    def read_extract_data_str(self, key):
        str_data = self.read_extract_data(key)
        return str(str_data)

    # 使用RSA加密
    def rsa_encrpt(self, password):
        # 获取公钥
        with open(get_object_path() + '/commons/public.pem', mode='rb') as publickfile:
            p = publickfile.read()
        rsakey = RSA.importKey(p)
        cipher = Cipher_pksc1_v1_5.new(rsakey)
        password = str(password)  # 密码为int类型时需要转化为str类型
        cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
        return cipher_text.decode()


    def jsonpath_field(self,data,field):
        """
        jsonpath 提取字段
        @param data: 提取数据
        @param field: 提取字段
        @return: 提取字段值
        """
        if data != False:
            res = jsonpath.jsonpath(data, f"${field}")
            if res != False:
                if len(res) == 1:
                    return res[0]
                elif len(res) > 1:
                    return res
            else:
                loggingUtil().get_error_log(
                    "jsonpath提取错误" + "\n" + "提取字段：" + str(field) + "\n" + "提取数据：" + str(data))
        else:
            loggingUtil().get_error_log("jsonpath提取数据data为空" + str(data))



    def get_add_wholesaler_org(self):
        add_wholesaler_org = self.read_extract_data("add_wholesaler_org")
        json_data = json.dumps(add_wholesaler_org[0])
        return json_data


    def get_name(self):
        fake = Faker(locale='zh_CN')
        return fake.name()

    def get_address(self):
        fake = Faker(locale='zh_CN')
        return fake.address()[:-7]

    def get_phone(self):
        fake = Faker(locale='zh_CN')
        return fake.phone_number()

    def get_t2_wholesaler_id(self,name="T1importT2_name"):
        id,parent_id =  PostpositionUtil().get_wholesaler_id_and_parent_id(read_extract_yaml(name))
        id = int(id)
        PostpositionUtil().update_status(id,3)

        id_data = {"T1importT2_id":id}
        parent_id_data = {"T1importT2_parent_id":parent_id}

        write_extract_yaml(id_data)
        write_extract_yaml(parent_id_data)
        return id

    def random_code(self,num=6):
        code = ""
        for i in range(num):
            num = random.randint(0, 9)
            letter = chr(random.randint(97, 122))
            Letter = chr(random.randint(65, 90))
            s = str(random.choice([num, letter, Letter]))
            code += s
        return code


    def get_group_info(self):
        info = read_extract_yaml("group_poc_info")
        return info[0]["pocId"]


    def get_group_info_1(self):
        info = read_extract_yaml("group_poc_info")
        return info[1]["pocId"]

    def auto_name(self):
        name = "自动化" + self.random_code()
        name_data = {"auto_name":name}
        write_extract_yaml(name_data)
        return name






if __name__ == '__main__':
    pass
