import os

import yaml

#读取yaml文件类
def read_testcase_yaml(yaml_path):
    with open(get_object_path() + yaml_path, encoding='utf-8') as f:
        value = yaml.load(f, Loader=yaml.FullLoader)
        return value


# 获取项目根目录
def get_object_path():
    current = os.path.abspath(__file__)
    path = os.path.dirname(os.path.dirname(current))
    return path

    # return os.getcwd()


# 读取关联的yaml文件
def read_extract_yaml(key):
    with open(get_object_path() + "/config/extract.yaml", encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)[key]

# 读取环境配置yaml文件
def read_environment_yaml(key):
    with open(get_object_path() + "/config/environment.yaml", encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)[key]


# 写入yaml文件（可以写入变量  在其他文件中使用）
def write_extract_yaml(data):
    with open(get_object_path() + "/config/extract.yaml", encoding='utf-8', mode='a') as f:
        yaml.dump(data=data, stream=f, allow_unicode=True)


# 写入环境配置yaml文件
def write_environment_yaml(data):
    with open(get_object_path() + "/config/environment.yaml", encoding='utf-8', mode='a') as f:
        yaml.dump(data=data, stream=f, allow_unicode=True)


# 清空yaml文件
def clear_extract_yaml():
    with open(get_object_path() + "/config/extract.yaml", encoding='utf-8', mode='w') as f:
        f.truncate()

# 清空yaml文件
def clear_environment_yaml():
    with open(get_object_path() + "/config/environment.yaml", encoding='utf-8', mode='w') as f:
        f.truncate()

# 读取配置文件
def read_config_yaml(key):
    with open(get_object_path() + "/config/config.yaml", encoding='utf-8') as f:
        value = yaml.load(f, Loader=yaml.FullLoader)
        return value[key]


