from nonebot import on_command, get_bot
from nonebot.adapters import Message, Bot
from nonebot.matcher import Matcher
from nonebot.adapters.qqguild import Bot
from nonebot.adapters.qqguild.event import AtMessageCreateEvent


from nonebot.params import CommandArg, Arg, ArgPlainText
from nonebot.permission import SUPERUSER
from nonebot.log import logger
from nonebot.exception import ActionFailed
from nonebot.rule import to_me
import random

# from .config import plugin_config


# async def search_group_mem_list_detail(bot: Bot, matcher: Matcher,event: AtMessageCreateEvent) -> None:
#     """
#         查询不活跃的成员明细
#     """
#     gid = int(event.group_id)
#     try:
#         await matcher.send("helloworld qq频道")

#     except ActionFailed:
#         await matcher.finish(f"error")



matcher_hellomessage = on_command('hello', aliases={'你好', '你好啊'}, priority=4)

@matcher_hellomessage.handle()
async def _(matcher: Matcher):
    await matcher.send("hello")