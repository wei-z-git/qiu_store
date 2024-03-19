from nonebot import on_command
# from nonebot.adapters import Bot, Message
from nonebot.matcher import Matcher
from nonebot.adapters.qqguild.event import AtMessageCreateEvent, MessageCreateEvent, DirectMessageCreateEvent
from nonebot.adapters.qqguild.exception import AuditException
from nonebot.typing import T_State
from nonebot.params import Depends, Arg, ArgPlainText
from nonebot.rule import to_me
from nonebot.log import logger
from PIL import Image
from io import BytesIO
import httpx
import json
from nonebot.adapters.qqguild import Message
from typing import Union

# from .config import plugin_config
# from .SDUtils import AifadianUtils

get_image = on_command('t', priority=1)


@get_image.got("img_attach", prompt="请发送图片")
async def _(state: T_State, matcher: Matcher, img_attach: Message = Arg()):
    img_attach: Message = Arg()
    img_attach[0].data["url"]
    data = json.loads(img_attach)
    # img_url=img_attach.0.["data"]["url"]
    with httpx.Client() as client:
        response = client.get(img_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print("图片下载成功！")
        else:
            print(f"下载失败，错误代码：{response.status_code}")
    mask = Image.open(BytesIO(img))
    # if default.result:
    #     if not await SUPERUSER(bot, event):
    #         await set_mask_cmd.finish("仅超级用户可设置词云默认形状")
    #     mask.save(plugin_config.get_mask_path(), format="PNG")
    #     await set_mask_cmd.finish("词云默认形状设置成功")
    # else:
    #     mask.save(plugin_config.get_mask_path(mask_key), format="PNG")
    #     await set_mask_cmd.finish("词云形状设置成功")

# <class 'nonebot.adapters.qqguild.message.Message'>