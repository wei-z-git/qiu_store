from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.params import Arg
from nonebot.adapters.qqguild import Message, MessageSegment

# from .config import plugin_config
from .SDUtils import SDUtils

get_image = on_command('转生', aliases={'rb'}, priority=1)


@get_image.got("img_attach", prompt="请发送图片",)
async def _(matcher: Matcher, img_attach: Message = Arg()):
    await matcher.send(f"正在生成中，请稍后...")
    img_url = "https://"+img_attach[0].data["url"]
    sd = SDUtils()
    pil_image, image_base64 = await sd.download_img(img_url)
    tags = await sd.img2tags(image_base64)
    img_new = await sd.img2img(tags, pil_image)
    await matcher.send(MessageSegment.file_image(img_new))
