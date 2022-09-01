import os
import time

import pytest

from commons.config_util import ConfigUtil
from commons.preposition_util import PrepositionUtil
from commons.postposition_util import PostpositionUtil



# 基础前置数据
@pytest.fixture(scope="session", autouse=True)
def base_config():
    ConfigUtil().get_environment_config()













