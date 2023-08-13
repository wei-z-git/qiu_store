# from typing import Optional
from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    aifadian_user_id: str = 'xxxxxx'  # 爱发电user_id
    aifadian_token: str = 'xxxxxx'  # 爱发电token
    goods_secrets_url:str='xxxxx' #plan_id和商品对照表url


driver = get_driver()
global_config = driver.config
plugin_config = Config.parse_obj(global_config)
