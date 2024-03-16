# from typing import Optional
from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    sd_api_url: str = 'xxxxxx'  # sd 地址


driver = get_driver()
global_config = driver.config
plugin_config = Config.parse_obj(global_config)
