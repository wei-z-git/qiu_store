"""
猜字谜，用来过审
"""

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


question = "题目：一只狗，两个口，谁遇它谁发愁。猜一字"

matcher_caizimi = on_command('猜字谜', aliases={'caizimi'}, priority=4,rule=to_me)

@matcher_caizimi.got("option", prompt=question)
async def call_robot(bot: Bot, matcher: Matcher, option: Message = Arg(), answer: str = ArgPlainText("option")):
    match answer:
        case "哭":
            await matcher_caizimi.finish(f"恭喜！答案正确！")
        case "公布答案":
            await matcher_caizimi.finish(f"答案是：哭")
        case "结束游戏":
            await matcher_caizimi.finish(f"游戏结束")
        case _:
            await matcher.reject("答案错误！")
