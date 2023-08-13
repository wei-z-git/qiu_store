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

# from nonebot.permission import SUPERUSER
# from nonebot.exception import ActionFailed
from typing import Union

from .config import plugin_config
from .AifadianUtils import AifadianUtils



# Rules
# 判断是否为私聊消息
async def is_private_message(event: DirectMessageCreateEvent) -> bool:
    return isinstance(event, DirectMessageCreateEvent)

# matchers
matcher_hellomessage = on_command(
    'hi', aliases={'1v1'}, priority=1, rule=to_me)
matcher_product_list = on_command(
    '商品列表', aliases={'列表'}, priority=2, rule=is_private_message)
matcher_call_bot = on_command(
    '召唤', aliases={'帮助'}, priority=2, rule=is_private_message)
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


# Handles: Call bot
@matcher_call_bot.got("option", prompt=question)
async def call_bot(state: T_State, matcher: Matcher, option: Message = Arg(), answer: str = ArgPlainText("option")):
    aifadian = AifadianUtils(plugin_config.aifadian_token,
                             plugin_config.aifadian_user_id)
    match answer:
        case "1":
            # 1.自动购买(包含2+3+4)
            # a.发送商品信息，b.将下单设置状态,进入下单流程
            formating_plan_list = await aifadian.get_formatting_plan_list()
            await matcher.send(f"商品信息如下：\n{formating_plan_list}")
            state["if_order"] = True
        case "2":
            #  2.查询商品列表
            formating_plan_list = await aifadian.get_formatting_plan_list()
            await matcher.finish(formating_plan_list)
        case "3":
            # 3.输入订单号
            state["if_check_order_id"] = True
            state["if_order"] = False
            matcher.set_arg("plan_id", option)  # 给planid设置一个值，让order_id询问跳过
        case "0":
            # 0.退出
            await matcher.finish(f"拜拜了您嘞~")
        case _:
            # 可以使用平台的 Message 类直接构造模板消息
            await matcher.reject(option.template("哥哥，泥在说些甚么！洒家听不懂！请再说一遍！ok?"))


@matcher_call_bot.got("if_order")
@matcher_call_bot.got("plan_id", prompt="请输入plan_id...,例如c797b4d4289f11eebd3052540025c377")
async def send_order_url(state: T_State, matcher: Matcher, plan_id: str = ArgPlainText("plan_id")):
    if state["if_order"] == True:
        qr_code_bytes = await AifadianUtils(plugin_config.aifadian_token,
                                            plugin_config.aifadian_user_id).generate_QRcode(plan_id)
        await matcher.send(f"请扫描二维码或使用链接下单(需要把'。'换成'.'), 并再购买完成后输入订单号...")
        url = await AifadianUtils.convert_message_url("地址: afdian.net/item/"+plan_id)
        await matcher.send(url)
        await matcher.send(MessageSegment.file_image(qr_code_bytes))
        state["if_check_order_id"] = True


@matcher_call_bot.got("if_check_order_id")
@matcher_call_bot.got("order_id", prompt="请输入订单号...")
async def check_order(state: T_State, matcher: Matcher, order_id: str = ArgPlainText("order_id")):
    if state["if_check_order_id"] == True:
        order_result = await AifadianUtils(plugin_config.aifadian_token,
                                           plugin_config.aifadian_user_id).deliver_goods(order_id, plugin_config.goods_secrets_url)
        order_result = await AifadianUtils.convert_message_url(str(order_result))
        await matcher.send(order_result)


@matcher_product_test.handle()
async def _(matcher: Matcher, event: DirectMessageCreateEvent) -> None:
    qr_code_bytes = await AifadianUtils.generate_QRcode("c797b4d4289f11eebd3052540025c377")
    await matcher.send("www。baidupan。com/phub")
