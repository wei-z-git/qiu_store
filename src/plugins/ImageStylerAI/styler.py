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
from nonebot.adapters.qqguild import Message,MessageSegment
from typing import Union
import base64
# from .config import plugin_config
# from .SDUtils import AifadianUtils

get_image = on_command('t', priority=1)


@get_image.got("img_attach", prompt="请发送图片")
async def _(matcher: Matcher, img_attach: Message = Arg()):
    img_url="https://"+img_attach[0].data["url"]
    with httpx.Client() as client:
        response = client.get(img_url)
        if response.status_code != 200:
            print(f"下载失败，错误代码：{response.status_code}")
    # await matcher.send(MessageSegment.file_image(response.content))

    url = 'http://127.0.0.1:7860/tagger/v1/interrogate'
    model = 'wd-v1-4-moat-tagger.v2'
    threshold = 0.35
    image_base64 = base64.b64encode(response.content).decode('utf-8')

    data = {
        "image": image_base64,
        "model": model,
        "threshold": threshold
    }

    # 发送POST请求
    response = httpx.post(url, json=data)

    # 检查响应状态码
    if response.status_code == 200: 
        json_data = response.json()
        # 处理返回的JSON数据
        caption_dict = list(json_data['caption']['tag'].keys())
        print(caption_dict)

    else:
        print('Error:', response.status_code)
        print('Response body:', response.text)
    # if default.result:
    #     if not await SUPERUSER(bot, event):
    #         await set_mask_cmd.finish("仅超级用户可设置词云默认形状")
    #     mask.save(plugin_config.get_mask_path(), format="PNG")
    #     await set_mask_cmd.finish("词云默认形状设置成功")
    # else:
    #     mask.save(plugin_config.get_mask_path(mask_key), format="PNG")
    #     await set_mask_cmd.finish("词云形状设置成功")

# <class 'nonebot.adapters.qqguild.message.Message'>