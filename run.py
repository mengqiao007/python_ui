import os
import time
import pytest

from commons.function_util import FunctionUtil

if __name__ == '__main__':
    pytest.main(['-vs','-W','ignore:Module already imported:pytest.PytestWarning'])
    time.sleep(1)
    os.system("allure generate ./temps -o ./reports --clean")
    # os.system("allure open reports")

