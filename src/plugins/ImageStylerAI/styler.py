from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.params import Depends, Arg, ArgPlainText
from nonebot.rule import to_me
from nonebot.adapters.qqguild.event import AtMessageCreateEvent, MessageCreateEvent, DirectMessageCreateEvent

import httpx
from nonebot.adapters.qqguild import Message,MessageSegment
import base64
# from .config import plugin_config
from .SDUtils import SDUtils
from PIL import Image
from io import BytesIO
from typing import Union
get_image = on_command('t', priority=1)


@get_image.got("img_attach", prompt="请发送图片",)
async def _(matcher: Matcher, img_attach: Message = Arg()):
    img_url = "https://"+img_attach[0].data["url"]
    with httpx.Client() as client:
        response = client.get(img_url)
        if response.status_code != 200:
            print(f"下载失败，错误代码：{response.status_code}")
    pil_image = Image.open(BytesIO(response.content))

    image_base64 = base64.b64encode(response.content).decode('utf-8')

    sd = SDUtils()
    tags = await sd.img2tags(image_base64)
    img_new = await sd.img2img(tags, pil_image)
    await matcher.send(MessageSegment.file_image(img_new))
