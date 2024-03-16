from nonebot import on_command
from nonebot.adapters import Bot, Message
from nonebot.matcher import Matcher
from nonebot.adapters.qqguild import Bot, MessageSegment
from nonebot.adapters.qqguild.event import AtMessageCreateEvent, MessageCreateEvent, DirectMessageCreateEvent
from nonebot.adapters.qqguild.exception import AuditException
from nonebot.typing import T_State
from nonebot.params import Depends,Arg, ArgPlainText
from nonebot.rule import to_me
from nonebot.log import logger

from typing import Union

from .config import plugin_config
from .SDUtils import AifadianUtils



# Rules
# 判断是否为私聊消息
async def is_private_message(event: DirectMessageCreateEvent) -> bool:
    return isinstance(event, DirectMessageCreateEvent)

# matchers
matcher_hellomessage = on_command(
    'hi', aliases={'1v1'}, priority=1, rule=to_me)
matcher_product_test = on_command('test', priority=3, rule=is_private_message)


# Handles: hello message
@matcher_hellomessage.handle()
async def _(bot: Bot, event: Union[AtMessageCreateEvent, MessageCreateEvent]) -> None:
    private_guild = await bot.post_dms(recipient_id=event.author.id, source_guild_id=event.guild_id)
    await matcher_hellomessage.send(f"1v1频道已创建，私信频道:{private_guild.guild_id}")
    try:
        # await matcher.send("如何购买？商品列表如下:")
        await bot.post_dms_messages(guild_id=private_guild.guild_id, content="1v1辅导频道已创建,请继续使用'/召唤'指令")
    except AuditException:
        logger.info("网络相关的AuditException, 群佬说可以忽略")


question = "洒家来啦~~，哥哥有何吩咐:\n  1.自动购买(包含2+3+4)\n  2.查询商品列表\n 3.输入订单号\n 0.退出\n请哥哥选择!\n ---消息来自美少女客服小鸠机器人"


# Dependence checks
def check(key: str):
    async def _d(state: T_State, matcher: Matcher):
        if state[key] == False:
            matcher.skip()
    return Depends(_d)

